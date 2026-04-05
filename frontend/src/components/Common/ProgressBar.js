import React from 'react';
import { Box, Typography } from '@mui/material';

/**
 * ProgressBar
 * Animated progress bar with optional label, value display and colour.
 *
 * Props:
 *   value        {number}  – 0–100
 *   color        {string}  – fill colour (default "#10B981")
 *   height       {number}  – bar height in px (default 8)
 *   showValue    {boolean} – show value text on right (default false)
 *   label        {string}  – optional label on left
 *   borderRadius {number}  – corner radius (default 4)
 *   animate      {boolean} – CSS transition animation (default true)
 */
export default function ProgressBar({
  value = 0,
  color = '#10B981',
  height = 8,
  showValue = false,
  label,
  borderRadius = 4,
  animate = true,
}) {
  const pct = Math.max(0, Math.min(100, value));

  return (
    <Box>
      {(label || showValue) && (
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
          {label && (
            <Typography variant="caption" fontWeight={500} color="text.primary">{label}</Typography>
          )}
          {showValue && (
            <Typography variant="caption" fontWeight={600} sx={{ color }}>{pct}%</Typography>
          )}
        </Box>
      )}

      <Box
        sx={{
          width: '100%',
          height,
          borderRadius,
          bgcolor: '#E5E7EB',
          overflow: 'hidden',
        }}
      >
        <Box
          sx={{
            width: `${pct}%`,
            height: '100%',
            bgcolor: color,
            borderRadius,
            transition: animate ? 'width 0.8s ease' : 'none',
          }}
        />
      </Box>
    </Box>
  );
}
