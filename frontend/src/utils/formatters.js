// ── Currency / Number ────────────────────────────────────────────────────────

/** Format a number as Indian Rupees (abbreviated) */
export function formatINR(value) {
  if (value >= 10000000) return `₹${(value / 10000000).toFixed(1)}Cr`;
  if (value >= 100000) return `₹${(value / 100000).toFixed(1)}L`;
  if (value >= 1000) return `₹${(value / 1000).toFixed(0)}K`;
  return `₹${value}`;
}

/** Format full Indian Rupee with commas */
export function formatINRFull(value) {
  return `₹${Number(value).toLocaleString('en-IN')}`;
}

// ── Percentages ──────────────────────────────────────────────────────────────

/** Add + sign for positive values */
export function formatPercent(value, decimals = 0) {
  const num = Number(value);
  const sign = num > 0 ? '+' : '';
  return `${sign}${num.toFixed(decimals)}%`;
}

/** 0-1 fraction → 0-100% string */
export function fractionToPercent(value, decimals = 0) {
  return `${(Number(value) * 100).toFixed(decimals)}%`;
}

// ── Soil / Agronomy ──────────────────────────────────────────────────────────

/** Get human-readable soil health label */
export function soilHealthLabel(score) {
  if (score >= 75) return 'Excellent';
  if (score >= 60) return 'Good';
  if (score >= 45) return 'Moderate';
  if (score >= 30) return 'Poor';
  return 'Critical';
}

/** Get colour for a soil health score */
export function soilHealthColor(score) {
  if (score >= 75) return '#10B981';
  if (score >= 50) return '#F59E0B';
  return '#EF4444';
}

/** Get colour for a match / profitability score */
export function matchScoreColor(score) {
  if (score >= 80) return '#10B981';
  if (score >= 60) return '#F59E0B';
  return '#EF4444';
}

// ── Dates ────────────────────────────────────────────────────────────────────

/** e.g. "Apr 2025" */
export function formatMonthYear(date) {
  return new Date(date).toLocaleDateString('en-IN', { month: 'short', year: 'numeric' });
}

/** ISO → "05 Apr 2025" */
export function formatDate(date) {
  return new Date(date).toLocaleDateString('en-IN', {
    day: '2-digit',
    month: 'short',
    year: 'numeric',
  });
}

// ── Yield ────────────────────────────────────────────────────────────────────

/** e.g. 5.2 → "5.2 t/ha" */
export function formatYield(value) {
  return `${Number(value).toFixed(1)} t/ha`;
}

// ── Misc ─────────────────────────────────────────────────────────────────────

/** Clamp a value between min and max */
export function clamp(value, min, max) {
  return Math.max(min, Math.min(max, value));
}

/** Convert an area in hectares to acres */
export function haToAcres(ha) {
  return (Number(ha) * 2.471).toFixed(2);
}
