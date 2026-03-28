import React, { useState, useMemo } from 'react';
import RecommendationCard from '../components/Cards/RecommendationCard';
import CropRecommendationChart from '../components/Charts/CropRecommendationChart';
import { CropRecommendation } from '../types';

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
    description: 'Strong global demand and favorable weather make wheat an excellent winter crop.',
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
    description: 'Strong ethanol and feed market demand. Requires adequate irrigation planning.',
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
    description: 'Low water requirement and nitrogen-fixing properties improve soil health.',
  },
  {
    id: 'r4',
    crop: 'Rice',
    profitabilityScore: 65,
    riskLevel: 'medium',
    season: 'Monsoon',
    confidence: 75,
    expectedYield: 5.5,
    waterRequirement: 'Very High',
    marketDemand: 'high',
    description: 'Staple crop with guaranteed demand. Water availability is critical.',
  },
  {
    id: 'r5',
    crop: 'Tomato',
    profitabilityScore: 81,
    riskLevel: 'high',
    season: 'Spring',
    confidence: 70,
    expectedYield: 35.0,
    waterRequirement: 'Medium',
    marketDemand: 'high',
    description: 'High profitability with premium market prices. Requires careful pest management.',
  },
  {
    id: 'r6',
    crop: 'Cotton',
    profitabilityScore: 58,
    riskLevel: 'high',
    season: 'Summer',
    confidence: 68,
    expectedYield: 1.8,
    waterRequirement: 'High',
    marketDemand: 'medium',
    description: 'Global cotton prices volatile. Best for farmers with established supply chains.',
  },
];

type Season = 'All' | 'Winter' | 'Summer' | 'Spring' | 'Monsoon';
type RiskFilter = 'All' | 'low' | 'medium' | 'high';

const Recommendations: React.FC = () => {
  const [seasonFilter, setSeasonFilter] = useState<Season>('All');
  const [riskFilter, setRiskFilter] = useState<RiskFilter>('All');

  const filtered = useMemo(() => {
    return MOCK_RECOMMENDATIONS.filter(r => {
      const matchSeason = seasonFilter === 'All' || r.season === seasonFilter;
      const matchRisk = riskFilter === 'All' || r.riskLevel === riskFilter;
      return matchSeason && matchRisk;
    });
  }, [seasonFilter, riskFilter]);

  const chartData = MOCK_RECOMMENDATIONS.map(r => ({
    crop: r.crop,
    profitability: r.profitabilityScore,
    risk: r.riskLevel === 'high' ? 75 : r.riskLevel === 'medium' ? 45 : 20,
  }));

  const avgScore = Math.round(filtered.reduce((s, r) => s + r.profitabilityScore, 0) / (filtered.length || 1));
  const lowRiskCount = filtered.filter(r => r.riskLevel === 'low').length;

  return (
    <div className="space-y-6">
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Crop Recommendations</h1>
          <p className="text-sm text-gray-500 mt-1">AI-driven crop suggestions for your farm</p>
        </div>
      </div>

      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4">
        <div className="bg-white rounded-xl shadow-card p-5">
          <p className="text-xs text-gray-500 font-medium mb-1">Total Recommendations</p>
          <p className="text-3xl font-bold text-gray-900">{filtered.length}</p>
        </div>
        <div className="bg-white rounded-xl shadow-card p-5">
          <p className="text-xs text-gray-500 font-medium mb-1">Avg. Profitability Score</p>
          <p className="text-3xl font-bold text-emerald-600">{avgScore}%</p>
        </div>
        <div className="bg-white rounded-xl shadow-card p-5">
          <p className="text-xs text-gray-500 font-medium mb-1">Low Risk Options</p>
          <p className="text-3xl font-bold text-gray-900">{lowRiskCount}</p>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-card p-5">
        <div className="flex flex-wrap gap-3 items-center">
          <span className="text-sm font-semibold text-gray-700">Filter by:</span>
          <div className="flex flex-wrap gap-2">
            {(['All', 'Winter', 'Summer', 'Spring', 'Monsoon'] as Season[]).map(s => (
              <button
                key={s}
                onClick={() => setSeasonFilter(s)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                  seasonFilter === s
                    ? 'bg-primary-500 text-white'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                {s}
              </button>
            ))}
          </div>
          <div className="w-px h-5 bg-gray-200 hidden sm:block" />
          <div className="flex flex-wrap gap-2">
            {(['All', 'low', 'medium', 'high'] as RiskFilter[]).map(r => (
              <button
                key={r}
                onClick={() => setRiskFilter(r)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium capitalize transition-colors ${
                  riskFilter === r
                    ? 'bg-primary-500 text-white'
                    : 'bg-gray-100 text-gray-600 hover:bg-gray-200'
                }`}
              >
                {r === 'All' ? 'All Risk' : `${r} risk`}
              </button>
            ))}
          </div>
        </div>
      </div>

      {filtered.length === 0 ? (
        <div className="bg-white rounded-xl shadow-card p-12 text-center">
          <div className="text-4xl mb-3">🌿</div>
          <p className="text-gray-500 font-medium">No recommendations match your filters</p>
          <button
            onClick={() => { setSeasonFilter('All'); setRiskFilter('All'); }}
            className="btn-primary mt-4 text-sm"
          >
            Clear Filters
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-3 gap-5">
          {filtered.map(rec => (
            <RecommendationCard key={rec.id} recommendation={rec} />
          ))}
        </div>
      )}

      <CropRecommendationChart data={chartData} />
    </div>
  );
};

export default Recommendations;
