import React from 'react';
import { Box, Card, CardContent, Typography, Chip, LinearProgress, Avatar } from '@mui/material';
import SpaIcon from '@mui/icons-material/Spa';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import WarningAmberIcon from '@mui/icons-material/WarningAmber';
import ErrorIcon from '@mui/icons-material/Error';
import { soilHealthLabel, soilHealthColor } from '../../utils/formatters';

/**
 * SoilHealthCard
 * Glassmorphic card that summarises a single soil metric with a labelled
 * progress bar and an optional status chip.
 *
 * Props:
 *   label     {string}  – e.g. "Nitrogen (N)"
 *   value     {number}  – current reading
 *   unit      {string}  – e.g. "ppm"
 *   max       {number}  – scale maximum
 *   optimal   {number}  – target value for status evaluation
 *   color     {string}  – bar colour hex
 *   icon      {node}    – optional MUI icon element
 *   compact   {boolean} – condensed single-line layout
 */
export default function SoilHealthCard({
  label,
  value,
  unit = '',
  max = 100,
  optimal,
  color = '#10B981',
  icon,
  compact = false,
}) {
  const pct = Math.min((value / max) * 100, 100);
  const isLow  = optimal && value < optimal * 0.8;
  const isHigh = optimal && value > optimal * 1.2;
  const status      = isLow ? 'Low' : isHigh ? 'High' : 'Optimal';
  const statusColor = isLow ? 'error' : isHigh ? 'warning' : 'success';

  const StatusIcon = isLow ? ErrorIcon : isHigh ? WarningAmberIcon : CheckCircleIcon;

  if (compact) {
    return (
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, py: 1 }}>
        <Avatar sx={{ bgcolor: `${color}20`, width: 32, height: 32, flexShrink: 0 }}>
          {icon ? React.cloneElement(icon, { sx: { color, fontSize: 16 } }) : <SpaIcon sx={{ color, fontSize: 16 }} />}
        </Avatar>
        <Box sx={{ flex: 1, minWidth: 0 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
            <Typography variant="caption" fontWeight={600} noWrap>{label}</Typography>
            <Typography variant="caption" color="text.secondary">
              {value} {unit}
            </Typography>
          </Box>
          <LinearProgress
            variant="determinate"
            value={pct}
            sx={{
              height: 5,
              borderRadius: 3,
              bgcolor: '#E5E7EB',
              '& .MuiLinearProgress-bar': { bgcolor: color, borderRadius: 3 },
            }}
          />
        </Box>
        <Chip label={status} color={statusColor} size="small" variant="outlined" sx={{ flexShrink: 0 }} />
      </Box>
    );
  }

  return (
    <Card
      sx={{
        background: 'rgba(255,255,255,0.92)',
        backdropFilter: 'blur(12px)',
        border: '1px solid rgba(255,255,255,0.5)',
        borderRadius: 3,
        transition: 'transform 0.2s ease, box-shadow 0.2s ease',
        '&:hover': { transform: 'translateY(-3px)', boxShadow: '0 10px 32px rgba(0,0,0,0.13)' },
      }}
    >
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1.5, gap: 1 }}>
          <Avatar sx={{ bgcolor: `${color}20`, width: 36, height: 36 }}>
            {icon
              ? React.cloneElement(icon, { sx: { color, fontSize: 20 } })
              : <SpaIcon sx={{ color, fontSize: 20 }} />
            }
          </Avatar>
          <Box sx={{ flex: 1 }}>
            <Typography variant="body2" fontWeight={600}>{label}</Typography>
            <Typography variant="caption" color="text.secondary">
              {value} {unit}
            </Typography>
          </Box>
          <Chip
            icon={<StatusIcon sx={{ fontSize: '14px !important' }} />}
            label={status}
            color={statusColor}
            size="small"
            variant="outlined"
          />
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

        {optimal && (
          <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: 0.5 }}>
            <Typography variant="caption" color="text.secondary">0</Typography>
            <Typography variant="caption" color="text.secondary">
              Optimal: {optimal} {unit}
            </Typography>
            <Typography variant="caption" color="text.secondary">{max}</Typography>
          </Box>
        )}
      </CardContent>
    </Card>
  );
}

SoilHealthCard.defaultProps = {
  unit:    '',
  max:     100,
  optimal: undefined,
  color:   '#10B981',
  icon:    undefined,
  compact: false,
};
