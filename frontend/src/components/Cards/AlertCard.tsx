import React from 'react';
import { Alert } from '../../types';
import { formatRelativeTime } from '../../utils/formatters';
import styles from './Cards.module.css';

interface AlertCardProps {
  alert: Alert;
  onDismiss?: (id: string) => void;
  onMarkRead?: (id: string) => void;
}

const severityConfig = {
  critical: {
    border: 'border-l-red-500',
    bg: 'bg-red-50',
    badge: 'bg-red-100 text-red-700',
    dot: 'bg-red-500',
    label: 'Critical',
  },
  warning: {
    border: 'border-l-yellow-500',
    bg: 'bg-yellow-50',
    badge: 'bg-yellow-100 text-yellow-700',
    dot: 'bg-yellow-500',
    label: 'Warning',
  },
  info: {
    border: 'border-l-blue-500',
    bg: 'bg-blue-50',
    badge: 'bg-blue-100 text-blue-700',
    dot: 'bg-blue-500',
    label: 'Info',
  },
};

const AlertCard: React.FC<AlertCardProps> = ({ alert, onDismiss, onMarkRead }) => {
  const config = severityConfig[alert.severity];

  return (
    <div
      className={`${styles.fadeIn} ${styles.card} bg-white rounded-xl shadow-card border-l-4 ${config.border} p-4 ${
        !alert.read ? 'ring-1 ring-gray-100' : 'opacity-75'
      }`}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="flex items-start gap-3 min-w-0">
          <div className={`w-2 h-2 rounded-full ${config.dot} mt-2 shrink-0`} />
          <div className="min-w-0">
            <div className="flex items-center gap-2 flex-wrap mb-1">
              <span className={`text-xs font-semibold px-2 py-0.5 rounded-full ${config.badge}`}>
                {config.label}
              </span>
              {alert.category && (
                <span className="text-xs text-gray-400">{alert.category}</span>
              )}
              {!alert.read && (
                <span className="w-2 h-2 rounded-full bg-primary-500 shrink-0" />
              )}
            </div>
            <h4 className="text-sm font-semibold text-gray-900 truncate">{alert.title}</h4>
            <p className="text-xs text-gray-500 mt-0.5 line-clamp-2">{alert.message}</p>
            <p className="text-xs text-gray-400 mt-1.5">{formatRelativeTime(alert.timestamp)}</p>
          </div>
        </div>

        <div className="flex items-center gap-1 shrink-0">
          {!alert.read && onMarkRead && (
            <button
              onClick={() => onMarkRead(alert.id)}
              className="p-1.5 text-gray-400 hover:text-primary-600 hover:bg-primary-50 rounded-lg transition-colors"
              title="Mark as read"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 13l4 4L19 7" />
              </svg>
            </button>
          )}
          {onDismiss && (
            <button
              onClick={() => onDismiss(alert.id)}
              className="p-1.5 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded-lg transition-colors"
              title="Dismiss"
            >
              <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          )}
        </div>
      </div>
    </div>
  );
};

export default AlertCard;
