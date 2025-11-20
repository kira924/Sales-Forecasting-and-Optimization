import React from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Area, AreaChart } from 'recharts';
import { formatCurrency } from '../../utils/helpers';
import { CHART_COLORS } from '../../utils/constants';

const TrendChart = ({ data }) => {
  if (!data || !data.monthlyForecast) return null;

  // Prepare chart data
  const chartData = data.monthlyForecast.map((item, index) => ({
    month: item.month,
    forecast: item.forecast,
    lower: item.lowerBound,
    upper: item.upperBound,
  }));

  // Custom tooltip
  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-4 rounded-lg shadow-lg border border-gray-200">
          <p className="font-semibold text-primary mb-2">{payload[0].payload.month}</p>
          <div className="space-y-1 text-sm">
            <p className="text-secondary">
              <strong>Forecast:</strong> {formatCurrency(payload[0].value)}
            </p>
            {payload[1] && (
              <p className="text-gray-400">
                <strong>Lower (95%):</strong> {formatCurrency(payload[1].value)}
              </p>
            )}
            {payload[2] && (
              <p className="text-gray-400">
                <strong>Upper (95%):</strong> {formatCurrency(payload[2].value)}
              </p>
            )}
          </div>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="w-full h-96">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis 
            dataKey="month" 
            stroke="#7F8C8D"
            style={{ fontSize: '12px' }}
          />
          <YAxis 
            stroke="#7F8C8D"
            style={{ fontSize: '12px' }}
            tickFormatter={(value) => `$${(value / 1000000).toFixed(1)}M`}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend 
            wrapperStyle={{ fontSize: '14px' }}
            iconType="line"
          />
          
          {/* Confidence Interval (shaded area) */}
          <Area
            type="monotone"
            dataKey="upper"
            stackId="1"
            stroke="none"
            fill={CHART_COLORS.lightBlue}
            fillOpacity={0.3}
            name="Upper Bound"
          />
          <Area
            type="monotone"
            dataKey="lower"
            stackId="1"
            stroke="none"
            fill={CHART_COLORS.lightBlue}
            fillOpacity={0.3}
            name="Lower Bound"
          />
          
          {/* Main Forecast Line */}
          <Line
            type="monotone"
            dataKey="forecast"
            stroke={CHART_COLORS.primary}
            strokeWidth={3}
            dot={{ fill: CHART_COLORS.primary, r: 4 }}
            activeDot={{ r: 6 }}
            name="Forecast"
          />
        </AreaChart>
      </ResponsiveContainer>
      
      {/* Legend */}
      <div className="mt-4 flex items-center justify-center space-x-6 text-sm text-gray-400">
        <div className="flex items-center">
          <div className="w-8 h-0.5 bg-primary mr-2"></div>
          <span>Forecast</span>
        </div>
        <div className="flex items-center">
          <div className="w-8 h-3 bg-secondary bg-opacity-30 mr-2"></div>
          <span>95% Confidence Interval</span>
        </div>
      </div>
    </div>
  );
};

export default TrendChart;