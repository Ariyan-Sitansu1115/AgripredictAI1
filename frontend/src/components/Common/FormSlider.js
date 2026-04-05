import React from 'react';
import { Box, Typography, Slider } from '@mui/material';

/**
 * FormSlider
 * Labelled MUI Slider with current value display, min/max labels and
 * Formik integration.
 *
 * Props:
 *   name         {string}  – formik field name
 *   formik       {object}  – formik instance
 *   label        {string}
 *   min          {number}
 *   max          {number}
 *   step         {number}
 *   marks        {boolean}
 *   valueSuffix  {string}  – e.g. "%" or " yrs"
 *   color        {string}  – MUI or hex colour for slider
 *   minLabel     {string}  – optional min label text
 *   maxLabel     {string}  – optional max label text
 *   onChange     {fn}      – optional override onChange (receives value)
 */
export default function FormSlider({
  name,
  formik,
  label,
  min = 0,
  max = 100,
  step = 1,
  marks = false,
  valueSuffix = '',
  color = 'primary',
  minLabel,
  maxLabel,
  onChange,
}) {
  const value = formik?.values?.[name] ?? min;

  const handleChange = (_, v) => {
    if (onChange) {
      onChange(v);
    } else {
      formik?.setFieldValue(name, v);
    }
  };

  return (
    <Box>
      <Typography variant="body2" fontWeight={500} mb={1}>
        {label}: <strong>{value}{valueSuffix}</strong>
      </Typography>

      <Slider
        name={name}
        value={value}
        onChange={handleChange}
        min={min}
        max={max}
        step={step}
        marks={marks}
        valueLabelDisplay="auto"
        valueLabelFormat={(v) => `${v}${valueSuffix}`}
        sx={{ color }}
      />

      {(minLabel || maxLabel) && (
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mt: -0.5 }}>
          <Typography variant="caption" color="text.secondary">{minLabel ?? min}</Typography>
          <Typography variant="caption" color="text.secondary">{maxLabel ?? max}</Typography>
        </Box>
      )}
    </Box>
  );
}
