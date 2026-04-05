import React, { useState } from 'react';
import { Alert, AlertTitle, Collapse, IconButton } from '@mui/material';
import CloseIcon from '@mui/icons-material/Close';

/**
 * AlertNotification
 * Dismissible inline alert with slide animation.
 *
 * Props:
 *   severity    {'success'|'info'|'warning'|'error'}  (default "info")
 *   title       {string}   – optional bold title
 *   children    {node}     – message content
 *   dismissible {boolean}  – show close button (default true)
 *   sx          {object}   – additional MUI sx overrides
 */
export default function AlertNotification({
  severity = 'info',
  title,
  children,
  dismissible = true,
  sx = {},
}) {
  const [open, setOpen] = useState(true);

  return (
    <Collapse in={open}>
      <Alert
        severity={severity}
        sx={{ borderRadius: 2, mb: 1.5, ...sx }}
        action={
          dismissible ? (
            <IconButton
              aria-label="close"
              size="small"
              onClick={() => setOpen(false)}
            >
              <CloseIcon fontSize="inherit" />
            </IconButton>
          ) : undefined
        }
      >
        {title && <AlertTitle>{title}</AlertTitle>}
        {children}
      </Alert>
    </Collapse>
  );
}
