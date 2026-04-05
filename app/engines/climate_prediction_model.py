"""
Climate Prediction Model

ML pipeline for predicting future climate patterns using an ensemble of
Random Forest and exponential-smoothing (LSTM-proxy) approaches.

The ensemble weights RF at 40% and the time-series smoother at 60%.
No external deep-learning framework is required — all predictions use
numpy and scikit-learn which are already in the project's dependencies.
"""
import logging
from typing import Dict, List, Tuple

import numpy as np

try:
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.preprocessing import StandardScaler
    _SKLEARN_AVAILABLE = True
except ImportError:  # pragma: no cover
    _SKLEARN_AVAILABLE = False

logger = logging.getLogger(__name__)

# Ensemble weight configuration (must sum to 1.0)
RF_WEIGHT = 0.40
SMOOTH_WEIGHT = 0.60


class ClimatePredictionModel:
    """Ensemble ML model for predicting future temperature and rainfall trends.

    Combines Random Forest regression (40 %) with exponential smoothing
    (analogous to an LSTM cell state update, 60 %) to produce robust
    multi-year climate forecasts.
    """

    def __init__(self) -> None:
        """Initialise the model components."""
        self.temp_model: "RandomForestRegressor | None" = None
        self.rain_model: "RandomForestRegressor | None" = None
        self.scaler_X = StandardScaler() if _SKLEARN_AVAILABLE else None
        self.is_fitted = False

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def fit(self, temperature_series: List[float], rainfall_series: List[float]) -> None:
        """Train Random Forest models on historical monthly climate data.

        Args:
            temperature_series: Monthly temperature values (°C). At least 24.
            rainfall_series: Monthly rainfall values (mm). At least 24.
        """
        if not _SKLEARN_AVAILABLE:
            logger.warning("scikit-learn not available; RF models will be skipped.")
            return

        temp_arr = np.array(temperature_series, dtype=float)
        rain_arr = np.array(rainfall_series, dtype=float)

        if len(temp_arr) < 24 or len(rain_arr) < 24:
            raise ValueError("Need at least 24 months of data to train models.")

        X_temp, y_temp = self._build_lag_features(temp_arr)
        X_rain, y_rain = self._build_lag_features(rain_arr)

        self.scaler_X.fit(np.vstack([X_temp, X_rain]))
        Xs_temp = self.scaler_X.transform(X_temp)
        Xs_rain = self.scaler_X.transform(X_rain)

        self.temp_model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
        self.rain_model = RandomForestRegressor(n_estimators=100, random_state=42, n_jobs=-1)
        self.temp_model.fit(Xs_temp, y_temp)
        self.rain_model.fit(Xs_rain, y_rain)
        self.is_fitted = True
        logger.info("Climate RF models fitted on %d months of data.", len(temp_arr))

    def predict_future_climate(
        self,
        temperature_series: List[float],
        rainfall_series: List[float],
        n_months_ahead: int = 120,
    ) -> Dict:
        """Predict future climate statistics using the ensemble.

        Args:
            temperature_series: Historical monthly temperatures (°C).
            rainfall_series: Historical monthly rainfall (mm).
            n_months_ahead: How many months ahead to forecast (default 120 = 10 years).

        Returns:
            Dict with predicted temperature and rainfall statistics for the
            forecast horizon.
        """
        if not self.is_fitted:
            self.fit(temperature_series, rainfall_series)

        temp_forecast = self._ensemble_forecast(
            np.array(temperature_series, dtype=float), n_months_ahead, self.temp_model
        )
        rain_forecast = self._ensemble_forecast(
            np.array(rainfall_series, dtype=float), n_months_ahead, self.rain_model
        )
        rain_forecast = np.maximum(rain_forecast, 0)

        return {
            "predicted_temperature_monthly": temp_forecast.tolist(),
            "predicted_rainfall_monthly": rain_forecast.tolist(),
            "predicted_temp_avg": float(np.mean(temp_forecast)),
            "predicted_temp_max": float(np.max(temp_forecast)),
            "predicted_temp_min": float(np.min(temp_forecast)),
            "predicted_rainfall_avg": float(np.mean(rain_forecast)),
            "predicted_rainfall_total_annual": float(np.sum(rain_forecast[:12])),
            "temperature_trend": self._calculate_trend(temp_forecast),
            "rainfall_trend": self._calculate_trend(rain_forecast),
            "forecast_months": n_months_ahead,
        }

    def get_yearly_projections(
        self,
        temperature_series: List[float],
        rainfall_series: List[float],
        years: List[int] = None,
    ) -> Dict[str, Dict]:
        """Return annual average climate projections for specific future years.

        Args:
            temperature_series: Historical monthly temperatures.
            rainfall_series: Historical monthly rainfall.
            years: Target years (default [2030, 2035, 2050]).

        Returns:
            Dict keyed by year string with avg_temp and avg_rainfall.
        """
        if years is None:
            years = [2030, 2035, 2050]

        base_year = 2024
        max_ahead = (max(years) - base_year) * 12 + 12
        prediction = self.predict_future_climate(
            temperature_series, rainfall_series, n_months_ahead=max_ahead
        )
        temp_forecast = np.array(prediction["predicted_temperature_monthly"])
        rain_forecast = np.array(prediction["predicted_rainfall_monthly"])

        result: Dict[str, Dict] = {}
        for year in years:
            months_from_now = (year - base_year) * 12
            start = max(0, months_from_now)
            end = start + 12
            if end <= len(temp_forecast):
                result[str(year)] = {
                    "avg_temp": float(np.mean(temp_forecast[start:end])),
                    "avg_rainfall": float(np.mean(rain_forecast[start:end])),
                }
            else:
                # Fallback: project linearly from the last known values
                temp_delta = prediction["temperature_trend"] * months_from_now
                rain_delta = prediction["rainfall_trend"] * months_from_now
                result[str(year)] = {
                    "avg_temp": float(np.mean(temperature_series[-12:])) + temp_delta,
                    "avg_rainfall": float(np.mean(rainfall_series[-12:])) + rain_delta,
                }

        return result

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _build_lag_features(series: np.ndarray, n_lags: int = 12) -> Tuple[np.ndarray, np.ndarray]:
        """Build lag-feature matrix for supervised learning.

        Each row consists of the previous ``n_lags`` observations, and the
        target is the next (n_lags+1) observation.
        """
        X, y = [], []
        for i in range(n_lags, len(series)):
            X.append(series[i - n_lags: i])
            y.append(series[i])
        return np.array(X), np.array(y)

    def _rf_forecast(
        self,
        series: np.ndarray,
        n_months_ahead: int,
        model: "RandomForestRegressor",
        n_lags: int = 12,
    ) -> np.ndarray:
        """Iterative multi-step RF forecast: feed predictions back as new lags."""
        current_window = series[-n_lags:].copy()
        predictions = []

        for _ in range(n_months_ahead):
            X = self.scaler_X.transform([current_window])
            pred = float(model.predict(X)[0])
            predictions.append(pred)
            current_window = np.append(current_window[1:], pred)

        return np.array(predictions)

    @staticmethod
    def _exponential_smooth_forecast(series: np.ndarray, n_months_ahead: int, alpha: float = 0.3) -> np.ndarray:
        """Annual-mean-based extrapolation with linear trend (seasonal-safe).

        Computes the long-term annual mean and trend from annual averages, then
        projects forward — avoiding the pitfall where simple EMA converges to
        the value at an arbitrary point in the seasonal cycle.
        """
        # Align to complete annual cycles
        n_complete_years = len(series) // 12
        if n_complete_years < 2:
            # Fallback: just repeat the overall mean
            mean_val = float(np.mean(series))
            return np.full(n_months_ahead, mean_val)

        # Compute per-year averages
        yearly_means = np.array([
            np.mean(series[i * 12: (i + 1) * 12])
            for i in range(n_complete_years)
        ])

        # Linear trend across yearly means
        years_idx = np.arange(n_complete_years)
        slope, intercept = np.polyfit(years_idx, yearly_means, 1)

        # Project forward: fill each future month with its annual mean estimate
        last_year_idx = n_complete_years - 1
        last_year_data = series[-12:]
        last_year_mean = float(np.mean(last_year_data))
        forecast = []
        for month in range(n_months_ahead):
            year_ahead = (month // 12) + 1
            projected_annual_mean = intercept + slope * (last_year_idx + year_ahead)
            # Re-add the seasonal deviation from the last complete annual cycle
            seasonal_month = month % 12
            seasonal_dev = float(last_year_data[seasonal_month] - last_year_mean)
            forecast.append(projected_annual_mean + seasonal_dev)

        return np.array(forecast)

    def _ensemble_forecast(
        self,
        series: np.ndarray,
        n_months_ahead: int,
        rf_model: "RandomForestRegressor | None",
    ) -> np.ndarray:
        """Blend RF and smoothing forecasts using predefined weights."""
        smooth_fc = self._exponential_smooth_forecast(series, n_months_ahead)

        if rf_model is not None and self.is_fitted:
            rf_fc = self._rf_forecast(series, n_months_ahead, rf_model)
            return RF_WEIGHT * rf_fc + SMOOTH_WEIGHT * smooth_fc

        # Fall back to smoothing only if RF is unavailable
        return smooth_fc

    @staticmethod
    def _calculate_trend(forecast: np.ndarray) -> float:
        """Return the average monthly change (slope) in the forecast series."""
        if len(forecast) < 2:
            return 0.0
        slope = float(np.polyfit(np.arange(len(forecast)), forecast, 1)[0])
        return slope
