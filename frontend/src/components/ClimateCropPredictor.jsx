/**
 * ClimateCropPredictor.jsx
 *
 * AI-powered climate-resilient crop recommendation component.
 * Farmers enter their location and soil data to receive ML-driven
 * crop recommendations suitable for projected climate conditions over
 * the next 5–10 years.
 */
import React, { useState } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  TextField,
  Button,
  CircularProgress,
  Chip,
  Divider,
  Slider,
  Alert,
} from '@mui/material';
import ThermostatIcon from '@mui/icons-material/Thermostat';
import OpacityIcon from '@mui/icons-material/Opacity';
import GrassIcon from '@mui/icons-material/Grass';
import ScienceIcon from '@mui/icons-material/Science';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';
import BarChartIcon from '@mui/icons-material/BarChart';
import WaterDropIcon from '@mui/icons-material/WaterDrop';
import {
  LineChart,
  Line,
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from 'recharts';
import axios from 'axios';
import '../styles/climate-predictor.css';

// ── Constants ──────────────────────────────────────────────────────────────

const DEFAULT_FORM = {
  latitude: '',
  longitude: '',
  soil_ph: 6.5,
  nitrogen: 80,
  phosphorus: 45,
  potassium: 50,
  target_year: 2035,
};

const RESILIENCE_LABEL = (score) => {
  if (score >= 0.75) return { label: 'High', cls: 'high' };
  if (score >= 0.50) return { label: 'Medium', cls: 'medium' };
  return { label: 'Low', cls: 'low' };
};

// ── Sub-components ─────────────────────────────────────────────────────────

function ScoreBar({ label, value }) {
  return (
    <div className="score-bar-wrap">
      <div className="score-bar-label">
        <span>{label}</span>
        <span>{(value * 100).toFixed(0)}%</span>
      </div>
      <div className="score-bar-track">
        <div className="score-bar-fill" style={{ width: `${value * 100}%` }} />
      </div>
    </div>
  );
}

function CropCard({ crop, rank }) {
  const { label, cls } = RESILIENCE_LABEL(crop.resilience_score);

  return (
    <div className="glass-card crop-card">
      <div className="crop-card-header">
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <Typography
            variant="caption"
            sx={{
              background: '#f0fdf4',
              color: '#047857',
              fontWeight: 700,
              px: 1,
              py: 0.25,
              borderRadius: '6px',
              fontSize: '0.75rem',
            }}
          >
            #{rank}
          </Typography>
          <p className="crop-name">{crop.crop}</p>
        </Box>
        <span className={`resilience-badge ${cls}`}>
          {label} · {(crop.resilience_score * 100).toFixed(0)}%
        </span>
      </div>

      <div className="crop-meta">
        <span className="crop-meta-item">
          <CalendarTodayIcon sx={{ fontSize: 14 }} />
          {crop.planting_season}
        </span>
        <span className="crop-meta-item">
          <GrassIcon sx={{ fontSize: 14 }} />
          Yield: {crop.expected_yield.toLocaleString()} kg/ha
        </span>
      </div>

      {crop.description && (
        <Typography variant="body2" sx={{ color: '#6b7280', fontSize: '0.82rem', mb: 1 }}>
          {crop.description}
        </Typography>
      )}

      <Divider sx={{ my: 0.75 }} />

      <ScoreBar label="Temperature Fit" value={crop.temperature_score} />
      <ScoreBar label="Rainfall Fit"    value={crop.rainfall_score} />
      <ScoreBar label="Drought Tolerance" value={crop.drought_tolerance} />
      <ScoreBar label="Heat Tolerance"    value={crop.heat_tolerance} />
    </div>
  );
}

function ClimateSummary({ summary }) {
  const stats = [
    { label: 'Temp Change',     value: summary.temperature_change,      icon: <ThermostatIcon sx={{ fontSize: 18 }} /> },
    { label: 'Rainfall',        value: summary.rainfall_variation,       icon: <OpacityIcon    sx={{ fontSize: 18 }} /> },
    { label: 'Growing Season',  value: summary.growing_season_change,    icon: <CalendarTodayIcon sx={{ fontSize: 18 }} /> },
    { label: 'Confidence',      value: `${(summary.confidence_score * 100).toFixed(0)}%`, icon: <ScienceIcon sx={{ fontSize: 18 }} /> },
  ];

  return (
    <div className="glass-card climate-summary">
      <Typography variant="subtitle1" sx={{ fontWeight: 700, color: '#065f46', mb: 0.5 }}>
        📊 Future Climate Summary · {summary.climate_zone}
      </Typography>
      <Typography variant="body2" sx={{ color: '#6b7280', mb: 1, fontSize: '0.82rem' }}>
        Projected avg temp: <strong>{summary.projected_temp}°C</strong> · 
        Avg monthly rainfall: <strong>{summary.projected_rainfall_monthly} mm</strong>
      </Typography>
      <div className="climate-stat-grid">
        {stats.map((s) => (
          <div className="climate-stat" key={s.label}>
            <div style={{ color: '#10b981', marginBottom: 4 }}>{s.icon}</div>
            <div className="climate-stat-value">{s.value}</div>
            <div className="climate-stat-label">{s.label}</div>
          </div>
        ))}
      </div>
    </div>
  );
}

function TemperatureChart({ data }) {
  return (
    <div className="glass-card" style={{ padding: '1rem' }}>
      <p className="chart-title">
        <ThermostatIcon sx={{ fontSize: 16, verticalAlign: 'middle', mr: 0.5 }} />
        Predicted Temperature Trend (°C)
      </p>
      <ResponsiveContainer width="100%" height={200}>
        <LineChart data={data} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0fdf4" />
          <XAxis dataKey="year" tick={{ fontSize: 11 }} />
          <YAxis tick={{ fontSize: 11 }} unit="°C" />
          <Tooltip formatter={(v) => [`${v}°C`, 'Avg Temp']} />
          <Legend />
          <Line
            type="monotone"
            dataKey="value"
            name="Avg Temperature"
            stroke="#ef4444"
            strokeWidth={2}
            dot={{ r: 3, fill: '#ef4444' }}
            activeDot={{ r: 5 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}

function RainfallChart({ data }) {
  return (
    <div className="glass-card" style={{ padding: '1rem' }}>
      <p className="chart-title">
        <WaterDropIcon sx={{ fontSize: 16, verticalAlign: 'middle', mr: 0.5 }} />
        Predicted Monthly Rainfall Trend (mm)
      </p>
      <ResponsiveContainer width="100%" height={200}>
        <BarChart data={data} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0fdf4" />
          <XAxis dataKey="year" tick={{ fontSize: 11 }} />
          <YAxis tick={{ fontSize: 11 }} unit=" mm" />
          <Tooltip formatter={(v) => [`${v} mm`, 'Avg Rainfall']} />
          <Legend />
          <Bar
            dataKey="value"
            name="Monthly Rainfall"
            fill="#3b82f6"
            radius={[4, 4, 0, 0]}
          />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

// ── Main Component ─────────────────────────────────────────────────────────

export default function ClimateCropPredictor() {
  const [form, setForm] = useState(DEFAULT_FORM);
  const [errors, setErrors] = useState({});
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [apiError, setApiError] = useState('');

  // ── Form handlers ────────────────────────────────────────────────────────

  const handleChange = (field) => (e) => {
    const val = e.target ? e.target.value : e;
    setForm((prev) => ({ ...prev, [field]: val }));
    setErrors((prev) => ({ ...prev, [field]: '' }));
  };

  const handleSlider = (field) => (_, val) => {
    setForm((prev) => ({ ...prev, [field]: val }));
  };

  // ── Validation ────────────────────────────────────────────────────────────

  const validate = () => {
    const errs = {};
    const lat = parseFloat(form.latitude);
    const lon = parseFloat(form.longitude);

    if (form.latitude === '' || isNaN(lat) || lat < -90 || lat > 90) {
      errs.latitude = 'Latitude must be between -90 and 90.';
    }
    if (form.longitude === '' || isNaN(lon) || lon < -180 || lon > 180) {
      errs.longitude = 'Longitude must be between -180 and 180.';
    }
    return errs;
  };

  // ── Submit ────────────────────────────────────────────────────────────────

  const handleSubmit = async () => {
    const errs = validate();
    if (Object.keys(errs).length) {
      setErrors(errs);
      return;
    }

    setLoading(true);
    setApiError('');
    setResult(null);

    try {
      const payload = {
        latitude:    parseFloat(form.latitude),
        longitude:   parseFloat(form.longitude),
        soil_ph:     form.soil_ph,
        nitrogen:    form.nitrogen,
        phosphorus:  form.phosphorus,
        potassium:   form.potassium,
        target_year: form.target_year,
        top_n: 5,
      };

      const { data } = await axios.post('/api/climate/predict/future-crops', payload);
      setResult(data);
    } catch (err) {
      const msg =
        err?.response?.data?.detail ||
        'Unable to get recommendations. Please try again.';
      setApiError(msg);
    } finally {
      setLoading(false);
    }
  };

  // ── Render ────────────────────────────────────────────────────────────────

  return (
    <Box className="climate-predictor">
      {/* Hero banner */}
      <div className="climate-hero">
        <span className="climate-hero-icon">🌍</span>
        <div className="climate-hero-text">
          <h1>Climate-Resilient Crop Recommendation Engine</h1>
          <p>
            Enter your farm location and soil data to discover which crops will thrive
            under projected climate conditions over the next 5–10 years.
          </p>
        </div>
      </div>

      <Grid container spacing={2.5}>
        {/* ── Input form ──────────────────────────────────────────────── */}
        <Grid item xs={12} md={4}>
          <Card className="glass-card form-card" sx={{ height: '100%' }}>
            <CardContent sx={{ p: 0, '&:last-child': { pb: 0 } }}>
              <Typography variant="subtitle1" sx={{ fontWeight: 700, color: '#065f46', mb: 1.5 }}>
                🗺️ Farm Location
              </Typography>

              <Grid container spacing={1.5}>
                <Grid item xs={6}>
                  <TextField
                    label="Latitude"
                    size="small"
                    fullWidth
                    value={form.latitude}
                    onChange={handleChange('latitude')}
                    error={!!errors.latitude}
                    helperText={errors.latitude || 'e.g. 20.2961'}
                    type="number"
                    inputProps={{ step: 0.0001 }}
                  />
                </Grid>
                <Grid item xs={6}>
                  <TextField
                    label="Longitude"
                    size="small"
                    fullWidth
                    value={form.longitude}
                    onChange={handleChange('longitude')}
                    error={!!errors.longitude}
                    helperText={errors.longitude || 'e.g. 85.8245'}
                    type="number"
                    inputProps={{ step: 0.0001 }}
                  />
                </Grid>
              </Grid>

              <Typography variant="subtitle1" sx={{ fontWeight: 700, color: '#065f46', mt: 2, mb: 1 }}>
                🌱 Soil Parameters
              </Typography>

              {/* Soil pH */}
              <Typography variant="body2" sx={{ color: '#374151', mb: 0.5 }}>
                Soil pH: <strong>{form.soil_ph.toFixed(1)}</strong>
              </Typography>
              <Slider
                value={form.soil_ph}
                min={3.5}
                max={9.5}
                step={0.1}
                onChange={handleSlider('soil_ph')}
                sx={{ color: '#10b981' }}
              />

              {/* Nitrogen */}
              <Typography variant="body2" sx={{ color: '#374151', mb: 0.5 }}>
                Nitrogen: <strong>{form.nitrogen} kg/ha</strong>
              </Typography>
              <Slider
                value={form.nitrogen}
                min={0}
                max={300}
                step={5}
                onChange={handleSlider('nitrogen')}
                sx={{ color: '#10b981' }}
              />

              {/* Phosphorus */}
              <Typography variant="body2" sx={{ color: '#374151', mb: 0.5 }}>
                Phosphorus: <strong>{form.phosphorus} kg/ha</strong>
              </Typography>
              <Slider
                value={form.phosphorus}
                min={0}
                max={200}
                step={5}
                onChange={handleSlider('phosphorus')}
                sx={{ color: '#10b981' }}
              />

              {/* Potassium */}
              <Typography variant="body2" sx={{ color: '#374151', mb: 0.5 }}>
                Potassium: <strong>{form.potassium} kg/ha</strong>
              </Typography>
              <Slider
                value={form.potassium}
                min={0}
                max={300}
                step={5}
                onChange={handleSlider('potassium')}
                sx={{ color: '#10b981' }}
              />

              <Typography variant="subtitle1" sx={{ fontWeight: 700, color: '#065f46', mt: 2, mb: 1 }}>
                📅 Projection Horizon
              </Typography>
              <Typography variant="body2" sx={{ color: '#374151', mb: 0.5 }}>
                Target year: <strong>{form.target_year}</strong>
              </Typography>
              <Slider
                value={form.target_year}
                min={2025}
                max={2060}
                step={1}
                onChange={handleSlider('target_year')}
                sx={{ color: '#10b981' }}
              />

              {apiError && (
                <div className="error-alert" style={{ marginTop: 12 }}>
                  ⚠️ {apiError}
                </div>
              )}

              <Button
                variant="contained"
                fullWidth
                className="predict-btn"
                onClick={handleSubmit}
                disabled={loading}
                startIcon={loading ? <CircularProgress size={18} color="inherit" /> : <BarChartIcon />}
                sx={{ mt: 2 }}
              >
                {loading ? 'Predicting…' : 'Predict Future Crops'}
              </Button>
            </CardContent>
          </Card>
        </Grid>

        {/* ── Results ──────────────────────────────────────────────────── */}
        <Grid item xs={12} md={8}>
          {!loading && !result && (
            <div className="glass-card">
              <div className="empty-state">
                <span className="empty-state-icon">🌾</span>
                <Typography variant="h6" sx={{ color: '#374151', mb: 0.5 }}>
                  Ready to Predict
                </Typography>
                <p>
                  Fill in your farm location and soil parameters on the left, then
                  click "Predict Future Crops" to see AI-driven recommendations.
                </p>
              </div>
            </div>
          )}

          {loading && (
            <div className="glass-card">
              <div className="loading-overlay">
                <CircularProgress sx={{ color: '#10b981' }} size={48} />
                <p>Running climate ML pipeline…</p>
              </div>
            </div>
          )}

          {result && !loading && (
            <Grid container spacing={2}>
              {/* Climate summary */}
              <Grid item xs={12}>
                <ClimateSummary summary={result.future_climate_summary} />
              </Grid>

              {/* Explanation */}
              {result.explanation && (
                <Grid item xs={12}>
                  <div className="explanation-box">
                    <span className="icon">💡</span>
                    {result.explanation}
                  </div>
                </Grid>
              )}

              {/* Crop recommendation cards */}
              {result.recommended_crops && result.recommended_crops.length > 0 && (
                <Grid item xs={12}>
                  <Typography variant="subtitle1" sx={{ fontWeight: 700, color: '#065f46', mb: 1 }}>
                    🌾 Top Recommended Crops
                  </Typography>
                  <Grid container spacing={1.5}>
                    {result.recommended_crops.map((crop, i) => (
                      <Grid item xs={12} sm={6} key={crop.crop}>
                        <CropCard crop={crop} rank={i + 1} />
                      </Grid>
                    ))}
                  </Grid>
                </Grid>
              )}

              {/* Charts */}
              {result.climate_trends && (
                <>
                  <Grid item xs={12} sm={6}>
                    <TemperatureChart data={result.climate_trends.temperature_trend} />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <RainfallChart data={result.climate_trends.rainfall_trend} />
                  </Grid>
                </>
              )}

              {/* No crops edge case */}
              {result.recommended_crops && result.recommended_crops.length === 0 && (
                <Grid item xs={12}>
                  <Alert severity="warning">
                    No crops with sufficient suitability were found for these conditions.
                    Try adjusting your soil parameters or target year.
                  </Alert>
                </Grid>
              )}
            </Grid>
          )}
        </Grid>
      </Grid>
    </Box>
  );
}
