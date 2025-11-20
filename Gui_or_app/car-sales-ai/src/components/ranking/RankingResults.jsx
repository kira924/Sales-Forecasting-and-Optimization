import React from 'react';
import { Download } from 'lucide-react';
import Card from '../common/Card';
import Button from '../common/Button';
import { useToast } from '../common/Toast';
import RankingTable from './RankingTable';
import RiskDistribution from './RiskDistribution';
import Recommendations from './Recommendations';
import { formatCurrency, formatPercentage } from '../../utils/helpers';

const RankingResults = ({ data, profitMargin }) => {
  const { success } = useToast();

  if (!data) return null;

  const handleExportPDF = () => {
    success('PDF export feature coming soon!');
  };

  const handleExportExcel = () => {
    success('Excel export feature coming soon!');
  };

  // Apply profit margin if set
  const adjustedData = {
    ...data,
    rankings: data.rankings.map(car => ({
      ...car,
      profit: profitMargin ? car.profit * profitMargin : car.profit,
    })),
  };

  const totalProfit = adjustedData.rankings.reduce((sum, car) => sum + car.profit, 0);
  const avgProfit = totalProfit / adjustedData.rankings.length;
  const bestCar = adjustedData.rankings[0];

  // Risk distribution
  const riskCounts = adjustedData.rankings.reduce((acc, car) => {
    acc[car.risk] = (acc[car.risk] || 0) + 1;
    return acc;
  }, {});

  return (
    <div className="space-y-8">
      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
        <div className="stat-card stat-card-primary">
          <p className="text-sm font-medium text-gray-400 mb-1">Total Expected Profit</p>
          <p className="text-3xl font-bold text-primary">
            {formatCurrency(totalProfit)}
          </p>
        </div>
        <div className="stat-card stat-card-success">
          <p className="text-sm font-medium text-gray-400 mb-1">Avg Profit per Car</p>
          <p className="text-3xl font-bold text-primary">
            {formatCurrency(avgProfit)}
          </p>
        </div>
        <div className="stat-card stat-card-warning">
          <p className="text-sm font-medium text-gray-400 mb-1">Best Pick</p>
          <p className="text-2xl font-bold text-primary">
            {bestCar.make}
          </p>
          <p className="text-sm text-gray-400 mt-1">{bestCar.model}</p>
        </div>
        <div className="stat-card stat-card-secondary">
          <p className="text-sm font-medium text-gray-400 mb-1">Cars Analyzed</p>
          <p className="text-3xl font-bold text-primary">
            {adjustedData.rankings.length}
          </p>
        </div>
      </div>

      {/* Risk Distribution */}
      <Card title=" Risk Distribution">
        <RiskDistribution data={adjustedData.rankings} />
      </Card>

      {/* Priority Ranking Table */}
      <Card
        title=" Priority Ranking Results"
        headerAction={
          <div className="flex items-center space-x-2">
            <Button
              variant="secondary"
              size="sm"
              leftIcon={<Download className="w-4 h-4" />}
              onClick={handleExportExcel}
            >
              Excel
            </Button>
            <Button
              variant="secondary"
              size="sm"
              leftIcon={<Download className="w-4 h-4" />}
              onClick={handleExportPDF}
            >
              PDF
            </Button>
          </div>
        }
      >
        <RankingTable data={adjustedData.rankings} />
      </Card>

      {/* Summary Statistics */}
      <Card title=" Summary Statistics">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div>
            <h4 className="font-semibold text-primary mb-3">Profit Analysis</h4>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between">
                <span className="text-gray-400">Total Expected Profit:</span>
                <span className="font-semibold text-primary">{formatCurrency(totalProfit)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Average Profit per Car:</span>
                <span className="font-semibold text-primary">{formatCurrency(avgProfit)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Highest Profit:</span>
                <span className="font-semibold text-success">
                  {formatCurrency(bestCar.profit)} ({bestCar.make} {bestCar.model})
                </span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-400">Lowest Profit:</span>
                <span className="font-semibold text-danger">
                  {formatCurrency(adjustedData.rankings[adjustedData.rankings.length - 1].profit)}
                </span>
              </div>
            </div>
          </div>

          <div>
            <h4 className="font-semibold text-primary mb-3">Risk Distribution</h4>
            <div className="space-y-2 text-sm">
              <div className="flex justify-between items-center">
                <span className="text-gray-400"> Low Risk:</span>
                <span className="font-semibold text-success">
                  {riskCounts.LOW || 0} cars ({formatPercentage(((riskCounts.LOW || 0) / adjustedData.rankings.length) * 100, 0)})
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-400"> Medium Risk:</span>
                <span className="font-semibold text-warning">
                  {riskCounts.MEDIUM || 0} cars ({formatPercentage(((riskCounts.MEDIUM || 0) / adjustedData.rankings.length) * 100, 0)})
                </span>
              </div>
              <div className="flex justify-between items-center">
                <span className="text-gray-400"> High Risk:</span>
                <span className="font-semibold text-danger">
                  {riskCounts.HIGH || 0} cars ({formatPercentage(((riskCounts.HIGH || 0) / adjustedData.rankings.length) * 100, 0)})
                </span>
              </div>
              <div className="flex justify-between items-center pt-2 border-t border-gray-100">
                <span className="text-gray-400">Average Confidence:</span>
                <span className="font-semibold text-primary">
                  {formatPercentage(adjustedData.rankings.reduce((sum, car) => sum + car.confidence, 0) / adjustedData.rankings.length, 1)}
                </span>
              </div>
            </div>
          </div>
        </div>
      </Card>

      {/* Recommendations */}
      <Recommendations data={adjustedData.rankings} />
    </div>
  );
};

export default RankingResults;