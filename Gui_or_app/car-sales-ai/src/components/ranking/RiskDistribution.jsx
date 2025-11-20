import React from 'react';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';
import { CHART_COLORS } from '../../utils/constants';

const RiskDistribution = ({ data }) => {
  if (!data || data.length === 0) return null;

  // Calculate risk distribution
  const riskCounts = data.reduce((acc, car) => {
    acc[car.risk] = (acc[car.risk] || 0) + 1;
    return acc;
  }, {});

  const chartData = [
    { name: ' Low Risk', value: riskCounts.LOW || 0, color: CHART_COLORS.success },
    { name: ' Medium Risk', value: riskCounts.MEDIUM || 0, color: CHART_COLORS.warning },
    { name: ' High Risk', value: riskCounts.HIGH || 0, color: CHART_COLORS.danger },
  ].filter(item => item.value > 0);

  const total = chartData.reduce((sum, item) => sum + item.value, 0);

  const CustomTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const percent = ((payload[0].value / total) * 100).toFixed(0);
      return (
        <div className="bg-white p-3 rounded-lg shadow-lg border border-gray-200">
          <p className="font-semibold text-primary">{payload[0].name}</p>
          <p className="text-sm text-gray-500">
            {payload[0].value} cars ({percent}%)
          </p>
        </div>
      );
    }
    return null;
  };

  return (
    <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 items-center">
      {/* Chart */}
      <div className="h-80">
        <ResponsiveContainer width="100%" height="100%">
          <PieChart>
            <Pie
              data={chartData}
              cx="50%"
              cy="50%"
              labelLine={false}
              label={({ name, percent }) => `${(percent * 100).toFixed(0)}%`}
              outerRadius={100}
              fill="#8884d8"
              dataKey="value"
            >
              {chartData.map((entry, index) => (
                <Cell key={`cell-${index}`} fill={entry.color} />
              ))}
            </Pie>
            <Tooltip content={<CustomTooltip />} />
          </PieChart>
        </ResponsiveContainer>
      </div>

      {/* Legend & Stats */}
      <div className="space-y-4">
        {chartData.map((item, index) => {
          const percent = ((item.value / total) * 100).toFixed(0);
          const totalProfit = data
            .filter(car => {
              if (item.name.includes('Low')) return car.risk === 'LOW';
              if (item.name.includes('Medium')) return car.risk === 'MEDIUM';
              if (item.name.includes('High')) return car.risk === 'HIGH';
              return false;
            })
            .reduce((sum, car) => sum + car.profit, 0);

          return (
            <div key={index} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <div 
                  className="w-4 h-4 rounded"
                  style={{ backgroundColor: item.color }}
                />
                <div>
                  <p className="font-semibold text-primary">{item.name}</p>
                  <p className="text-sm text-gray-400">
                    {item.value} cars ({percent}%)
                  </p>
                </div>
              </div>
              <div className="text-right">
                <p className="font-semibold text-primary">
                  ${totalProfit.toLocaleString()}
                </p>
                <p className="text-xs text-gray-400">Total profit</p>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};

export default RiskDistribution;