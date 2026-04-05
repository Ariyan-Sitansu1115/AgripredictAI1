// Crop database with icons, types, and agronomic details
export const CROP_DATA = {
  Rice:       { icon: '🍚', type: 'Cereal',   season: 'Kharif',      waterReq: 'High',    rootDepth: 'Shallow' },
  Wheat:      { icon: '🌾', type: 'Cereal',   season: 'Rabi',        waterReq: 'Medium',  rootDepth: 'Medium'  },
  Maize:      { icon: '🌽', type: 'Cereal',   season: 'Kharif/Rabi', waterReq: 'Medium',  rootDepth: 'Deep'    },
  Cotton:     { icon: '🌿', type: 'Fiber',    season: 'Kharif',      waterReq: 'Medium',  rootDepth: 'Deep'    },
  Sugarcane:  { icon: '🎋', type: 'Fiber',    season: 'Annual',      waterReq: 'Very High', rootDepth: 'Deep'  },
  Soybean:    { icon: '🫘', type: 'Legume',   season: 'Kharif',      waterReq: 'Medium',  rootDepth: 'Medium'  },
  Groundnut:  { icon: '🥜', type: 'Legume',   season: 'Kharif',      waterReq: 'Medium',  rootDepth: 'Shallow' },
  Sunflower:  { icon: '🌻', type: 'Oilseed',  season: 'Kharif/Rabi', waterReq: 'Medium',  rootDepth: 'Deep'    },
  Mustard:    { icon: '🌿', type: 'Oilseed',  season: 'Rabi',        waterReq: 'Low',     rootDepth: 'Medium'  },
  Chickpea:   { icon: '🫘', type: 'Legume',   season: 'Rabi',        waterReq: 'Low',     rootDepth: 'Medium'  },
  Lentil:     { icon: '🟤', type: 'Legume',   season: 'Rabi',        waterReq: 'Low',     rootDepth: 'Shallow' },
  'Mung Bean':{ icon: '🟢', type: 'Legume',   season: 'Kharif/Zaid', waterReq: 'Low',     rootDepth: 'Shallow' },
  'Black Gram':{ icon: '⚫', type: 'Legume',  season: 'Kharif',      waterReq: 'Low',     rootDepth: 'Shallow' },
  Sorghum:    { icon: '🌾', type: 'Cereal',   season: 'Kharif',      waterReq: 'Very Low', rootDepth: 'Deep'   },
  Millets:    { icon: '🌾', type: 'Cereal',   season: 'Kharif',      waterReq: 'Very Low', rootDepth: 'Medium' },
  Barley:     { icon: '🌾', type: 'Cereal',   season: 'Rabi',        waterReq: 'Low',     rootDepth: 'Medium'  },
  Tomato:     { icon: '🍅', type: 'Vegetable',season: 'Rabi/Kharif', waterReq: 'Medium',  rootDepth: 'Shallow' },
  Onion:      { icon: '🧅', type: 'Vegetable',season: 'Rabi',        waterReq: 'Medium',  rootDepth: 'Shallow' },
  Potato:     { icon: '🥔', type: 'Vegetable',season: 'Rabi',        waterReq: 'Medium',  rootDepth: 'Shallow' },
  Cabbage:    { icon: '🥬', type: 'Vegetable',season: 'Rabi',        waterReq: 'Medium',  rootDepth: 'Shallow' },
};

// Ordered list of crop names for dropdowns
export const CROP_LIST = Object.keys(CROP_DATA);

// Get icon for a crop name (case-insensitive fallback)
export function getCropIcon(name) {
  if (!name) return '🌱';
  const match = Object.keys(CROP_DATA).find(
    (k) => k.toLowerCase() === name.toLowerCase()
  );
  return match ? CROP_DATA[match].icon : '🌱';
}

// Get crop type badge color
export const CROP_TYPE_COLORS = {
  Cereal:    { bg: '#FEF9C3', color: '#92400E' },
  Legume:    { bg: '#D1FAE5', color: '#065F46' },
  Oilseed:   { bg: '#FEF3C7', color: '#92400E' },
  Fiber:     { bg: '#EDE9FE', color: '#5B21B6' },
  Vegetable: { bg: '#DBEAFE', color: '#1D4ED8' },
};
