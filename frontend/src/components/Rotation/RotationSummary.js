import React from 'react';
import {
  Box, Grid, Card, CardContent, Typography, Chip, Avatar, LinearProgress, Divider,
} from '@mui/material';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import SpaIcon from '@mui/icons-material/Spa';
import AttachMoneyIcon from '@mui/icons-material/AttachMoney';
import BugReportIcon from '@mui/icons-material/BugReport';
import NatureIcon from '@mui/icons-material/Nature';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';

const DEFAULT_SUMMARY = {
  currentSeason: 'Rabi 2024-25',
  nextRecommendedCrop: { name: 'Chickpea', icon: '🫘', matchScore: 94 },
  soilHealthScore: 74,
  profitabilityTrend: '+12%',
  sustainabilityScore: 82,
  pestRiskReduction: '42%',
  highlights: [
    'Nitrogen levels improving with legume rotation',
    'Pest pressure reduced by 42% from last cycle',
    'Soil organic matter trending upward (+0.5% YoY)',
    'Water usage optimized with drought-tolerant crop selection',
  ],
};

export default function RotationSummary({ plan, soilData }) {
  const summary = plan?.summary
    ? {
        ...DEFAULT_SUMMARY,
        soilHealthScore: soilData?.healthScore || DEFAULT_SUMMARY.soilHealthScore,
        profitabilityTrend: `+${plan.summary.avgProfitability || 80}%`,
        pestRiskReduction: plan.summary.pestReduction || DEFAULT_SUMMARY.pestRiskReduction,
        sustainabilityScore: Math.round((plan.summary.avgProfitability || 80) * 1.05),
      }
    : DEFAULT_SUMMARY;

  const stats = [
    {
      label: 'Soil Health',
      value: `${summary.soilHealthScore}/100`,
      pct: summary.soilHealthScore,
      color: '#10B981',
      icon: <SpaIcon />,
    },
    {
      label: 'Profitability',
      value: summary.profitabilityTrend,
      pct: 80,
      color: '#F59E0B',
      icon: <AttachMoneyIcon />,
    },
    {
      label: 'Sustainability',
      value: `${summary.sustainabilityScore}/100`,
      pct: summary.sustainabilityScore,
      color: '#8B5CF6',
      icon: <NatureIcon />,
    },
    {
      label: 'Pest Reduction',
      value: summary.pestRiskReduction,
      pct: parseInt(summary.pestRiskReduction),
      color: '#3B82F6',
      icon: <BugReportIcon />,
    },
  ];

  return (
    <Card sx={{ background: 'linear-gradient(135deg, rgba(16,185,129,0.05), rgba(139,92,246,0.05))' }}>
      <CardContent sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 3, flexWrap: 'wrap', gap: 1 }}>
          <Box>
            <Typography variant="h5" fontWeight={700}>Rotation Overview</Typography>
            <Typography variant="body2" color="text.secondary">
              Season: {summary.currentSeason}
            </Typography>
          </Box>
          <Chip
            icon={<TrendingUpIcon />}
            label={`Next: ${summary.nextRecommendedCrop.name} ${summary.nextRecommendedCrop.icon}`}
            sx={{ bgcolor: '#D1FAE5', color: '#065F46', fontWeight: 600 }}
          />
        </Box>

        <Grid container spacing={2} sx={{ mb: 3 }}>
          {stats.map((s) => (
            <Grid item xs={6} sm={3} key={s.label}>
              <Box sx={{ p: 1.5, bgcolor: 'white', borderRadius: 2, boxShadow: '0 1px 4px rgba(0,0,0,0.08)' }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                  <Avatar sx={{ bgcolor: `${s.color}15`, width: 32, height: 32 }}>
                    {React.cloneElement(s.icon, { sx: { color: s.color, fontSize: 16 } })}
                  </Avatar>
                  <Typography variant="body2" color="text.secondary" sx={{ fontSize: 11 }}>{s.label}</Typography>
                </Box>
                <Typography variant="h6" fontWeight={700} sx={{ color: s.color, mb: 0.5 }}>
                  {s.value}
                </Typography>
                <LinearProgress
                  variant="determinate"
                  value={s.pct || 0}
                  sx={{
                    height: 4,
                    borderRadius: 2,
                    bgcolor: '#E5E7EB',
                    '& .MuiLinearProgress-bar': { bgcolor: s.color, borderRadius: 2 },
                  }}
                />
              </Box>
            </Grid>
          ))}
        </Grid>

        <Divider sx={{ mb: 2 }} />

        <Typography variant="subtitle2" fontWeight={600} mb={1.5}>
          Key Highlights
        </Typography>
        <Box sx={{ display: 'flex', flexDirection: 'column', gap: 0.75 }}>
          {summary.highlights.map((h, i) => (
            <Box key={i} sx={{ display: 'flex', alignItems: 'flex-start', gap: 1 }}>
              <CheckCircleIcon sx={{ fontSize: 16, color: '#10B981', mt: 0.2, flexShrink: 0 }} />
              <Typography variant="body2" color="text.secondary" sx={{ fontSize: 13 }}>{h}</Typography>
            </Box>
          ))}
        </Box>
      </CardContent>
    </Card>
  );
}
