import React, { useState, useMemo } from 'react';
import AlertCard from '../components/Cards/AlertCard';
import { Alert } from '../types';

const MOCK_ALERTS: Alert[] = [
  {
    id: 'a1',
    severity: 'critical',
    title: 'Frost Warning Tonight',
    message: 'Temperature expected to drop to -3°C tonight. Cover sensitive seedlings immediately and activate frost protection systems.',
    timestamp: new Date(Date.now() - 1800000).toISOString(),
    read: false,
    category: 'Weather',
  },
  {
    id: 'a2',
    severity: 'critical',
    title: 'Pest Outbreak Detected',
    message: 'High probability of armyworm outbreak in your region based on satellite imagery and weather patterns. Apply preventive pesticides.',
    timestamp: new Date(Date.now() - 3600000).toISOString(),
    read: false,
    category: 'Pest',
  },
  {
    id: 'a3',
    severity: 'warning',
    title: 'Wheat Price Decline Forecast',
    message: 'AI models predict an 8% decline in wheat prices over the next 2 weeks due to increased global supply.',
    timestamp: new Date(Date.now() - 7200000).toISOString(),
    read: false,
    category: 'Market',
  },
  {
    id: 'a4',
    severity: 'warning',
    title: 'Low Soil Moisture Alert',
    message: 'Soil moisture levels in Field B have dropped below optimal range. Consider irrigation within 48 hours.',
    timestamp: new Date(Date.now() - 14400000).toISOString(),
    read: true,
    category: 'Soil',
  },
  {
    id: 'a5',
    severity: 'info',
    title: 'Optimal Planting Window',
    message: 'This week provides optimal conditions for corn planting. Soil temperature at 18°C with favorable 10-day outlook.',
    timestamp: new Date(Date.now() - 86400000).toISOString(),
    read: true,
    category: 'Planting',
  },
  {
    id: 'a6',
    severity: 'info',
    title: 'Market Report Available',
    message: 'Weekly crop market analysis report is ready. Highlights include soybean export demand increasing 12% month-over-month.',
    timestamp: new Date(Date.now() - 172800000).toISOString(),
    read: true,
    category: 'Market',
  },
];

type FilterType = 'all' | 'critical' | 'warning' | 'info';

const Alerts: React.FC = () => {
  const [alerts, setAlerts] = useState<Alert[]>(MOCK_ALERTS);
  const [filter, setFilter] = useState<FilterType>('all');

  const filtered = useMemo(() => {
    if (filter === 'all') return alerts;
    return alerts.filter(a => a.severity === filter);
  }, [alerts, filter]);

  const counts = useMemo(() => ({
    all: alerts.length,
    critical: alerts.filter(a => a.severity === 'critical').length,
    warning: alerts.filter(a => a.severity === 'warning').length,
    info: alerts.filter(a => a.severity === 'info').length,
  }), [alerts]);

  const unreadCount = alerts.filter(a => !a.read).length;

  const handleDismiss = (id: string) => {
    setAlerts(prev => prev.filter(a => a.id !== id));
  };

  const handleMarkRead = (id: string) => {
    setAlerts(prev => prev.map(a => a.id === id ? { ...a, read: true } : a));
  };

  const handleMarkAllRead = () => {
    setAlerts(prev => prev.map(a => ({ ...a, read: true })));
  };

  const filterButtons: { key: FilterType; label: string; color: string }[] = [
    { key: 'all', label: 'All', color: 'gray' },
    { key: 'critical', label: 'Critical', color: 'red' },
    { key: 'warning', label: 'Warning', color: 'yellow' },
    { key: 'info', label: 'Info', color: 'blue' },
  ];

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Alerts & Notifications</h1>
          <p className="text-sm text-gray-500 mt-1">
            {unreadCount > 0 ? `${unreadCount} unread alerts` : 'All alerts read'}
          </p>
        </div>
        {unreadCount > 0 && (
          <button onClick={handleMarkAllRead} className="btn-secondary text-sm">
            ✓ Mark All Read
          </button>
        )}
      </div>

      <div className="flex flex-wrap gap-2">
        {filterButtons.map(({ key, label }) => {
          const count = counts[key];
          const isActive = filter === key;
          return (
            <button
              key={key}
              onClick={() => setFilter(key)}
              className={`px-4 py-2 rounded-xl text-sm font-medium flex items-center gap-2 transition-colors ${
                isActive
                  ? 'bg-primary-500 text-white shadow-sm'
                  : 'bg-white text-gray-600 border border-gray-200 hover:bg-gray-50'
              }`}
            >
              {label}
              <span className={`text-xs font-bold px-1.5 py-0.5 rounded-full ${
                isActive ? 'bg-white/20 text-white' : 'bg-gray-100 text-gray-500'
              }`}>
                {count}
              </span>
            </button>
          );
        })}
      </div>

      <div className="space-y-3">
        {filtered.length === 0 ? (
          <div className="bg-white rounded-xl shadow-card p-12 text-center">
            <div className="text-4xl mb-3">🔔</div>
            <p className="text-gray-500 font-medium">No alerts in this category</p>
          </div>
        ) : (
          filtered.map(alert => (
            <AlertCard
              key={alert.id}
              alert={alert}
              onDismiss={handleDismiss}
              onMarkRead={handleMarkRead}
            />
          ))
        )}
      </div>
    </div>
  );
};

export default Alerts;
