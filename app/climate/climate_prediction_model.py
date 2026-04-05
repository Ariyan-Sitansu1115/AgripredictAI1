"""
climate_prediction_model.py
============================
Machine-learning pipeline that predicts future climate patterns (5–10 years ahead)
based on historical observations and IPCC trend parameters.

Model choices
-------------
* **Random Forest Regressor** (default) – ensemble method that handles small
  non-linear datasets well; fast, interpretable, no GPU required.
* **LinearTrend** (fallback) – simple linear extrapolation used when fewer than
  MIN_TRAIN_SAMPLES data points are available.

Features used for training
--------------------------
  year, latitude, longitude, month_index (0–11 rolling), baseline_temp,
  baseline_rainfall, co2_proxy (year - 1990, proxy for cumulative GHG forcing)

The model is trained on the 10-year historical window provided by
:mod:`climate_data_loader` and then used to forecast the requested horizon.

Public API
----------
    predict_future_climate(bundle, horizon_years=7)
        -> ClimatePrediction
"""

from __future__ import annotations

import logging
import math
from dataclasses import dataclass, field
from typing import List, Optional

logger = logging.getLogger(__name__)

# Minimum samples required to train the Random Forest; fall back to linear otherwise.
MIN_RF_SAMPLES = 6

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class FutureYearClimate:
    """Predicted climate for a single future year."""
    year: int
    avg_temperature: float   # °C
    total_rainfall: float    # mm
    avg_humidity: float      # %


@dataclass
class ClimatePrediction:
    """Full prediction result returned by predict_future_climate()."""
    predicted_years: List[FutureYearClimate]
    # Aggregate changes relative to current baseline
    temperature_change: float    # °C (positive = warmer)
    rainfall_variation: float    # % change
    humidity_change: float       # % change (absolute percentage points)
    # Model confidence (0–1); RF uses out-of-bag score proxy, linear uses fixed value
    confidence_score: float
    model_type: str              # "RandomForest" | "LinearTrend"


# ---------------------------------------------------------------------------
# Feature engineering helpers
# ---------------------------------------------------------------------------

def _co2_proxy(year: int) -> float:
    """Proxy for cumulative GHG forcing: linear increase since 1990."""
    return float(max(0, year - 1990))


def _build_features(year: int, lat: float, lon: float,
                    base_temp: float, base_rain: float) -> List[float]:
    """Construct a feature vector for a single year."""
    return [
        float(year),
        lat,
        lon,
        base_temp,
        base_rain,
        _co2_proxy(year),
    ]


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------

def predict_future_climate(
    bundle: "ClimateDataBundle",  # type: ignore[name-defined]  # noqa: F821
    horizon_years: int = 7,
) -> ClimatePrediction:
    """Predict climate for the next *horizon_years* years using ML.

    The function trains a small Random Forest on the 10-year historical window
    embedded in *bundle* and forecasts the requested horizon.

    Args:
        bundle:        A :class:`~climate_data_loader.ClimateDataBundle` instance.
        horizon_years: Number of years ahead to predict (1–10).

    Returns:
        A populated :class:`ClimatePrediction`.
    """
    horizon_years = max(1, min(10, horizon_years))

    historical = bundle.historical
    n_samples = len(historical)

    lat  = bundle.latitude
    lon  = bundle.longitude
    base_temp = bundle.baseline_temp
    base_rain = bundle.baseline_rainfall

    # ----------------------------------------------------------------
    # Build training data
    # ----------------------------------------------------------------
    X_temp: List[List[float]] = []
    y_temp: List[float] = []
    X_rain: List[List[float]] = []
    y_rain: List[float] = []
    X_hum:  List[List[float]] = []
    y_hum:  List[float] = []

    for rec in historical:
        feats = _build_features(rec.year, lat, lon, base_temp, base_rain)
        X_temp.append(feats);  y_temp.append(rec.avg_temperature)
        X_rain.append(feats);  y_rain.append(rec.total_rainfall)
        X_hum.append(feats);   y_hum.append(rec.avg_humidity)

    # ----------------------------------------------------------------
    # Choose model and train
    # ----------------------------------------------------------------
    model_type: str
    confidence: float
    rf_temp = rf_rain = rf_hum = None

    if n_samples >= MIN_RF_SAMPLES:
        try:
            from sklearn.ensemble import RandomForestRegressor  # type: ignore

            def _fit(X: List[List[float]], y: List[float]) -> RandomForestRegressor:
                model = RandomForestRegressor(
                    n_estimators=50,
                    max_depth=4,
                    random_state=42,
                    oob_score=True,
                )
                model.fit(X, y)
                return model

            rf_temp = _fit(X_temp, y_temp)
            rf_rain = _fit(X_rain, y_rain)
            rf_hum  = _fit(X_hum,  y_hum)

            # OOB score as a proxy for model confidence (clamp to [0.5, 0.97])
            oob_scores = [
                getattr(rf_temp, "oob_score_", 0.7),
                getattr(rf_rain, "oob_score_", 0.7),
                getattr(rf_hum,  "oob_score_", 0.7),
            ]
            raw_conf = sum(oob_scores) / 3
            confidence = round(max(0.50, min(0.97, raw_conf)), 2)
            model_type = "RandomForest"
            logger.info(
                "RandomForest trained | n_samples=%d oob_conf=%.2f",
                n_samples, confidence,
            )
        except ImportError:
            logger.warning("scikit-learn not available; falling back to LinearTrend.")
            model_type = "LinearTrend"
            confidence = 0.72
    else:
        model_type = "LinearTrend"
        confidence = 0.72
        logger.info("Using LinearTrend (n_samples=%d < %d)", n_samples, MIN_RF_SAMPLES)

    # ----------------------------------------------------------------
    # Generate predictions for each future year
    # ----------------------------------------------------------------
    current_year = historical[-1].year if historical else 2024
    predicted_years: List[FutureYearClimate] = []

    for h in range(1, horizon_years + 1):
        year = current_year + h
        feats = _build_features(year, lat, lon, base_temp, base_rain)

        if model_type == "RandomForest" and rf_temp is not None:
            pred_temp = float(rf_temp.predict([feats])[0])
            pred_rain = float(rf_rain.predict([feats])[0])
            pred_hum  = float(rf_hum.predict([feats])[0])
        else:
            # Linear trend extrapolation
            pred_temp = base_temp + bundle.temp_trend_per_year    * h
            pred_rain = base_rain + bundle.rainfall_trend_per_year * h
            pred_hum  = bundle.baseline_humidity + bundle.humidity_trend_per_year * h

        # Enforce physically plausible bounds
        pred_temp = round(max(-10.0, min(55.0, pred_temp)), 2)
        pred_rain = round(max(0.0,   pred_rain), 1)
        pred_hum  = round(max(10.0,  min(98.0, pred_hum)), 1)

        predicted_years.append(FutureYearClimate(
            year=year,
            avg_temperature=pred_temp,
            total_rainfall=pred_rain,
            avg_humidity=pred_hum,
        ))

    # ----------------------------------------------------------------
    # Aggregate change summary (vs current baseline)
    # ----------------------------------------------------------------
    mid_year_pred = predicted_years[len(predicted_years) // 2]
    temp_change  = round(mid_year_pred.avg_temperature - base_temp, 2)
    rain_change  = round(
        (mid_year_pred.total_rainfall - base_rain) / max(1.0, base_rain) * 100, 1
    )
    humid_change = round(mid_year_pred.avg_humidity - bundle.baseline_humidity, 1)

    return ClimatePrediction(
        predicted_years=predicted_years,
        temperature_change=temp_change,
        rainfall_variation=rain_change,
        humidity_change=humid_change,
        confidence_score=confidence,
        model_type=model_type,
    )
