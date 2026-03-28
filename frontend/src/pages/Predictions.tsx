import React, { useState, useMemo } from 'react';
import PriceChart from '../components/Charts/PriceChart';
import LoadingSpinner from '../components/Common/LoadingSpinner';
import { PricePrediction, PriceHistoryPoint } from '../types';
import { formatCurrency, formatPercentage } from '../utils/formatters';
import { CROP_NAMES } from '../utils/constants';

const buildHistory = (base: number, trend: number): PriceHistoryPoint[] =>
  Array.from({ length: 30 }, (_, i) => ({
    date: new Date(Date.now() - (29 - i) * 86400000).toISOString().split('T')[0],
    actual: i < 25 ? Math.round(base + trend * i * 0.5 + (Math.random() - 0.5) * 20) : undefined,
    predicted: i >= 20 ? Math.round(base + trend * i * 0.6 + (Math.random() - 0.5) * 15) : undefined,
  }));

const MOCK_PREDICTIONS: PricePrediction[] = [
  { id: '1', crop: 'Wheat', currentPrice: 425, predictedPrice: 448, confidence: 87, trend: 'up', period: '30 days', priceHistory: buildHistory(400, 1.2) },
  { id: '2', crop: 'Rice', currentPrice: 380, predictedPrice: 365, confidence: 82, trend: 'down', period: '30 days', priceHistory: buildHistory(395, -0.8) },
  { id: '3', crop: 'Corn', currentPrice: 290, predictedPrice: 305, confidence: 79, trend: 'up', period: '30 days', priceHistory: buildHistory(278, 0.9) },
  { id: '4', crop: 'Soybean', currentPrice: 520, predictedPrice: 535, confidence: 84, trend: 'up', period: '30 days', priceHistory: buildHistory(505, 1.5) },
  { id: '5', crop: 'Cotton', currentPrice: 175, predictedPrice: 168, confidence: 76, trend: 'down', period: '30 days', priceHistory: buildHistory(182, -0.5) },
];

const Predictions: React.FC = () => {
  const [selectedCrop, setSelectedCrop] = useState('Wheat');
  const [isLoading] = useState(false);

  const selectedPrediction = useMemo(
    () => MOCK_PREDICTIONS.find(p => p.crop === selectedCrop) || MOCK_PREDICTIONS[0],
    [selectedCrop]
  );

  const priceDiff = selectedPrediction.predictedPrice - selectedPrediction.currentPrice;
  const priceDiffPct = (priceDiff / selectedPrediction.currentPrice) * 100;

  if (isLoading) {
    return (
      <div className="flex items-center justify-center min-h-96">
        <LoadingSpinner size="lg" label="Loading predictions..." />
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Price Predictions</h1>
          <p className="text-sm text-gray-500 mt-1">AI-powered market price forecasts</p>
        </div>
        <select
          value={selectedCrop}
          onChange={e => setSelectedCrop(e.target.value)}
          className="input-field max-w-[180px]"
        >
          {CROP_NAMES.slice(0, 5).map(crop => (
            <option key={crop} value={crop}>{crop}</option>
          ))}
        </select>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="bg-white rounded-xl shadow-card p-5">
          <p className="text-xs text-gray-500 font-medium mb-1">Current Price</p>
          <p className="text-2xl font-bold text-gray-900">{formatCurrency(selectedPrediction.currentPrice)}</p>
          <p className="text-xs text-gray-400 mt-1">per ton</p>
        </div>
        <div className="bg-white rounded-xl shadow-card p-5">
          <p className="text-xs text-gray-500 font-medium mb-1">Predicted Price ({selectedPrediction.period})</p>
          <p className={`text-2xl font-bold ${priceDiff >= 0 ? 'text-emerald-600' : 'text-red-500'}`}>
            {formatCurrency(selectedPrediction.predictedPrice)}
          </p>
          <p className={`text-xs mt-1 font-medium ${priceDiff >= 0 ? 'text-emerald-600' : 'text-red-500'}`}>
            {priceDiff >= 0 ? '+' : ''}{formatCurrency(priceDiff)} ({formatPercentage(priceDiffPct)})
          </p>
        </div>
        <div className="bg-white rounded-xl shadow-card p-5">
          <p className="text-xs text-gray-500 font-medium mb-1">Model Confidence</p>
          <p className="text-2xl font-bold text-gray-900">{selectedPrediction.confidence}%</p>
          <div className="mt-2 h-2 bg-gray-100 rounded-full overflow-hidden">
            <div
              className="h-full bg-gradient-to-r from-primary-400 to-primary-600 rounded-full transition-all duration-500"
              style={{ width: `${selectedPrediction.confidence}%` }}
            />
          </div>
        </div>
      </div>

      <PriceChart
        data={selectedPrediction.priceHistory}
        title={`${selectedCrop} Price History & Prediction`}
        cropName={selectedCrop}
      />

      <div className="bg-white rounded-xl shadow-card overflow-hidden">
        <div className="px-6 py-4 border-b border-gray-100">
          <h3 className="text-base font-bold text-gray-900">All Crop Predictions</h3>
        </div>
        <div className="overflow-x-auto">
          <table className="w-full text-sm">
            <thead>
              <tr className="bg-gray-50 border-b border-gray-100">
                <th className="text-left px-6 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">Crop</th>
                <th className="text-right px-6 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">Current Price</th>
                <th className="text-right px-6 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">Predicted</th>
                <th className="text-right px-6 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">Change</th>
                <th className="text-right px-6 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">Confidence</th>
                <th className="text-center px-6 py-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">Trend</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-gray-50">
              {MOCK_PREDICTIONS.map(pred => {
                const diff = pred.predictedPrice - pred.currentPrice;
                const pct = (diff / pred.currentPrice) * 100;
                return (
                  <tr
                    key={pred.id}
                    className={`hover:bg-gray-50 cursor-pointer transition-colors ${selectedCrop === pred.crop ? 'bg-primary-50' : ''}`}
                    onClick={() => setSelectedCrop(pred.crop)}
                  >
                    <td className="px-6 py-4 font-semibold text-gray-900">{pred.crop}</td>
                    <td className="px-6 py-4 text-right text-gray-700">{formatCurrency(pred.currentPrice)}</td>
                    <td className="px-6 py-4 text-right font-semibold text-gray-900">{formatCurrency(pred.predictedPrice)}</td>
                    <td className={`px-6 py-4 text-right font-semibold ${diff >= 0 ? 'text-emerald-600' : 'text-red-500'}`}>
                      {diff >= 0 ? '+' : ''}{formatPercentage(pct)}
                    </td>
                    <td className="px-6 py-4 text-right">
                      <div className="flex items-center justify-end gap-2">
                        <div className="w-16 h-1.5 bg-gray-100 rounded-full overflow-hidden">
                          <div
                            className="h-full bg-primary-500 rounded-full"
                            style={{ width: `${pred.confidence}%` }}
                          />
                        </div>
                        <span className="text-gray-700 w-10 text-right">{pred.confidence}%</span>
                      </div>
                    </td>
                    <td className="px-6 py-4 text-center">
                      {pred.trend === 'up' && <span className="text-emerald-500 text-lg">↑</span>}
                      {pred.trend === 'down' && <span className="text-red-500 text-lg">↓</span>}
                      {pred.trend === 'neutral' && <span className="text-gray-400 text-lg">→</span>}
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Predictions;
