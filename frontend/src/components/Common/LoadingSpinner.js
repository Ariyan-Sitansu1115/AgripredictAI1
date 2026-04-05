import React from 'react';
import { Box, CircularProgress, Typography } from '@mui/material';

/**
 * LoadingSpinner
 * Centred animated spinner with optional message.
 *
 * Props:
 *   message {string}  – loading text (default "Loading…")
 *   size    {number}  – spinner diameter (default 48)
 *   color   {string}  – spinner colour (default primary.main / "#10B981")
 *   py      {number}  – vertical padding (default 4)
 */
export default function LoadingSpinner({
  message = 'Loading…',
  size = 48,
  color = '#10B981',
  py = 4,
}) {
  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        gap: 1.5,
        py,
      }}
    >
      <CircularProgress size={size} sx={{ color }} />
      {message && (
        <Typography variant="body2" color="text.secondary">
          {message}
        </Typography>
      )}
    </Box>
  );
}
