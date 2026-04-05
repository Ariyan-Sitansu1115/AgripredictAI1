import React from 'react';
import { Box, Card, CardContent, Typography } from '@mui/material';
import { ResponsiveContainer } from 'recharts';

/**
 * AnimatedChart
 * Wrapper around Recharts ResponsiveContainer with a consistent card style,
 * optional title and subtitle.
 *
 * Props:
 *   title    {string}
 *   subtitle {string}
 *   height   {number}  – chart height (default 280)
 *   children {node}    – a Recharts chart element
 *   noPadding {boolean} – removes CardContent padding
 */
export default function AnimatedChart({ title, subtitle, height = 280, children, noPadding = false }) {
  return (
    <Card>
      <CardContent sx={noPadding ? { p: 0, '&:last-child': { pb: 0 } } : {}}>
        {title && (
          <Box sx={{ px: noPadding ? 2 : 0, pt: noPadding ? 2 : 0, mb: 2 }}>
            <Typography variant="h6" fontWeight={600}>{title}</Typography>
            {subtitle && (
              <Typography variant="body2" color="text.secondary">{subtitle}</Typography>
            )}
          </Box>
        )}

        <Box
          sx={{
            borderRadius: 2,
            overflow: 'hidden',
            animation: 'fadeIn 0.4s ease',
            '@keyframes fadeIn': {
              from: { opacity: 0 },
              to:   { opacity: 1 },
            },
          }}
        >
          <ResponsiveContainer width="100%" height={height}>
            {children}
          </ResponsiveContainer>
        </Box>
      </CardContent>
    </Card>
  );
}
