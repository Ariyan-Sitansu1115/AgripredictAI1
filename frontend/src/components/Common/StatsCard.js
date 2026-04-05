import React from 'react';
import { Box, Card, CardContent, Typography, Avatar } from '@mui/material';
import TrendArrow from './TrendArrow';

/**
 * StatsCard
 * Compact card that shows an icon, a value, a label and an optional trend.
 *
 * Props:
 *   icon    {node}    – MUI icon element
 *   value   {string|number}
 *   label   {string}
 *   sub     {string}  – optional subtitle / trend text
 *   color   {string}  – accent colour
 *   trend   {number}  – positive = up, negative = down, 0/undefined = neutral
 *   onClick {fn}      – optional click handler
 */
export default function StatsCard({ icon, value, label, sub, color = '#10B981', trend, onClick }) {
  return (
    <Card
      onClick={onClick}
      sx={{
        cursor: onClick ? 'pointer' : 'default',
        transition: 'transform 0.2s ease, box-shadow 0.2s ease',
        '&:hover': onClick
          ? { transform: 'translateY(-3px)', boxShadow: '0 8px 24px rgba(0,0,0,0.12)' }
          : {},
      }}
    >
      <CardContent sx={{ p: 2.5, '&:last-child': { pb: 2.5 } }}>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.5, mb: 1 }}>
          <Avatar sx={{ bgcolor: `${color}20`, width: 40, height: 40 }}>
            {icon ? React.cloneElement(icon, { sx: { color, fontSize: 22 } }) : null}
          </Avatar>
          <Box sx={{ flex: 1, minWidth: 0 }}>
            <Typography variant="h5" fontWeight={700} sx={{ color, lineHeight: 1.2 }}>
              {value}
            </Typography>
            <Typography variant="body2" fontWeight={500} noWrap>{label}</Typography>
          </Box>
          {trend !== undefined && <TrendArrow value={trend} />}
        </Box>
        {sub && (
          <Typography variant="caption" color="text.secondary">{sub}</Typography>
        )}
      </CardContent>
    </Card>
  );
}
