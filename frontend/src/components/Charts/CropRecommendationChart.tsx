import React from 'react';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid,
  Tooltip, ResponsiveContainer, Cell,
} from 'recharts';

interface CropData {
  crop: string;
  profitability: number;
  risk: number;
}

interface CropRecommendationChartProps {
  data: CropData[];
}

const COLORS = ['#10B981', '#059669', '#34D399', '#6EE7B7', '#047857', '#065F46'];

const CropRecommendationChart: React.FC<CropRecommendationChartProps> = ({ data }) => {
  const sorted = [...data].sort((a, b) => b.profitability - a.profitability);

  return (
    <div className="bg-white rounded-xl shadow-card p-6">
      <div className="mb-5">
        <h3 className="text-base font-bold text-gray-900">Crop Profitability Comparison</h3>
        <p className="text-xs text-gray-500 mt-0.5">Profitability score by crop</p>
      </div>
      <ResponsiveContainer width="100%" height={260}>
        <BarChart
          data={sorted}
          layout="vertical"
          margin={{ top: 5, right: 20, left: 10, bottom: 5 }}
        >
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" horizontal={false} />
          <XAxis
            type="number"
            domain={[0, 100]}
            tick={{ fontSize: 11, fill: '#9ca3af' }}
            tickLine={false}
            axisLine={{ stroke: '#f0f0f0' }}
          />
          <YAxis
            dataKey="crop"
            type="category"
            tick={{ fontSize: 12, fill: '#374151' }}
            tickLine={false}
            axisLine={false}
            width={70}
          />
          <Tooltip
            formatter={(value: number) => [`${value}%`, 'Profitability']}
            contentStyle={{ borderRadius: '12px', border: '1px solid #f0f0f0', fontSize: '12px' }}
          />
          <Bar dataKey="profitability" radius={[0, 6, 6, 0]} maxBarSize={28}>
            {sorted.map((_, index) => (
              <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
            ))}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
};

export default CropRecommendationChart;
