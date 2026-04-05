import React from 'react';
import { Box, Typography } from '@mui/material';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import TrendingDownIcon from '@mui/icons-material/TrendingDown';
import TrendingFlatIcon from '@mui/icons-material/TrendingFlat';

/**
 * TrendArrow
 * Compact up / down / neutral trend indicator with optional percentage label.
 *
 * Props:
 *   value    {number}  – positive = up, negative = down, 0 = neutral
 *   suffix   {string}  – e.g. "%" (default "")
 *   showIcon {boolean} – show arrow icon (default true)
 *   size     {'small'|'medium'} – icon size (default "small")
 */
export default function TrendArrow({ value, suffix = '%', showIcon = true, size = 'small' }) {
  if (value === undefined || value === null) return null;

  const isUp     = value > 0;
  const isDown   = value < 0;
  const color    = isUp ? '#10B981' : isDown ? '#EF4444' : '#6B7280';
  const Icon     = isUp ? TrendingUpIcon : isDown ? TrendingDownIcon : TrendingFlatIcon;
  const display  = isUp ? `+${value}${suffix}` : `${value}${suffix}`;
  const fontSize = size === 'small' ? 16 : 22;

  return (
    <Box
      sx={{
        display: 'inline-flex',
        alignItems: 'center',
        gap: 0.25,
        color,
        fontWeight: 600,
      }}
    >
      {showIcon && <Icon sx={{ fontSize }} />}
      <Typography variant="caption" fontWeight={600} sx={{ color }}>
        {display}
      </Typography>
    </Box>
  );
}
