// ── Color Palette ────────────────────────────────────────────────────────────
export const COLORS = {
  primaryGreen: '#10B981',
  darkGreen: '#047857',
  lightGreen: '#D1FAE5',
  brown: '#92400E',
  amber: '#F59E0B',
  red: '#EF4444',
  white: '#FFFFFF',
  lightGray: '#F9FAFB',
  darkGray: '#374151',
  purple: '#8B5CF6',
  blue: '#3B82F6',
  indigo: '#6366F1',
};

// ── Soil health thresholds ───────────────────────────────────────────────────
export const SOIL_HEALTH = {
  excellent: 75,
  moderate: 50,
};

// ── Nutrient reference ranges (ppm or %) ────────────────────────────────────
export const NUTRIENT_RANGES = {
  nitrogen:     { min: 0, max: 100, optimal: 50,  unit: 'ppm' },
  phosphorus:   { min: 0, max: 60,  optimal: 25,  unit: 'ppm' },
  potassium:    { min: 0, max: 300, optimal: 150, unit: 'ppm' },
  organicMatter:{ min: 0, max: 8,   optimal: 4,   unit: '%'   },
  moisture:     { min: 0, max: 100, optimal: 65,  unit: '%'   },
  ph:           { min: 0, max: 14,  optimal: 6.5, unit: ''    },
};

// ── Pest pressure levels ─────────────────────────────────────────────────────
export const PEST_PRESSURE = [
  { value: 'low',    label: 'Low – Minimal pest history' },
  { value: 'medium', label: 'Medium – Occasional outbreaks' },
  { value: 'high',   label: 'High – Frequent infestations' },
];

// ── Timeline color palette ───────────────────────────────────────────────────
export const TIMELINE_COLORS = [
  '#10B981', '#F59E0B', '#8B5CF6', '#3B82F6', '#EF4444', '#EC4899', '#14B8A6',
];

// ── Chart theme ──────────────────────────────────────────────────────────────
export const CHART_COLORS = {
  nitrogen:    '#10B981',
  phosphorus:  '#F59E0B',
  potassium:   '#8B5CF6',
  organicMatter: '#92400E',
  healthScore: '#3B82F6',
};

// ── Animation durations (ms) ─────────────────────────────────────────────────
export const ANIMATION = {
  fast:   150,
  normal: 300,
  slow:   500,
};
