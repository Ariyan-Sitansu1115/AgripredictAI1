import React from 'react';
import { CropRecommendation } from '../../types';
import styles from './Cards.module.css';

interface RecommendationCardProps {
  recommendation: CropRecommendation;
}

const CROP_EMOJIS: Record<string, string> = {
  Wheat: '🌾', Rice: '🌾', Corn: '🌽', Soybean: '🫘',
  Cotton: '🌸', Sugarcane: '🍬', Tomato: '🍅',
  Potato: '🥔', Onion: '🧅', Chili: '🌶️',
};

const riskConfig = {
  low: { label: 'Low Risk', classes: 'bg-green-100 text-green-700' },
  medium: { label: 'Medium Risk', classes: 'bg-yellow-100 text-yellow-700' },
  high: { label: 'High Risk', classes: 'bg-red-100 text-red-700' },
};

const demandConfig = {
  high: { label: 'High Demand', classes: 'bg-emerald-100 text-emerald-700' },
  medium: { label: 'Medium Demand', classes: 'bg-blue-100 text-blue-700' },
  low: { label: 'Low Demand', classes: 'bg-gray-100 text-gray-600' },
};

const RecommendationCard: React.FC<RecommendationCardProps> = ({ recommendation }) => {
  const {
    crop, profitabilityScore, riskLevel, season,
    confidence, expectedYield, waterRequirement, marketDemand, description,
  } = recommendation;

  const risk = riskConfig[riskLevel];
  const demand = demandConfig[marketDemand];
  const emoji = CROP_EMOJIS[crop] || '🌿';

  return (
    <div className={`${styles.card} bg-white rounded-xl shadow-card p-5 border border-gray-50 hover:shadow-card-hover transition-shadow duration-200`}>
      <div className="flex items-start justify-between mb-3">
        <div className="flex items-center gap-3">
          <span className="text-3xl">{emoji}</span>
          <div>
            <h3 className="text-base font-bold text-gray-900">{crop}</h3>
            <p className="text-xs text-gray-500">{season} Season</p>
          </div>
        </div>
        <span className={`text-xs font-semibold px-2.5 py-1 rounded-full ${risk.classes}`}>
          {risk.label}
        </span>
      </div>

      <div className="mb-4">
        <div className="flex items-center justify-between mb-1.5">
          <span className="text-xs text-gray-500 font-medium">Profitability Score</span>
          <span className="text-sm font-bold text-gray-900">{profitabilityScore}%</span>
        </div>
        <div className="h-2 bg-gray-100 rounded-full overflow-hidden">
          <div
            className={`${styles.progressBar} h-full rounded-full bg-gradient-to-r from-primary-400 to-primary-600`}
            style={{ width: `${profitabilityScore}%` }}
          />
        </div>
      </div>

      <div className="grid grid-cols-2 gap-2 mb-4 text-xs">
        <div className="bg-gray-50 rounded-lg p-2.5">
          <p className="text-gray-400 mb-0.5">Expected Yield</p>
          <p className="font-semibold text-gray-800">{expectedYield} t/ha</p>
        </div>
        <div className="bg-gray-50 rounded-lg p-2.5">
          <p className="text-gray-400 mb-0.5">Water Req.</p>
          <p className="font-semibold text-gray-800">{waterRequirement}</p>
        </div>
        <div className="bg-gray-50 rounded-lg p-2.5">
          <p className="text-gray-400 mb-0.5">Confidence</p>
          <p className="font-semibold text-gray-800">{confidence}%</p>
        </div>
        <div className="bg-gray-50 rounded-lg p-2.5">
          <p className="text-gray-400 mb-0.5">Market</p>
          <span className={`text-xs font-semibold px-1.5 py-0.5 rounded-full ${demand.classes}`}>
            {demand.label}
          </span>
        </div>
      </div>

      {description && (
        <p className="text-xs text-gray-500 mb-4 line-clamp-2">{description}</p>
      )}

      <button className="w-full btn-primary text-sm py-2">
        View Details
      </button>
    </div>
  );
};

export default RecommendationCard;
