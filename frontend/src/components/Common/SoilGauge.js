import React from 'react';
import { Box, Typography, Chip, CircularProgress } from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import WarningAmberIcon from '@mui/icons-material/WarningAmber';
import ErrorIcon from '@mui/icons-material/Error';
import { soilHealthLabel, soilHealthColor } from '../../utils/formatters';

/**
 * SoilGauge
 * Circular progress gauge showing a soil health score (0–100)
 * with colour-coded label and status chip.
 *
 * Props:
 *   score  {number}  – 0–100
 *   size   {number}  – diameter in px (default 120)
 *   label  {string}  – optional override for label text
 */
export default function SoilGauge({ score = 0, size = 120, label }) {
  const color     = soilHealthColor(score);
  const scoreLabel = label || soilHealthLabel(score);

  const StatusIcon =
    score >= 75 ? CheckCircleIcon
    : score >= 50 ? WarningAmberIcon
    : ErrorIcon;

  const thickness = Math.round(size / 15);

  return (
    <Box sx={{ position: 'relative', display: 'inline-flex', flexDirection: 'column', alignItems: 'center' }}>
      {/* Track + fill */}
      <Box sx={{ position: 'relative', display: 'inline-flex' }}>
        {/* Track (background circle) */}
        <CircularProgress
          variant="determinate"
          value={100}
          size={size}
          thickness={thickness}
          sx={{ color: '#E5E7EB', position: 'absolute' }}
        />
        {/* Fill */}
        <CircularProgress
          variant="determinate"
          value={score}
          size={size}
          thickness={thickness}
          sx={{ color }}
        />

        {/* Centre text */}
        <Box
          sx={{
            inset: 0,
            position: 'absolute',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <Typography
            variant={size >= 100 ? 'h4' : 'h6'}
            fontWeight={700}
            sx={{ color, lineHeight: 1 }}
          >
            {score}
          </Typography>
          <Typography variant="caption" color="text.secondary">/ 100</Typography>
        </Box>
      </Box>

      {/* Status chip */}
      <Chip
        label={scoreLabel}
        size="small"
        sx={{ mt: 1, bgcolor: `${color}20`, color, fontWeight: 600, fontSize: '0.72rem' }}
        icon={<StatusIcon sx={{ fontSize: '14px !important', color: `${color} !important` }} />}
      />
    </Box>
  );
}
