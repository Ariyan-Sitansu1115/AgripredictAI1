import React from 'react';
import { Box, Card, CardContent, Typography, Chip, LinearProgress, Avatar } from '@mui/material';
import TrendingUpIcon from '@mui/icons-material/TrendingUp';
import SpaIcon from '@mui/icons-material/Spa';
import { TIMELINE_COLORS } from '../../utils/constants';

/**
 * RotationTimelineCard
 * A single year card used inside RotationTimeline.
 *
 * Props:
 *   yearData  {object}   – { year, crop, icon, profitability, soilImpact, expectedYield, notes }
 *   colorIndex {number}  – index into TIMELINE_COLORS
 *   isLast    {boolean}  – whether this is the final item (hides connector)
 *   onClick   {function} – optional click handler
 */
export default function RotationTimelineCard({ yearData, colorIndex = 0, isLast = false, onClick }) {
  const color = TIMELINE_COLORS[colorIndex % TIMELINE_COLORS.length];

  return (
    <Box sx={{ display: 'flex', gap: 2 }}>
      {/* Connector column */}
      <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', flexShrink: 0 }}>
        <Avatar
          sx={{
            bgcolor: color,
            width: 40,
            height: 40,
            fontSize: '1.2rem',
            cursor: onClick ? 'pointer' : 'default',
            boxShadow: `0 0 0 3px ${color}30`,
          }}
          onClick={onClick}
        >
          {yearData.icon || '🌱'}
        </Avatar>
        {!isLast && (
          <Box sx={{ width: 2, flexGrow: 1, bgcolor: '#E5E7EB', mt: 0.5, minHeight: 24 }} />
        )}
      </Box>

      {/* Card */}
      <Box sx={{ pb: isLast ? 0 : 3, flex: 1 }}>
        <Card
          onClick={onClick}
          sx={{
            borderLeft: `3px solid ${color}`,
            cursor: onClick ? 'pointer' : 'default',
            transition: 'transform 0.2s ease',
            '&:hover': onClick ? { transform: 'translateX(4px)' } : {},
          }}
        >
          <CardContent sx={{ py: 1.5, '&:last-child': { pb: 1.5 } }}>
            {/* Header row */}
            <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
              <Box>
                <Typography variant="caption" color="text.secondary" fontWeight={600} letterSpacing={0.5}>
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

            {/* Progress bar */}
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

            {/* Chips */}
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
                  color:  yearData.soilImpact?.startsWith('+') ? '#065F46' : '#92400E',
                }}
              />
            </Box>

            {/* Notes */}
            {yearData.notes && (
              <Typography variant="caption" color="text.secondary">{yearData.notes}</Typography>
            )}
          </CardContent>
        </Card>
      </Box>
    </Box>
  );
}
