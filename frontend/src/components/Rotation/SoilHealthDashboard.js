import React, { useState, useEffect } from 'react';
import {
  Box, Grid, Card, CardContent, Typography, Chip, LinearProgress,
  Avatar, Alert, CircularProgress, Divider,
} from '@mui/material';
import SpaIcon from '@mui/icons-material/Spa';
import ScienceIcon from '@mui/icons-material/Science';
import WarningAmberIcon from '@mui/icons-material/WarningAmber';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';
import WaterDropIcon from '@mui/icons-material/WaterDrop';
import LocalFireDepartmentIcon from '@mui/icons-material/LocalFireDepartment';
import BubbleChartIcon from '@mui/icons-material/BubbleChart';
import {
  XAxis, YAxis, CartesianGrid, Tooltip, Legend,
  ResponsiveContainer, AreaChart, Area,
} from 'recharts';

// ── Mock data ────────────────────────────────────────────────────────────────
const MOCK_SOIL_METRICS = {
  nitrogen: 45,
  phosphorus: 22,
  potassium: 148,
  organicMatter: 3.4,
  ph: 6.7,
  moisture: 62,
  healthScore: 74,
};

const MOCK_TREND_DATA = [
  { month: 'Aug', nitrogen: 40, phosphorus: 18, potassium: 135, organicMatter: 3.1 },
  { month: 'Sep', nitrogen: 42, phosphorus: 20, potassium: 140, organicMatter: 3.2 },
  { month: 'Oct', nitrogen: 44, phosphorus: 21, potassium: 143, organicMatter: 3.3 },
  { month: 'Nov', nitrogen: 45, phosphorus: 22, potassium: 148, organicMatter: 3.4 },
  { month: 'Dec', nitrogen: 43, phosphorus: 22, potassium: 150, organicMatter: 3.5 },
  { month: 'Jan', nitrogen: 46, phosphorus: 23, potassium: 152, organicMatter: 3.6 },
];

const MOCK_ALERTS = [
  { id: 1, severity: 'warning', message: 'Phosphorus levels slightly below optimal (22 vs 25 ppm recommended)' },
  { id: 2, severity: 'info', message: 'Nitrogen levels stable. Consider legume rotation to maintain.' },
];

// ── Helper: health score → color ────────────────────────────────────────────
function getScoreColor(score) {
  if (score >= 75) return '#10B981';
  if (score >= 50) return '#F59E0B';
  return '#EF4444';
}

function getScoreLabel(score) {
  if (score >= 75) return 'Excellent';
  if (score >= 50) return 'Moderate';
  return 'Poor';
}

// ── Circular gauge ────────────────────────────────────────────────────────────
function HealthGauge({ score }) {
  const color = getScoreColor(score);
  const label = getScoreLabel(score);
  return (
    <Box sx={{ position: 'relative', display: 'inline-flex', flexDirection: 'column', alignItems: 'center' }}>
      <Box sx={{ position: 'relative', display: 'inline-flex' }}>
        <CircularProgress
          variant="determinate"
          value={100}
          size={120}
          sx={{ color: '#E5E7EB', position: 'absolute' }}
        />
        <CircularProgress
          variant="determinate"
          value={score}
          size={120}
          sx={{ color }}
        />
        <Box
          sx={{
            top: 0, left: 0, bottom: 0, right: 0,
            position: 'absolute',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            flexDirection: 'column',
          }}
        >
          <Typography variant="h4" fontWeight={700} sx={{ color }}>
            {score}
          </Typography>
          <Typography variant="caption" color="text.secondary">/ 100</Typography>
        </Box>
      </Box>
      <Chip
        label={label}
        size="small"
        sx={{
          mt: 1,
          bgcolor: `${color}20`,
          color,
          fontWeight: 600,
          fontSize: '0.75rem',
        }}
        icon={
          score >= 75
            ? <CheckCircleIcon sx={{ fontSize: 14, color: `${color} !important` }} />
            : score >= 50
            ? <WarningAmberIcon sx={{ fontSize: 14, color: `${color} !important` }} />
            : <ErrorIcon sx={{ fontSize: 14, color: `${color} !important` }} />
        }
      />
    </Box>
  );
}

// ── Nutrient bar card ─────────────────────────────────────────────────────────
function NutrientCard({ label, value, unit, max, color, icon, optimal }) {
  const pct = Math.min((value / max) * 100, 100);
  const isLow = value < optimal * 0.8;
  const isHigh = value > optimal * 1.2;
  const status = isLow ? 'Low' : isHigh ? 'High' : 'Optimal';
  const statusColor = isLow ? 'error' : isHigh ? 'warning' : 'success';

  return (
    <Card>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1.5, gap: 1 }}>
          <Avatar sx={{ bgcolor: `${color}20`, width: 36, height: 36 }}>
            {React.cloneElement(icon, { sx: { color, fontSize: 20 } })}
          </Avatar>
          <Box sx={{ flex: 1 }}>
            <Typography variant="body2" fontWeight={600}>{label}</Typography>
            <Typography variant="caption" color="text.secondary">
              {value} {unit}
            </Typography>
          </Box>
          <Chip label={status} color={statusColor} size="small" variant="outlined" />
        </Box>
        <LinearProgress
          variant="determinate"
          value={pct}
          sx={{
            height: 8,
            borderRadius: 4,
            bgcolor: '#E5E7EB',
            '& .MuiLinearProgress-bar': { bgcolor: color, borderRadius: 4 },
          }}
        />
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 0.5 }}>
          <Typography variant="caption" color="text.secondary">0</Typography>
          <Typography variant="caption" color="text.secondary">Optimal: {optimal} {unit}</Typography>
          <Typography variant="caption" color="text.secondary">{max}</Typography>
        </Box>
      </CardContent>
    </Card>
  );
}

// ── Main component ────────────────────────────────────────────────────────────
export default function SoilHealthDashboard({ soilData }) {
  const [metrics, setMetrics] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Use provided data or fall back to mock data
    const timer = setTimeout(() => {
      setMetrics(soilData || MOCK_SOIL_METRICS);
      setLoading(false);
    }, 600);
    return () => clearTimeout(timer);
  }, [soilData]);

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', py: 6 }}>
        <CircularProgress />
      </Box>
    );
  }

  const NUTRIENTS = [
    {
      label: 'Nitrogen (N)',
      value: metrics.nitrogen,
      unit: 'ppm',
      max: 100,
      optimal: 50,
      color: '#10B981',
      icon: <SpaIcon />,
    },
    {
      label: 'Phosphorus (P)',
      value: metrics.phosphorus,
      unit: 'ppm',
      max: 60,
      optimal: 25,
      color: '#F59E0B',
      icon: <LocalFireDepartmentIcon />,
    },
    {
      label: 'Potassium (K)',
      value: metrics.potassium,
      unit: 'ppm',
      max: 300,
      optimal: 150,
      color: '#8B5CF6',
      icon: <BubbleChartIcon />,
    },
    {
      label: 'Organic Matter',
      value: metrics.organicMatter,
      unit: '%',
      max: 8,
      optimal: 4,
      color: '#92400E',
      icon: <ScienceIcon />,
    },
    {
      label: 'Soil Moisture',
      value: metrics.moisture,
      unit: '%',
      max: 100,
      optimal: 65,
      color: '#3B82F6',
      icon: <WaterDropIcon />,
    },
  ];

  return (
    <Box>
      {/* Alerts */}
      {MOCK_ALERTS.map((alert) => (
        <Alert key={alert.id} severity={alert.severity} sx={{ mb: 1.5, borderRadius: 2 }}>
          {alert.message}
        </Alert>
      ))}

      <Grid container spacing={3}>
        {/* Health Score Gauge */}
        <Grid item xs={12} md={3}>
          <Card sx={{ height: '100%' }}>
            <CardContent sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', py: 4 }}>
              <Typography variant="h6" fontWeight={600} mb={3} textAlign="center">
                Soil Health Score
              </Typography>
              <HealthGauge score={metrics.healthScore} />
              <Divider sx={{ my: 2, width: '100%' }} />
              <Typography variant="body2" color="text.secondary" textAlign="center">
                Based on N, P, K, organic matter, pH, and moisture levels
              </Typography>
              <Box sx={{ mt: 2, width: '100%' }}>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                  <Typography variant="caption" color="text.secondary">pH Level</Typography>
                  <Typography variant="caption" fontWeight={600}>{metrics.ph}</Typography>
                </Box>
                <LinearProgress
                  variant="determinate"
                  value={(metrics.ph / 14) * 100}
                  sx={{
                    height: 6,
                    borderRadius: 3,
                    bgcolor: '#E5E7EB',
                    '& .MuiLinearProgress-bar': { bgcolor: '#10B981', borderRadius: 3 },
                  }}
                />
                <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
                  <Typography variant="caption" color="text.secondary">0 (Acidic)</Typography>
                  <Typography variant="caption" color="text.secondary">14 (Alkaline)</Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        {/* Nutrient Cards */}
        <Grid item xs={12} md={9}>
          <Grid container spacing={2}>
            {NUTRIENTS.map((n) => (
              <Grid item xs={12} sm={6} lg={4} key={n.label}>
                <NutrientCard {...n} />
              </Grid>
            ))}
          </Grid>
        </Grid>

        {/* Trend Chart */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" fontWeight={600} mb={2}>
                Soil Nutrient Trends (6 Months)
              </Typography>
              <ResponsiveContainer width="100%" height={280}>
                <AreaChart data={MOCK_TREND_DATA} margin={{ top: 10, right: 20, left: -10, bottom: 0 }}>
                  <defs>
                    <linearGradient id="nitrogen" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#10B981" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#10B981" stopOpacity={0} />
                    </linearGradient>
                    <linearGradient id="phosphorus" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#F59E0B" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#F59E0B" stopOpacity={0} />
                    </linearGradient>
                    <linearGradient id="potassium" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#8B5CF6" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#8B5CF6" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#F3F4F6" />
                  <XAxis dataKey="month" tick={{ fontSize: 12 }} />
                  <YAxis tick={{ fontSize: 12 }} />
                  <Tooltip
                    contentStyle={{ borderRadius: 8, border: '1px solid #E5E7EB', fontSize: 12 }}
                  />
                  <Legend />
                  <Area type="monotone" dataKey="nitrogen" stroke="#10B981" fill="url(#nitrogen)" name="Nitrogen (ppm)" strokeWidth={2} />
                  <Area type="monotone" dataKey="phosphorus" stroke="#F59E0B" fill="url(#phosphorus)" name="Phosphorus (ppm)" strokeWidth={2} />
                  <Area type="monotone" dataKey="potassium" stroke="#8B5CF6" fill="url(#potassium)" name="Potassium (ppm)" strokeWidth={2} />
                </AreaChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}
