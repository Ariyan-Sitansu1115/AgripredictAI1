"""
Climate Data Loader

Handles loading and preprocessing climate data from various sources including
historical records and IPCC climate projection datasets.
"""
import logging
from typing import Dict, List

import numpy as np

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ClimateDataLoader:
    """Load and preprocess climate data for ML models."""

    def __init__(self) -> None:
        """Initialize climate data loader with predefined climate zone thresholds."""
        self.historical_climate_cache: Dict = {}
        self.climate_zones = {
            "tropical": {"temp": (20, 30), "rainfall": (1500, 3000)},
            "subtropical": {"temp": (15, 28), "rainfall": (1000, 2500)},
            "temperate": {"temp": (10, 20), "rainfall": (600, 1500)},
            "arid": {"temp": (20, 40), "rainfall": (0, 400)},
            "semi-arid": {"temp": (15, 35), "rainfall": (400, 900)},
        }

    def load_historical_climate_data(
        self, latitude: float, longitude: float
    ) -> Dict:
        """Load historical climate data for a location.

        Simulates 30 years of monthly climate data with realistic seasonal
        patterns, warming trends, and monsoon dynamics based on location.

        Args:
            latitude: Geographic latitude of the location.
            longitude: Geographic longitude of the location.

        Returns:
            Dict containing monthly temperature, rainfall, humidity arrays
            (360 data points each) along with summary averages.
        """
        cache_key = f"{round(latitude, 2)}_{round(longitude, 2)}"
        if cache_key in self.historical_climate_cache:
            return self.historical_climate_cache[cache_key]

        try:
            rng = np.random.default_rng(seed=int(abs(latitude * 100 + longitude * 10)))
            months = np.arange(360)  # 30 years × 12 months

            # Temperature: seasonal pattern with long-term warming trend
            base_temp = 15 + abs(latitude) * 0.3 if abs(latitude) < 30 else 25 - abs(latitude) * 0.1
            temp_amplitude = 8 - abs(latitude) * 0.05
            temp_base = base_temp + temp_amplitude * np.sin(2 * np.pi * months / 12)
            temp_trend = np.linspace(0, 1.5, 360)
            temperature = temp_base + temp_trend + rng.normal(0, 1, 360)

            # Rainfall: monsoon-influenced pattern with declining trend
            # Adjust phase offset based on hemisphere
            phase = np.pi / 2 if latitude >= 0 else -np.pi / 2
            # Scale base rainfall to realistic monthly values (50-200mm/month average)
            base_monthly_rain = 80 + max(0, 40 - abs(latitude) * 0.5)  # ~80-100mm/month
            seasonal_amplitude = base_monthly_rain * 1.2  # peak is 2.2x base
            rainfall_base = (
                base_monthly_rain
                + seasonal_amplitude * np.maximum(0, np.sin(2 * np.pi * months / 12 + phase))
            )
            rainfall_trend = np.linspace(0, -base_monthly_rain * 0.15, 360)
            rainfall = rainfall_base + rainfall_trend + rng.normal(0, 8, 360)
            rainfall = np.maximum(rainfall, 0)

            # Humidity: inversely correlated with temperature
            humidity = 65 + 15 * np.sin(2 * np.pi * months / 12) - 0.5 * (temperature - 20)
            humidity = np.clip(humidity, 20, 95)

            result = {
                "latitude": latitude,
                "longitude": longitude,
                "temperature_monthly": temperature.tolist(),
                "rainfall_monthly": rainfall.tolist(),
                "humidity_monthly": humidity.tolist(),
                "temp_avg": float(np.mean(temperature)),
                "rainfall_avg": float(np.mean(rainfall)),
                "humidity_avg": float(np.mean(humidity)),
            }
            self.historical_climate_cache[cache_key] = result
            return result

        except Exception as exc:
            logger.error("Error loading climate data: %s", exc)
            raise

    def load_ipcc_projections(
        self,
        latitude: float,
        longitude: float,
        years: List[int] = None,
    ) -> Dict:
        """Load IPCC RCP 4.5 climate projections for specified future years.

        Uses the RCP 4.5 (moderate emissions) scenario to estimate temperature
        increase, rainfall change, and humidity change relative to 2024.

        Args:
            latitude: Geographic latitude.
            longitude: Geographic longitude.
            years: List of target years to project. Defaults to [2030, 2050].

        Returns:
            Dict keyed by year string containing temperature_change,
            rainfall_change, humidity_change, and confidence values.
        """
        if years is None:
            years = [2030, 2050]

        try:
            projections: Dict = {}
            base_year = 2024

            for year in years:
                years_ahead = year - base_year

                # RCP 4.5: ~1.2 °C by 2040, ~2.0 °C by 2100
                temp_change = 1.2 + (years_ahead / 100) * 0.8
                # Rainfall: slight decrease on average (highly location-dependent)
                rainfall_change = -5 - (years_ahead / 100) * 10
                # Humidity decreases as temperatures rise
                humidity_change = -2 - (years_ahead / 100) * 3
                # Confidence decreases for projections further into the future
                confidence = 0.82 if years_ahead <= 30 else 0.70

                projections[str(year)] = {
                    "year": year,
                    "temperature_change": float(temp_change),
                    "rainfall_change": float(rainfall_change),
                    "humidity_change": float(humidity_change),
                    "confidence": confidence,
                }

            return projections

        except Exception as exc:
            logger.error("Error loading IPCC projections: %s", exc)
            raise

    def get_climate_zone(
        self,
        latitude: float,
        avg_temp: float,
        avg_rainfall: float,
    ) -> str:
        """Determine the climate zone based on temperature and annual rainfall.

        Args:
            latitude: Geographic latitude (unused but kept for API compatibility).
            avg_temp: Long-run average annual temperature (°C).
            avg_rainfall: Average monthly rainfall (mm).  Annual equivalent is
                          computed internally by multiplying by 12.

        Returns:
            Climate zone string: one of tropical, subtropical, temperate,
            arid, or semi-arid.
        """
        annual_rainfall = avg_rainfall * 12  # convert monthly mm to annual mm
        if avg_temp > 20 and annual_rainfall > 1500:
            return "tropical"
        if avg_temp > 15 and annual_rainfall > 1000:
            return "subtropical"
        if avg_temp < 15 and annual_rainfall > 600:
            return "temperate"
        if annual_rainfall < 400:
            return "arid"
        return "semi-arid"

    def get_projected_climate(
        self,
        latitude: float,
        longitude: float,
        target_year: int = 2035,
    ) -> Dict:
        """Combine historical data with IPCC projections to get future climate.

        Args:
            latitude: Geographic latitude.
            longitude: Geographic longitude.
            target_year: The future year for the projection.

        Returns:
            Dict with projected temperature, rainfall, humidity, and climate zone.
        """
        historical = self.load_historical_climate_data(latitude, longitude)
        projections = self.load_ipcc_projections(latitude, longitude, years=[target_year])
        proj = projections[str(target_year)]

        projected_temp = historical["temp_avg"] + proj["temperature_change"]
        # Rainfall change is expressed as percentage shift
        projected_rainfall = historical["rainfall_avg"] * (1 + proj["rainfall_change"] / 100)
        projected_humidity = historical["humidity_avg"] + proj["humidity_change"]
        projected_humidity = float(np.clip(projected_humidity, 20, 95))

        climate_zone = self.get_climate_zone(latitude, projected_temp, projected_rainfall)

        return {
            "target_year": target_year,
            "projected_temp": projected_temp,
            "projected_rainfall": projected_rainfall,
            "projected_humidity": projected_humidity,
            "climate_zone": climate_zone,
            "temperature_change": proj["temperature_change"],
            "rainfall_change": proj["rainfall_change"],
            "humidity_change": proj["humidity_change"],
            "confidence": proj["confidence"],
            "historical_temp": historical["temp_avg"],
            "historical_rainfall": historical["rainfall_avg"],
            "historical_humidity": historical["humidity_avg"],
        }
