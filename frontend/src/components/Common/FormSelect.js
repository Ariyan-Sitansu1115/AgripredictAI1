import React from 'react';
import { FormControl, InputLabel, Select, MenuItem, FormHelperText } from '@mui/material';

/**
 * FormSelect
 * Formik-compatible select dropdown with label and validation support.
 *
 * Props:
 *   name     {string}  – formik field name
 *   formik   {object}  – formik instance
 *   label    {string}
 *   options  {Array}   – [{ value, label }] or string[]
 *   size     {string}  – "small" | "medium"
 *   required {boolean}
 */
export default function FormSelect({
  name,
  formik,
  label,
  options = [],
  size = 'small',
  required = false,
  fullWidth = true,
  ...rest
}) {
  const touched  = formik?.touched?.[name];
  const error    = formik?.errors?.[name];
  const hasError = Boolean(touched && error);

  return (
    <FormControl size={size} fullWidth={fullWidth} error={hasError} {...rest}>
      <InputLabel>{required ? `${label} *` : label}</InputLabel>
      <Select
        id={name}
        name={name}
        value={formik?.values?.[name] ?? ''}
        label={required ? `${label} *` : label}
        onChange={formik?.handleChange}
        onBlur={formik?.handleBlur}
      >
        {options.map((opt) => {
          const val = typeof opt === 'object' ? opt.value : opt;
          const lbl = typeof opt === 'object' ? opt.label : opt;
          return (
            <MenuItem key={val} value={val}>{lbl}</MenuItem>
          );
        })}
      </Select>
      {hasError && <FormHelperText>{error}</FormHelperText>}
    </FormControl>
  );
}
