import React from 'react';
import { Box, Typography, CircularProgress } from '@mui/material';

/**
 * MetricGauge
 * A compact circular gauge for any 0–100 metric (e.g. profitability, match score).
 *
 * Props:
 *   value    {number}  – 0–100
 *   label    {string}  – label below the circle
 *   color    {string}  – fill colour
 *   size     {number}  – diameter (default 80)
 *   suffix   {string}  – suffix after value (default "%")
 */
export default function MetricGauge({
  value = 0,
  label = '',
  color = '#10B981',
  size = 80,
  suffix = '%',
}) {
  const thickness = Math.round(size / 12);
  const fontSize  = size >= 80 ? '1.1rem' : '0.85rem';

  return (
    <Box sx={{ display: 'inline-flex', flexDirection: 'column', alignItems: 'center', gap: 0.5 }}>
      <Box sx={{ position: 'relative', display: 'inline-flex' }}>
        {/* Track */}
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
          value={Math.min(value, 100)}
          size={size}
          thickness={thickness}
          sx={{ color }}
        />
        {/* Centre */}
        <Box
          sx={{
            inset: 0,
            position: 'absolute',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <Typography sx={{ fontSize, fontWeight: 700, color, lineHeight: 1 }}>
            {value}{suffix}
          </Typography>
        </Box>
      </Box>
      {label && (
        <Typography variant="caption" color="text.secondary" align="center">
          {label}
        </Typography>
      )}
    </Box>
  );
}
