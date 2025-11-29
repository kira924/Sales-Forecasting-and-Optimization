import React from 'react';
// 1. ⚠️ قم بتغيير الاستيراد هنا: استبدل AreaChart بـ ComposedChart
import { ComposedChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, Area } from 'recharts';
import { formatCurrency } from '../../utils/helpers';
import { CHART_COLORS } from '../../utils/constants';

const billion = 1000000000;

const TrendChart = ({ data }) => {
  if (!data || !data.monthlyForecast) return null;

  // Prepare chart data
  const chartData = data.monthlyForecast.map((item) => {
    const forecastValue = (Number(item.forecast) || 0) / billion;
    const lowerValue = (Number(item.lower_bound) || 0) / billion; 
    const upperBoundValue = (Number(item.upper_bound) || 0) / billion; 

    return ({
      month: item.month,
      forecast: forecastValue,
      lower: lowerValue,
      upper: upperBoundValue,
    });
  });

  // Custom tooltip
  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      return (
        <div className="bg-white p-4 rounded-lg shadow-lg border border-gray-200">
          <p className="font-semibold text-primary mb-2">{payload[0].payload.month}</p>
          <div className="space-y-1 text-sm">
            <p className="text-secondary">
              <strong>Forecast:</strong> ${payload[0].value.toFixed(2)}M
            </p>
            <p className="text-gray-400">
              <strong>Upper (95%):</strong> ${payload.find(p => p.dataKey === 'upper')?.value.toFixed(2)}M
            </p>
            <p className="text-gray-400">
              <strong>Lower (95%):</strong> ${payload.find(p => p.dataKey === 'lower')?.value.toFixed(2)}M
            </p>
          </div>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="w-full h-96">
      <ResponsiveContainer width="100%" height="100%">
        <ComposedChart data={chartData}>
          <CartesianGrid strokeDasharray="3 3" stroke="#f0f0f0" />
          <XAxis 
            dataKey="month" 
            stroke="#7F8C8D"
            style={{ fontSize: '12px' }}
          />
          <YAxis 
            stroke="#7F8C8D"
            style={{ fontSize: '12px' }}
            tickFormatter={(value) => `$${value.toFixed(1)}M`}
          />
          <Tooltip content={<CustomTooltip />} />
          <Legend 
            wrapperStyle={{ fontSize: '14px' }}
            iconType="line"
          />
          
          <Area
            type="monotone"
            dataKey="upper"
            stroke="none"
            fill={CHART_COLORS.lightBlue}
            fillOpacity={0.3}
            name="Upper Bound"
          />
          <Area
            type="monotone"
            dataKey="lower"
            stroke="none"
            fill={CHART_COLORS.lightBlue} 
            fillOpacity={0.1}
            name="Lower Bound Area"
          />
          
          <Line
            type="monotone"
            dataKey="lower"
            stroke="#000000" 
            strokeWidth={1}
            dot={false}
            activeDot={false}
            name="Lower Bound" 
          />

          <Line
            type="monotone"
            dataKey="forecast"
            stroke={CHART_COLORS.primary}
            strokeWidth={2}
            dot={false}
            activeDot={{ r: 6 }}
            name="Forecast"
          />
        </ComposedChart>
      </ResponsiveContainer>
      
    </div>
  );
};

export default TrendChart;