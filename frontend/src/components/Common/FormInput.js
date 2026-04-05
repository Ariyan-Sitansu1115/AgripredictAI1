import React from 'react';
import { TextField } from '@mui/material';

/**
 * FormInput
 * Thin wrapper around MUI TextField with Formik-compatible props and
 * consistent validation feedback display.
 *
 * Props – all standard TextField props, plus:
 *   name        {string}  – formik field name
 *   formik      {object}  – formik instance (values, touched, errors, handleChange, handleBlur)
 *   label       {string}
 *   type        {string}  – input type (default "text")
 *   size        {string}  – "small" | "medium"
 *   required    {boolean}
 *   placeholder {string}
 *   endAdornment {node}   – optional end adornment
 */
export default function FormInput({
  name,
  formik,
  label,
  type = 'text',
  size = 'small',
  required = false,
  placeholder,
  endAdornment,
  ...rest
}) {
  const touched = formik?.touched?.[name];
  const error   = formik?.errors?.[name];
  const hasError = Boolean(touched && error);

  return (
    <TextField
      id={name}
      name={name}
      label={required ? `${label} *` : label}
      type={type}
      size={size}
      placeholder={placeholder}
      value={formik?.values?.[name] ?? ''}
      onChange={formik?.handleChange}
      onBlur={formik?.handleBlur}
      error={hasError}
      helperText={hasError ? error : rest.helperText}
      InputProps={endAdornment ? { endAdornment } : undefined}
      fullWidth
      {...rest}
    />
  );
}
