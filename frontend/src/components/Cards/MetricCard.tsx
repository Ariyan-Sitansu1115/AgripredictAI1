import React from 'react';
import { MetricCard as MetricCardType } from '../../types';
import styles from './Cards.module.css';

interface MetricCardProps {
  metric: MetricCardType;
}

const TrendIcon: React.FC<{ trend: 'up' | 'down' | 'neutral'; value?: number }> = ({ trend, value }) => {
  if (trend === 'up') {
    return (
      <span className="flex items-center gap-1 text-emerald-600 text-sm font-medium">
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7h8m0 0v8m0-8l-8 8-4-4-6 6" />
        </svg>
        {value !== undefined && `${value}%`}
      </span>
    );
  }
  if (trend === 'down') {
    return (
      <span className="flex items-center gap-1 text-red-500 text-sm font-medium">
        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 17h8m0 0v-8m0 8l-8-8-4 4-6-6" />
        </svg>
        {value !== undefined && `${value}%`}
      </span>
    );
  }
  return <span className="text-gray-400 text-sm">–</span>;
};

const MetricCard: React.FC<MetricCardProps> = ({ metric }) => {
  const { title, value, unit, trend, trendValue, icon, color, description } = metric;

  return (
    <div
      className={`${styles.card} bg-white rounded-xl shadow-card p-6 border border-gray-50 relative overflow-hidden`}
    >
      <div
        className="absolute top-0 left-0 w-1 h-full rounded-l-xl"
        style={{ backgroundColor: color }}
      />
      <div className="pl-2">
        <div className="flex items-start justify-between mb-3">
          <div
            className="w-11 h-11 rounded-xl flex items-center justify-center text-xl shadow-sm"
            style={{ backgroundColor: `${color}20` }}
          >
            {icon}
          </div>
          <TrendIcon trend={trend} value={trendValue} />
        </div>
        <p className="text-sm font-medium text-gray-500 mb-1">{title}</p>
        <div className="flex items-baseline gap-1">
          <span className="text-2xl font-bold text-gray-900">{value}</span>
          {unit && <span className="text-sm text-gray-500 font-medium">{unit}</span>}
        </div>
        {description && (
          <p className="text-xs text-gray-400 mt-1.5">{description}</p>
        )}
      </div>
    </div>
  );
};

export default MetricCard;
