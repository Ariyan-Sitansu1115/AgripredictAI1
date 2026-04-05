import React from 'react';
import { Button, CircularProgress } from '@mui/material';

/**
 * GradientButton
 * Modern gradient CTA button with hover lift and loading state.
 *
 * Props:
 *   children  {node}
 *   loading   {boolean}
 *   startIcon {node}
 *   onClick   {fn}
 *   disabled  {boolean}
 *   size      {'small'|'medium'|'large'}
 *   fullWidth {boolean}
 *   gradient  {string}  – CSS gradient string (optional override)
 *   color     {string}  – MUI color token for fallback (optional)
 */
export default function GradientButton({
  children,
  loading = false,
  startIcon,
  onClick,
  disabled = false,
  size = 'medium',
  fullWidth = false,
  gradient = 'linear-gradient(135deg, #10B981, #047857)',
  ...rest
}) {
  return (
    <Button
      variant="contained"
      size={size}
      onClick={onClick}
      disabled={disabled || loading}
      fullWidth={fullWidth}
      startIcon={loading ? <CircularProgress size={18} color="inherit" /> : startIcon}
      sx={{
        background: disabled || loading ? undefined : gradient,
        fontWeight: 600,
        borderRadius: 2,
        textTransform: 'none',
        boxShadow: '0 4px 14px rgba(16,185,129,0.35)',
        transition: 'transform 0.2s ease, box-shadow 0.2s ease',
        '&:hover': {
          background: gradient,
          transform: 'translateY(-2px)',
          boxShadow: '0 8px 20px rgba(16,185,129,0.45)',
        },
        '&:active': {
          transform: 'translateY(0)',
        },
        ...rest.sx,
      }}
      {...rest}
    >
      {loading ? 'Loading…' : children}
    </Button>
  );
}
