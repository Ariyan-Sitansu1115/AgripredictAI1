export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

export const API_ENDPOINTS = {
  LOGIN: '/api/auth/login',
  REGISTER: '/api/auth/register',
  REFRESH: '/api/auth/refresh',
  DASHBOARD: '/api/dashboard',
  PREDICTION: '/api/prediction',
  RECOMMENDATION: '/api/recommendation',
  PROFIT: '/api/profit',
  RISK: '/api/risk',
  ALERT: '/api/alert',
  SIMULATION: '/api/simulation',
  PROFILE: '/api/profile',
};

export const CROP_NAMES = [
  'Wheat', 'Rice', 'Corn', 'Soybean', 'Cotton',
  'Sugarcane', 'Tomato', 'Potato', 'Onion', 'Chili'
];

export const CHART_COLORS = {
  primary: '#10B981',
  secondary: '#059669',
  accent: '#34D399',
  warning: '#F59E0B',
  danger: '#EF4444',
  info: '#3B82F6',
  purple: '#8B5CF6',
  gray: '#6B7280',
};

export const SEVERITY_COLORS = {
  critical: 'red',
  warning: 'yellow',
  info: 'blue',
};

export const RISK_LEVELS = {
  low: { color: '#10B981', label: 'Low Risk' },
  medium: { color: '#F59E0B', label: 'Medium Risk' },
  high: { color: '#EF4444', label: 'High Risk' },
};
