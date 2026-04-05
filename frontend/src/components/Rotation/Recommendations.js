import React, { useState } from 'react';
import {
  Box, Grid, Card, CardContent, Typography, Chip, Button,
  LinearProgress, Select, MenuItem, FormControl, InputLabel,
  TextField, InputAdornment,
} from '@mui/material';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import SpaIcon from '@mui/icons-material/Spa';
import BugReportIcon from '@mui/icons-material/BugReport';
import AttachMoneyIcon from '@mui/icons-material/AttachMoney';
import SearchIcon from '@mui/icons-material/Search';

const RECOMMENDATIONS = [
  {
    id: 1,
    crop: 'Chickpea',
    icon: '🫘',
    type: 'Legume',
    matchScore: 94,
    yieldImprovement: '+22%',
    profitabilityScore: 85,
    soilImpact: 'Excellent',
    soilImpactColor: '#10B981',
    pestCycle: 'Breaks cereal pest cycles',
    reason: 'High nitrogen fixation restores depleted nitrogen. Ideal after cereal crops.',
    season: 'Rabi',
    waterReq: 'Low',
  },
  {
    id: 2,
    crop: 'Maize',
    icon: '🌽',
    type: 'Cereal',
    matchScore: 88,
    yieldImprovement: '+18%',
    profitabilityScore: 90,
    soilImpact: 'Good',
    soilImpactColor: '#F59E0B',
    pestCycle: 'Different pest class from wheat',
    reason: 'Excellent market demand. Benefits from residual nitrogen from legume predecessor.',
    season: 'Kharif',
    waterReq: 'Medium',
  },
  {
    id: 3,
    crop: 'Mustard',
    icon: '🌿',
    type: 'Oilseed',
    matchScore: 82,
    yieldImprovement: '+12%',
    profitabilityScore: 72,
    soilImpact: 'Good',
    soilImpactColor: '#F59E0B',
    pestCycle: 'Biofumigation effect on soil pests',
    reason: 'Good oilseed market. Biofumigation properties suppress soil-borne pathogens.',
    season: 'Rabi',
    waterReq: 'Low',
  },
  {
    id: 4,
    crop: 'Sorghum',
    icon: '🌾',
    type: 'Cereal',
    matchScore: 78,
    yieldImprovement: '+10%',
    profitabilityScore: 68,
    soilImpact: 'Moderate',
    soilImpactColor: '#8B5CF6',
    pestCycle: 'No overlap with rice/wheat pests',
    reason: 'Drought-tolerant. Good for areas with erratic rainfall. Low input cost.',
    season: 'Kharif',
    waterReq: 'Very Low',
  },
  {
    id: 5,
    crop: 'Sunflower',
    icon: '🌻',
    type: 'Oilseed',
    matchScore: 74,
    yieldImprovement: '+8%',
    profitabilityScore: 76,
    soilImpact: 'Good',
    soilImpactColor: '#F59E0B',
    pestCycle: 'Different pest profile from cereals',
    reason: 'Good MSP support. Deep taproot breaks soil hardpan and improves drainage.',
    season: 'Kharif / Rabi',
    waterReq: 'Medium',
  },
  {
    id: 6,
    crop: 'Lentil',
    icon: '🟤',
    type: 'Legume',
    matchScore: 70,
    yieldImprovement: '+15%',
    profitabilityScore: 65,
    soilImpact: 'Excellent',
    soilImpactColor: '#10B981',
    pestCycle: 'Effective rotation break for wheat diseases',
    reason: 'Strong nitrogen fixation. Short duration allows double cropping.',
    season: 'Rabi',
    waterReq: 'Low',
  },
];

const CROP_TYPES = ['All', 'Cereal', 'Legume', 'Oilseed'];
const SORT_OPTIONS = [
  { value: 'matchScore', label: 'Best Match' },
  { value: 'profitabilityScore', label: 'Profitability' },
  { value: 'yieldImprovement', label: 'Yield Improvement' },
];

function RecommendationCard({ rec }) {
  return (
    <Card
      sx={{
        transition: 'transform 0.2s ease, box-shadow 0.2s ease',
        '&:hover': {
          transform: 'translateY(-3px)',
          boxShadow: '0 12px 32px rgba(0,0,0,0.12)',
        },
      }}
    >
      <CardContent>
        {/* Header */}
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, mb: 2 }}>
          <Typography variant="h2" sx={{ lineHeight: 1 }}>{rec.icon}</Typography>
          <Box sx={{ flex: 1 }}>
            <Typography variant="h6" fontWeight={700}>{rec.crop}</Typography>
            <Box sx={{ display: 'flex', gap: 0.5, flexWrap: 'wrap' }}>
              <Chip label={rec.type} size="small" sx={{ bgcolor: '#EDE9FE', color: '#5B21B6' }} />
              <Chip label={rec.season} size="small" sx={{ bgcolor: '#FEF3C7', color: '#92400E' }} />
              <Chip label={`💧 ${rec.waterReq}`} size="small" sx={{ bgcolor: '#DBEAFE', color: '#1D4ED8' }} />
            </Box>
          </Box>
          <Box sx={{ textAlign: 'center' }}>
            <Typography variant="h5" fontWeight={700} sx={{ color: '#10B981' }}>
              {rec.matchScore}%
            </Typography>
            <Typography variant="caption" color="text.secondary">Match</Typography>
          </Box>
        </Box>

        {/* Match Score Bar */}
        <LinearProgress
          variant="determinate"
          value={rec.matchScore}
          sx={{
            height: 6,
            borderRadius: 3,
            mb: 2,
            bgcolor: '#E5E7EB',
            '& .MuiLinearProgress-bar': {
              bgcolor: rec.matchScore >= 85 ? '#10B981' : rec.matchScore >= 70 ? '#F59E0B' : '#8B5CF6',
              borderRadius: 3,
            },
          }}
        />

        {/* Stats Row */}
        <Grid container spacing={1} sx={{ mb: 2 }}>
          <Grid item xs={4}>
            <Box sx={{ textAlign: 'center', p: 1, bgcolor: '#F0FDF4', borderRadius: 1 }}>
              <TrendingUpIcon sx={{ fontSize: 18, color: '#10B981' }} />
              <Typography variant="caption" display="block" color="text.secondary">Yield</Typography>
              <Typography variant="body2" fontWeight={600} sx={{ color: '#10B981' }}>{rec.yieldImprovement}</Typography>
            </Box>
          </Grid>
          <Grid item xs={4}>
            <Box sx={{ textAlign: 'center', p: 1, bgcolor: '#FFFBEB', borderRadius: 1 }}>
              <AttachMoneyIcon sx={{ fontSize: 18, color: '#F59E0B' }} />
              <Typography variant="caption" display="block" color="text.secondary">Profit</Typography>
              <Typography variant="body2" fontWeight={600} sx={{ color: '#F59E0B' }}>{rec.profitabilityScore}%</Typography>
            </Box>
          </Grid>
          <Grid item xs={4}>
            <Box sx={{ textAlign: 'center', p: 1, bgcolor: '#F0FDF4', borderRadius: 1 }}>
              <SpaIcon sx={{ fontSize: 18, color: rec.soilImpactColor }} />
              <Typography variant="caption" display="block" color="text.secondary">Soil</Typography>
              <Typography variant="body2" fontWeight={600} sx={{ color: rec.soilImpactColor }}>{rec.soilImpact}</Typography>
            </Box>
          </Grid>
        </Grid>

        {/* Pest note */}
        <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 1, mb: 1.5 }}>
          <BugReportIcon sx={{ fontSize: 16, color: '#6B7280', mt: 0.2 }} />
          <Typography variant="caption" color="text.secondary">{rec.pestCycle}</Typography>
        </Box>

        {/* Reason */}
        <Typography variant="body2" color="text.secondary" sx={{ fontSize: 12, fontStyle: 'italic' }}>
          {rec.reason}
        </Typography>
      </CardContent>
    </Card>
  );
}

export default function Recommendations() {
  const [cropFilter, setCropFilter] = useState('All');
  const [sortBy, setSortBy] = useState('matchScore');
  const [search, setSearch] = useState('');

  const filtered = RECOMMENDATIONS
    .filter((r) => cropFilter === 'All' || r.type === cropFilter)
    .filter((r) => r.crop.toLowerCase().includes(search.toLowerCase()))
    .sort((a, b) => {
      if (sortBy === 'yieldImprovement') {
        return parseInt(b.yieldImprovement) - parseInt(a.yieldImprovement);
      }
      return b[sortBy] - a[sortBy];
    });

  return (
    <Box>
      {/* Filter row */}
      <Box sx={{ display: 'flex', gap: 2, mb: 3, flexWrap: 'wrap', alignItems: 'center' }}>
        <TextField
          size="small"
          placeholder="Search crops…"
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start"><SearchIcon fontSize="small" /></InputAdornment>
            ),
          }}
          sx={{ minWidth: 180 }}
        />
        <FormControl size="small" sx={{ minWidth: 140 }}>
          <InputLabel>Crop Type</InputLabel>
          <Select value={cropFilter} label="Crop Type" onChange={(e) => setCropFilter(e.target.value)}>
            {CROP_TYPES.map((t) => <MenuItem key={t} value={t}>{t}</MenuItem>)}
          </Select>
        </FormControl>
        <FormControl size="small" sx={{ minWidth: 160 }}>
          <InputLabel>Sort By</InputLabel>
          <Select value={sortBy} label="Sort By" onChange={(e) => setSortBy(e.target.value)}>
            {SORT_OPTIONS.map((o) => <MenuItem key={o.value} value={o.value}>{o.label}</MenuItem>)}
          </Select>
        </FormControl>
        <Typography variant="body2" color="text.secondary" sx={{ ml: 'auto' }}>
          {filtered.length} recommendation{filtered.length !== 1 ? 's' : ''} found
        </Typography>
      </Box>

      <Grid container spacing={2}>
        {filtered.map((rec) => (
          <Grid item xs={12} sm={6} lg={4} key={rec.id}>
            <RecommendationCard rec={rec} />
          </Grid>
        ))}
        {filtered.length === 0 && (
          <Grid item xs={12}>
            <Card>
              <CardContent sx={{ textAlign: 'center', py: 6 }}>
                <Typography variant="h4" mb={1}>🔍</Typography>
                <Typography variant="h6" color="text.secondary">No crops match your filters</Typography>
                <Button variant="text" onClick={() => { setCropFilter('All'); setSearch(''); }} sx={{ mt: 1 }}>
                  Clear Filters
                </Button>
              </CardContent>
            </Card>
          </Grid>
        )}
      </Grid>
    </Box>
  );
}
