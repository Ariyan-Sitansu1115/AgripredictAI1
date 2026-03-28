export interface User {
  id: string;
  name: string;
  email: string;
  farmName?: string;
  location?: string;
  farmSize?: number;
  preferredCrops?: string[];
  avatar?: string;
}

export interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterCredentials extends LoginCredentials {
  name: string;
  farmName?: string;
}

export interface MetricCard {
  id: string;
  title: string;
  value: number | string;
  unit?: string;
  trend: 'up' | 'down' | 'neutral';
  trendValue?: number;
  icon: string;
  color: string;
  description?: string;
}

export interface Alert {
  id: string;
  severity: 'critical' | 'warning' | 'info';
  title: string;
  message: string;
  timestamp: string;
  read: boolean;
  category?: string;
}

export interface DashboardData {
  metrics: MetricCard[];
  alerts: Alert[];
  lastUpdated: string;
}

export interface PriceHistoryPoint {
  date: string;
  actual?: number;
  predicted?: number;
  crop?: string;
}

export interface PricePrediction {
  id: string;
  crop: string;
  currentPrice: number;
  predictedPrice: number;
  confidence: number;
  trend: 'up' | 'down' | 'neutral';
  period: string;
  priceHistory: PriceHistoryPoint[];
}

export interface CropRecommendation {
  id: string;
  crop: string;
  profitabilityScore: number;
  riskLevel: 'low' | 'medium' | 'high';
  season: string;
  confidence: number;
  expectedYield: number;
  waterRequirement: string;
  marketDemand: 'high' | 'medium' | 'low';
  description?: string;
}

export interface RiskDimension {
  metric: string;
  value: number;
  fullMark: number;
}

export interface RiskData {
  overall: number;
  dimensions: RiskDimension[];
  category: 'low' | 'medium' | 'high';
  factors: string[];
}

export interface ProfitDataPoint {
  month: string;
  projected: number;
  actual?: number;
}

export interface ProfitData {
  totalProjected: number;
  totalActual?: number;
  roi: number;
  breakdown: ProfitDataPoint[];
}

export interface SimulationScenario {
  name: string;
  revenue: number;
  cost: number;
  profit: number;
  probability: number;
}

export interface SimulationResult {
  id: string;
  crop: string;
  scenarios: SimulationScenario[];
  bestCase: SimulationScenario;
  worstCase: SimulationScenario;
  expectedCase: SimulationScenario;
}
