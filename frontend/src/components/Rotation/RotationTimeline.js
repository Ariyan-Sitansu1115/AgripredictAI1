import React from 'react';
import {
  Box, Grid, Card, CardContent, Typography, LinearProgress, Chip, Avatar,
} from '@mui/material';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import SpaIcon from '@mui/icons-material/Spa';
import AttachMoneyIcon from '@mui/icons-material/AttachMoney';
import BugReportIcon from '@mui/icons-material/BugReport';
import CalendarTodayIcon from '@mui/icons-material/CalendarToday';
import LandscapeIcon from '@mui/icons-material/Landscape';

const TIMELINE_COLORS = ['#10B981', '#F59E0B', '#8B5CF6', '#3B82F6', '#EF4444', '#EC4899', '#14B8A6'];

function TimelineItem({ yearData, color, isLast }) {
  return (
    <Box sx={{ display: 'flex', gap: 2 }}>
      {/* Connector */}
      <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
        <Avatar sx={{ bgcolor: color, width: 40, height: 40, fontSize: '1.2rem', flexShrink: 0 }}>
          {yearData.icon}
        </Avatar>
        {!isLast && (
          <Box sx={{ width: 2, flexGrow: 1, bgcolor: '#E5E7EB', mt: 0.5, minHeight: 24 }} />
        )}
      </Box>

      {/* Content */}
      <Box sx={{ pb: isLast ? 0 : 3, flex: 1 }}>
        <Card
          sx={{
            borderLeft: `3px solid ${color}`,
            transition: 'transform 0.2s',
            '&:hover': { transform: 'translateX(4px)' },
          }}
        >
          <CardContent sx={{ py: 1.5, '&:last-child': { pb: 1.5 } }}>
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
              <Box>
                <Typography variant="caption" color="text.secondary" fontWeight={600}>
                  YEAR {yearData.year}
                </Typography>
                <Typography variant="subtitle1" fontWeight={700}>{yearData.crop}</Typography>
              </Box>
              <Box sx={{ textAlign: 'right' }}>
                <Typography variant="caption" color="text.secondary">Profitability</Typography>
                <Typography variant="h6" fontWeight={700} sx={{ color }}>
                  {yearData.profitability}%
                </Typography>
              </Box>
            </Box>

            <LinearProgress
              variant="determinate"
              value={yearData.profitability}
              sx={{
                height: 5,
                borderRadius: 3,
                mb: 1,
                bgcolor: '#E5E7EB',
                '& .MuiLinearProgress-bar': { bgcolor: color, borderRadius: 3 },
              }}
            />

            <Box sx={{ display: 'flex', gap: 0.75, flexWrap: 'wrap', mb: 0.75 }}>
              <Chip
                icon={<TrendingUpIcon sx={{ fontSize: '14px !important' }} />}
                label={yearData.expectedYield}
                size="small"
                sx={{ fontSize: 11 }}
              />
              <Chip
                icon={<SpaIcon sx={{ fontSize: '14px !important' }} />}
                label={yearData.soilImpact}
                size="small"
                sx={{
                  fontSize: 11,
                  bgcolor: yearData.soilImpact?.startsWith('+') ? '#D1FAE5' : '#FEF3C7',
                  color: yearData.soilImpact?.startsWith('+') ? '#065F46' : '#92400E',
                }}
              />
            </Box>

            <Typography variant="caption" color="text.secondary">{yearData.notes}</Typography>
          </CardContent>
        </Card>
      </Box>
    </Box>
  );
}

const DEFAULT_YEARS = [
  { year: 1, crop: 'Wheat', icon: '🌾', profitability: 82, soilImpact: '+5% N', notes: 'Deep roots improve soil structure', expectedYield: '4.2 t/ha' },
  { year: 2, crop: 'Chickpea', icon: '🫘', profitability: 75, soilImpact: '+12% N', notes: 'Nitrogen-fixing legume', expectedYield: '1.8 t/ha' },
  { year: 3, crop: 'Maize', icon: '🌽', profitability: 88, soilImpact: '-8% N', notes: 'Benefits from legume nitrogen', expectedYield: '6.5 t/ha' },
  { year: 4, crop: 'Mustard', icon: '🌿', profitability: 70, soilImpact: '+3% OM', notes: 'Breaks pest cycles', expectedYield: '1.5 t/ha' },
  { year: 5, crop: 'Rice', icon: '🍚', profitability: 85, soilImpact: 'Neutral', notes: 'Flooding suppresses weeds naturally', expectedYield: '5.0 t/ha' },
];

export default function RotationTimeline({ plan }) {
  const years = plan?.years || DEFAULT_YEARS;

  const avgProfitability = Math.round(years.reduce((s, y) => s + y.profitability, 0) / years.length);

  return (
    <Box>
      {/* Summary strip */}
      <Grid container spacing={2} sx={{ mb: 3 }}>
        {[
          { label: 'Total Years', value: years.length, icon: <CalendarTodayIcon />, color: '#10B981' },
          { label: 'Avg Profitability', value: `${avgProfitability}%`, icon: <AttachMoneyIcon />, color: '#F59E0B' },
          { label: 'Crops in Cycle', value: years.length, icon: <LandscapeIcon />, color: '#8B5CF6' },
          { label: 'Pest Reduction', value: '42%', icon: <BugReportIcon />, color: '#3B82F6' },
        ].map((s) => (
          <Grid item xs={6} sm={3} key={s.label}>
            <Card>
              <CardContent sx={{ py: 1.5, '&:last-child': { pb: 1.5 } }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <Avatar sx={{ bgcolor: `${s.color}20`, width: 36, height: 36 }}>
                    {React.cloneElement(s.icon, { sx: { color: s.color, fontSize: 18 } })}
                  </Avatar>
                  <Box>
                    <Typography variant="h6" fontWeight={700} sx={{ color: s.color }}>
                      {s.value}
                    </Typography>
                    <Typography variant="caption" color="text.secondary">{s.label}</Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Timeline */}
      <Card>
        <CardContent>
          <Typography variant="h6" fontWeight={600} mb={2}>
            Rotation Timeline
          </Typography>
          <Box>
            {years.map((yr, i) => (
              <TimelineItem
                key={yr.year}
                yearData={yr}
                color={TIMELINE_COLORS[i % TIMELINE_COLORS.length]}
                isLast={i === years.length - 1}
              />
            ))}
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
}
