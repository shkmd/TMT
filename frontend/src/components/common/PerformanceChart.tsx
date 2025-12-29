import React, { useState } from 'react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

// Sample data for demo - replace with real data from API
const generateData = () => {
  const data = [];
  const startTime = 9.5; // 09:30
  const endTime = 15.5; // 15:30
  const interval = 0.5; // 30 minutes

  for (let time = startTime; time <= endTime; time += interval) {
    const hours = Math.floor(time);
    const minutes = (time % 1) * 60;
    const timeStr = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;

    // Generate random P&L values with upward trend
    const baseValue = (time - startTime) * 500;
    const randomVariation = Math.random() * 500;
    const value = Math.floor(baseValue + randomVariation);

    data.push({
      time: timeStr,
      value: value,
    });
  }

  return data;
};

const data = generateData();

export const PerformanceChart: React.FC = () => {
  const [timeframe, setTimeframe] = useState('Today');

  return (
    <div className="bg-dark-card border border-dark-border rounded-xl p-6">
      {/* Header */}
      <div className="flex items-center justify-between mb-6">
        <h3 className="text-lg font-semibold text-white">Intraday Performance</h3>
        <select
          value={timeframe}
          onChange={(e) => setTimeframe(e.target.value)}
          className="px-4 py-2 bg-dark-surface border border-dark-border rounded-lg text-gray-200 text-sm focus:outline-none focus:ring-2 focus:ring-primary-500/50"
        >
          <option>Today</option>
          <option>Yesterday</option>
          <option>Last 7 Days</option>
          <option>Last 30 Days</option>
        </select>
      </div>

      {/* Chart */}
      <ResponsiveContainer width="100%" height={350}>
        <AreaChart
          data={data}
          margin={{ top: 10, right: 10, left: 0, bottom: 0 }}
        >
          <defs>
            <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
              <stop offset="5%" stopColor="#14b8a6" stopOpacity={0.3} />
              <stop offset="95%" stopColor="#14b8a6" stopOpacity={0} />
            </linearGradient>
          </defs>
          <CartesianGrid strokeDasharray="3 3" stroke="#1e2937" />
          <XAxis
            dataKey="time"
            stroke="#6b7280"
            style={{ fontSize: '12px' }}
            tickLine={false}
          />
          <YAxis
            stroke="#6b7280"
            style={{ fontSize: '12px' }}
            tickLine={false}
            tickFormatter={(value) => `${(value / 1000).toFixed(0)}k`}
          />
          <Tooltip
            contentStyle={{
              backgroundColor: '#151b26',
              border: '1px solid #1e2937',
              borderRadius: '8px',
              color: '#fff',
            }}
            labelStyle={{ color: '#9ca3af' }}
            formatter={(value: number) => [`₹${value.toFixed(0)}`, 'P&L']}
          />
          <Area
            type="monotone"
            dataKey="value"
            stroke="#14b8a6"
            strokeWidth={2}
            fillOpacity={1}
            fill="url(#colorValue)"
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
};
