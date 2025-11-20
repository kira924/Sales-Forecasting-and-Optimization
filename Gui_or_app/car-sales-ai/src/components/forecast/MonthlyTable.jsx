import React from 'react';
import { formatCurrency, formatPercentage } from '../../utils/helpers';
import { TrendingUp, TrendingDown, Minus } from 'lucide-react';

const MonthlyTable = ({ data }) => {
  if (!data || data.length === 0) return null;

  // Calculate month-over-month change
  const dataWithChange = data.map((item, index) => {
    if (index === 0) {
      return { ...item, change: 0, changePercent: 0 };
    }
    const prevForecast = data[index - 1].forecast;
    const change = item.forecast - prevForecast;
    const changePercent = (change / prevForecast) * 100;
    return { ...item, change, changePercent };
  });

  const getChangeIcon = (change) => {
    if (change > 0) return <TrendingUp className="w-4 h-4 text-success" />;
    if (change < 0) return <TrendingDown className="w-4 h-4 text-danger" />;
    return <Minus className="w-4 h-4 text-gray-400" />;
  };

  const getChangeColor = (change) => {
    if (change > 0) return 'text-success';
    if (change < 0) return 'text-danger';
    return 'text-gray-400';
  };

  return (
    <div className="overflow-x-auto">
      <table className="w-full text-sm">
        <thead>
          <tr className="border-b-2 border-gray-200">
            <th className="text-left py-3 px-4 font-semibold text-gray-500">Month</th>
            <th className="text-right py-3 px-4 font-semibold text-gray-500">Expected</th>
            <th className="text-right py-3 px-4 font-semibold text-gray-500">Lower (95%)</th>
            <th className="text-right py-3 px-4 font-semibold text-gray-500">Upper (95%)</th>
            <th className="text-right py-3 px-4 font-semibold text-gray-500">Change</th>
          </tr>
        </thead>
        <tbody>
          {dataWithChange.map((row, index) => (
            <tr 
              key={index} 
              className="border-b border-gray-100 hover:bg-gray-50 transition-colors"
            >
              <td className="py-3 px-4">
                <span className="font-medium text-primary">{row.month}</span>
              </td>
              <td className="py-3 px-4 text-right font-mono font-semibold text-primary">
                {formatCurrency(row.forecast)}
              </td>
              <td className="py-3 px-4 text-right font-mono text-gray-400">
                {formatCurrency(row.lowerBound)}
              </td>
              <td className="py-3 px-4 text-right font-mono text-gray-400">
                {formatCurrency(row.upperBound)}
              </td>
              <td className="py-3 px-4 text-right">
                <div className="flex items-center justify-end space-x-2">
                  {getChangeIcon(row.changePercent)}
                  <span className={`font-semibold ${getChangeColor(row.changePercent)}`}>
                    {index === 0 ? '-' : formatPercentage(Math.abs(row.changePercent), 1)}
                  </span>
                </div>
              </td>
            </tr>
          ))}
        </tbody>
        <tfoot>
          <tr className="border-t-2 border-gray-200 font-semibold bg-gray-50">
            <td className="py-3 px-4 text-primary">Total</td>
            <td className="py-3 px-4 text-right font-mono text-primary">
              {formatCurrency(data.reduce((sum, row) => sum + row.forecast, 0))}
            </td>
            <td className="py-3 px-4 text-right font-mono text-gray-400">
              {formatCurrency(data.reduce((sum, row) => sum + row.lowerBound, 0))}
            </td>
            <td className="py-3 px-4 text-right font-mono text-gray-400">
              {formatCurrency(data.reduce((sum, row) => sum + row.upperBound, 0))}
            </td>
            <td className="py-3 px-4"></td>
          </tr>
        </tfoot>
      </table>

      <div className="mt-4 text-xs text-gray-400 italic">
        💡 Hover over any row for detailed insights
      </div>
    </div>
  );
};

export default MonthlyTable;