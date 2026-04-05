import React from 'react';
import { Box, Typography, Avatar } from '@mui/material';

/**
 * FeatureHighlight
 * Icon + title + description highlight card used in hero / feature sections.
 *
 * Props:
 *   icon        {string|node} – emoji string or MUI icon element
 *   title       {string}
 *   description {string}
 *   color       {string}   – accent colour (default "#10B981")
 *   variant     {'glass'|'default'} – glass = glassmorphism style
 */
export default function FeatureHighlight({ icon, title, description, color = '#10B981', variant = 'default' }) {
  const isGlass = variant === 'glass';

  return (
    <Box
      sx={{
        display: 'flex',
        alignItems: 'flex-start',
        gap: 1.5,
        p: 2,
        borderRadius: 2,
        background: isGlass ? 'rgba(255,255,255,0.12)' : '#F9FAFB',
        backdropFilter: isGlass ? 'blur(8px)' : undefined,
        border: `1px solid ${isGlass ? 'rgba(255,255,255,0.2)' : '#E5E7EB'}`,
        transition: 'background 0.2s ease, border-color 0.2s ease',
        '&:hover': {
          background: isGlass ? 'rgba(255,255,255,0.2)' : '#ECFDF5',
          borderColor: isGlass ? 'rgba(255,255,255,0.3)' : '#6EE7B7',
        },
      }}
    >
      {/* Icon */}
      {typeof icon === 'string' ? (
        <Typography variant="h5" sx={{ lineHeight: 1, flexShrink: 0, mt: 0.25 }}>{icon}</Typography>
      ) : (
        <Avatar sx={{ bgcolor: `${color}20`, width: 36, height: 36, flexShrink: 0 }}>
          {React.cloneElement(icon, { sx: { color, fontSize: 20 } })}
        </Avatar>
      )}

      {/* Text */}
      <Box>
        <Typography
          variant="body2"
          fontWeight={600}
          sx={{ color: isGlass ? 'white' : 'text.primary', lineHeight: 1.4 }}
        >
          {title}
        </Typography>
        {description && (
          <Typography
            variant="caption"
            sx={{ color: isGlass ? 'rgba(255,255,255,0.8)' : 'text.secondary' }}
          >
            {description}
          </Typography>
        )}
      </Box>
    </Box>
  );
}
