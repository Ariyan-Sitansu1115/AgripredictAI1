import React from 'react';
import {
  RadarChart, Radar, PolarGrid, PolarAngleAxis,
  PolarRadiusAxis, ResponsiveContainer, Tooltip,
} from 'recharts';
import { RiskDimension } from '../../types';

interface RiskAnalysisChartProps {
  data: RiskDimension[];
}

const RiskAnalysisChart: React.FC<RiskAnalysisChartProps> = ({ data }) => {
  return (
    <div className="bg-white rounded-xl shadow-card p-6">
      <div className="mb-5">
        <h3 className="text-base font-bold text-gray-900">Risk Analysis</h3>
        <p className="text-xs text-gray-500 mt-0.5">Multi-dimensional risk assessment</p>
      </div>
      <ResponsiveContainer width="100%" height={260}>
        <RadarChart data={data} margin={{ top: 10, right: 30, left: 30, bottom: 10 }}>
          <PolarGrid stroke="#f0f0f0" />
          <PolarAngleAxis
            dataKey="metric"
            tick={{ fontSize: 11, fill: '#6b7280' }}
          />
          <PolarRadiusAxis
            angle={90}
            domain={[0, 100]}
            tick={{ fontSize: 9, fill: '#9ca3af' }}
          />
          <Tooltip
            formatter={(value: number) => [`${value}`, 'Score']}
            contentStyle={{ borderRadius: '12px', border: '1px solid #f0f0f0', fontSize: '12px' }}
          />
          <Radar
            name="Risk"
            dataKey="value"
            stroke="#10B981"
            fill="#10B981"
            fillOpacity={0.2}
            strokeWidth={2}
          />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default RiskAnalysisChart;
