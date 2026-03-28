import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import DashboardHeader from './DashboardHeader';
import MetricCard from '../Cards/MetricCard';
import AlertCard from '../Cards/AlertCard';
import RecommendationCard from '../Cards/RecommendationCard';
import PriceChart from '../Charts/PriceChart';
import ProfitChart from '../Charts/ProfitChart';
import LoadingSpinner from '../Common/LoadingSpinner';
import { MetricCard as MetricCardType, Alert, CropRecommendation, PriceHistoryPoint, ProfitDataPoint } from '../../types';
import { formatRelativeTime } from '../../utils/formatters';

const generatePriceHistory = (): PriceHistoryPoint[] => {
  const points: PriceHistoryPoint[] = [];
  const now = Date.now();
  for (let i = 29; i >= 0; i--) {
    const date = new Date(now - i * 86400000).toISOString().split('T')[0];
    points.push({
      date,
      actual: i > 5 ? Math.round(400 + Math.sin(i * 0.3) * 30 + Math.random() * 15) : undefined,
      predicted: i <= 8 ? Math.round(420 + Math.cos(i * 0.25) * 20 + Math.random() * 10) : undefined,
    });
  }
  return points;
};

const MOCK_METRICS: MetricCardType[] = [
  {
    id: '1',
    title: 'Predicted Revenue',
    value: '$124,500',
    trend: 'up',
    trendValue: 12.5,
    icon: '💰',
    color: '#10B981',
    description: 'Next 30 days forecast',
  },
  {
    id: '2',
    title: 'Active Crops',
    value: 8,
    unit: 'crops',
    trend: 'up',
    trendValue: 2,
    icon: '🌾',
    color: '#059669',
    description: 'Currently monitored',
  },
  {
    id: '3',
    title: 'Risk Score',
    value: '23%',
    trend: 'down',
    trendValue: 5,
    icon: '⚠️',
    color: '#F59E0B',
    description: 'Overall portfolio risk',
  },
  {
    id: '4',
    title: 'Wheat Market Price',
    value: '$425',
    unit: '/ton',
    trend: 'up',
    trendValue: 3.2,
    icon: '📈',
    color: '#3B82F6',
    description: 'Current spot price',
  },
];

const MOCK_ALERTS: Alert[] = [
  {
    id: 'a1',
    severity: 'critical',
    title: 'Frost Warning',
    message: 'Temperatures expected to drop below 0°C in your region tonight. Protect sensitive crops immediately.',
    timestamp: new Date(Date.now() - 3600000).toISOString(),
    read: false,
    category: 'Weather',
  },
  {
    id: 'a2',
    severity: 'warning',
    title: 'Wheat Price Drop Predicted',
    message: 'AI models predict a 8% decline in wheat prices over the next 2 weeks. Consider adjusting selling strategy.',
    timestamp: new Date(Date.now() - 7200000).toISOString(),
    read: false,
    category: 'Market',
  },
  {
    id: 'a3',
    severity: 'info',
    title: 'Optimal Planting Window',
    message: 'This week is optimal for planting corn based on soil temperature and weather forecasts.',
    timestamp: new Date(Date.now() - 86400000).toISOString(),
    read: true,
    category: 'Planting',
  },
];

const MOCK_RECOMMENDATIONS: CropRecommendation[] = [
  {
    id: 'r1',
    crop: 'Wheat',
    profitabilityScore: 87,
    riskLevel: 'low',
    season: 'Winter',
    confidence: 91,
    expectedYield: 4.5,
    waterRequirement: 'Medium',
    marketDemand: 'high',
    description: 'Strong global demand and favorable weather conditions make wheat an excellent choice.',
  },
  {
    id: 'r2',
    crop: 'Corn',
    profitabilityScore: 74,
    riskLevel: 'medium',
    season: 'Summer',
    confidence: 83,
    expectedYield: 8.2,
    waterRequirement: 'High',
    marketDemand: 'high',
    description: 'Good profitability with adequate irrigation. Strong ethanol market driving demand.',
  },
  {
    id: 'r3',
    crop: 'Soybean',
    profitabilityScore: 69,
    riskLevel: 'low',
    season: 'Summer',
    confidence: 78,
    expectedYield: 2.8,
    waterRequirement: 'Low',
    marketDemand: 'medium',
    description: 'Low water requirement and soil-enriching properties make soybeans a sustainable option.',
  },
];

const MOCK_PROFIT: ProfitDataPoint[] = [
  { month: 'Jan', projected: 18000, actual: 17200 },
  { month: 'Feb', projected: 21000, actual: 22100 },
  { month: 'Mar', projected: 24500, actual: 23800 },
  { month: 'Apr', projected: 19800, actual: 20500 },
  { month: 'May', projected: 28000, actual: 27300 },
  { month: 'Jun', projected: 32000 },
];

const Dashboard: React.FC = () => {
  const [alerts, setAlerts] = useState<Alert[]>(MOCK_ALERTS);
  const [isLoading, setIsLoading] = useState(true);
  const [lastUpdated, setLastUpdated] = useState('');

  useEffect(() => {
    const timer = setTimeout(() => {
      setIsLoading(false);
      setLastUpdated(formatRelativeTime(new Date().toISOString()));
    }, 800);
    return () => clearTimeout(timer);
  }, []);

  const handleDismiss = (id: string) => {
    setAlerts(prev => prev.filter(a => a.id !== id));
  };

  const handleMarkRead = (id: string) => {
    setAlerts(prev => prev.map(a => a.id === id ? { ...a, read: true } : a));
  };

  const handleRefresh = () => {
    setIsLoading(true);
    return new Promise<void>(resolve => {
      setTimeout(() => {
        setIsLoading(false);
        setLastUpdated(formatRelativeTime(new Date().toISOString()));
        resolve();
      }, 1000);
    });
  };

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-96">
        <LoadingSpinner size="lg" label="Loading dashboard..." />
      </div>
    );
  }

  const unreadCount = alerts.filter(a => !a.read).length;

  return (
    <div className="space-y-6">
      <DashboardHeader lastUpdated={lastUpdated} onRefresh={handleRefresh} />

      <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-4 gap-4">
        {MOCK_METRICS.map(metric => (
          <MetricCard key={metric.id} metric={metric} />
        ))}
      </div>

      <PriceChart
        data={generatePriceHistory()}
        title="Wheat Price History & Prediction"
        cropName="Wheat"
      />

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-1 space-y-3">
          <div className="flex items-center justify-between">
            <h2 className="text-base font-bold text-gray-900">Recent Alerts</h2>
            {unreadCount > 0 && (
              <span className="badge-danger">{unreadCount} unread</span>
            )}
          </div>
          {alerts.length === 0 ? (
            <div className="bg-white rounded-xl shadow-card p-8 text-center">
              <div className="text-3xl mb-2">✅</div>
              <p className="text-sm text-gray-500">No active alerts</p>
            </div>
          ) : (
            alerts.map(alert => (
              <AlertCard
                key={alert.id}
                alert={alert}
                onDismiss={handleDismiss}
                onMarkRead={handleMarkRead}
              />
            ))
          )}
        </div>

        <div className="lg:col-span-2">
          <div className="flex items-center justify-between mb-3">
            <h2 className="text-base font-bold text-gray-900">Top Recommendations</h2>
            <Link to="/recommendations" className="text-xs text-primary-600 hover:text-primary-700 font-medium">
              View all →
            </Link>
          </div>
          <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-4">
            {MOCK_RECOMMENDATIONS.map(rec => (
              <RecommendationCard key={rec.id} recommendation={rec} />
            ))}
          </div>
        </div>
      </div>

      <ProfitChart data={MOCK_PROFIT} />
    </div>
  );
};

export default Dashboard;
