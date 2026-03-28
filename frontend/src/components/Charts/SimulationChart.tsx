import React from 'react';
import {
  ComposedChart, Bar, Line, XAxis, YAxis, CartesianGrid,
  Tooltip, Legend, ResponsiveContainer,
} from 'recharts';
import { SimulationScenario } from '../../types';

interface SimulationChartProps {
  scenarios: SimulationScenario[];
  crop?: string;
}

const SimulationChart: React.FC<SimulationChartProps> = ({ scenarios, crop }) => {
  return (
    <div className="bg-white rounded-xl shadow-card p-6">
      <div className="mb-5">
        <h3 className="text-base font-bold text-gray-900">
          {crop ? `${crop} Simulation Scenarios` : 'Simulation Scenarios'}
        </h3>
        <p className="text-xs text-gray-500 mt-0.5">Revenue, cost and profit by scenario</p>
      </div>
      <ResponsiveContainer width="100%" height={280}>
        <ComposedChart data={scenarios} margin={{ top: 5, right: 20, left: 0, bottom: 5 }}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" vertical={false} />
          <XAxis
            dataKey="name"
            tick={{ fontSize: 11, fill: '#9ca3af' }}
            tickLine={false}
            axisLine={{ stroke: '#f0f0f0' }}
          />
          <YAxis
            tick={{ fontSize: 11, fill: '#9ca3af' }}
            tickLine={false}
            axisLine={false}
            tickFormatter={(v) => `$${(v / 1000).toFixed(0)}k`}
            width={55}
          />
          <Tooltip
            formatter={(value: number) => [`$${value.toLocaleString()}`, '']}
            contentStyle={{ borderRadius: '12px', border: '1px solid #f0f0f0', fontSize: '12px' }}
          />
          <Legend iconType="circle" iconSize={8} wrapperStyle={{ fontSize: '12px', paddingTop: '12px' }} />
          <Bar dataKey="revenue" name="Revenue" fill="#34D399" radius={[4, 4, 0, 0]} maxBarSize={40} />
          <Bar dataKey="cost" name="Cost" fill="#FCA5A5" radius={[4, 4, 0, 0]} maxBarSize={40} />
          <Line
            type="monotone"
            dataKey="profit"
            name="Profit"
            stroke="#059669"
            strokeWidth={2.5}
            dot={{ r: 5, fill: '#059669' }}
          />
        </ComposedChart>
      </ResponsiveContainer>
    </div>
  );
};

export default SimulationChart;
