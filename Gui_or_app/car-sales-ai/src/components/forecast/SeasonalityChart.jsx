import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts';
import { CHART_COLORS } from '../../utils/constants';

const SeasonalityChart = ({ data }) => {
  if (!data || !data.monthlyForecast) return null;

  // Calculate relative strength (compared to average)
  const avgForecast = data.monthlyForecast.reduce((sum, m) => sum + m.forecast, 0) / data.monthlyForecast.length;
  
  const chartData = data.monthlyForecast.map(item => {
    const relativeStrength = ((item.forecast - avgForecast) / avgForecast) * 100;
    return {
      month: item.month.substring(0, 3), // Short month name
      strength: relativeStrength,
      forecast: item.forecast,
    };
  });

  // Color bars based on strength
  const getBarColor = (strength) => {
    if (strength > 5) return CHART_COLORS.success;
    if (strength < -5) return CHART_COLORS.danger;
    return CHART_COLORS.gray;
  };

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const strength = payload[0].value;
      return (
        <div className="bg-white p-3 rounded-lg shadow-lg border border-gray-200">
          <p className="font-semibold text-primary mb-1">{payload[0].payload.month}</p>
          <p className="text-sm">
            <span className={strength > 0 ? 'text-success' : 'text-danger'}>
              {strength > 0 ? '↑' : '↓'} {Math.abs(strength).toFixed(1)}%
            </span>
            {' '}vs average
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="w-full">
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <BarChart data={chartData}>
            <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
            <XAxis 
              dataKey="month"
              stroke="#7F8C8D"
              style={{ fontSize: '12px' }}
            />
            <YAxis 
              stroke="#7F8C8D"
              style={{ fontSize: '12px' }}
              tickFormatter={(value) => `${value > 0 ? '+' : ''}${value}%`}
            />
            <Tooltip content={<CustomTooltip />} />
            <Bar dataKey="strength" radius={[8, 8, 0, 0]}>
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={getBarColor(entry.strength)} />
              ))}
            </Bar>
          </BarChart>
        </ResponsiveContainer>
      </div>

      {/* Legend */}
      <div className="mt-6 grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
        <div className="flex items-center space-x-2">
          <div className="w-4 h-4 rounded bg-success"></div>
          <div>
            <p className="font-medium text-gray-500"> Peak Months</p>
            <p className="text-xs text-gray-400">March, November, December</p>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-4 h-4 rounded bg-gray-400"></div>
          <div>
            <p className="font-medium text-gray-500"> Average Months</p>
            <p className="text-xs text-gray-400">January, April, May, October</p>
          </div>
        </div>
        <div className="flex items-center space-x-2">
          <div className="w-4 h-4 rounded bg-danger"></div>
          <div>
            <p className="font-medium text-gray-500"> Low Months</p>
            <p className="text-xs text-gray-400">June, July, August</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SeasonalityChart;