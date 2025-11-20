import React from 'react';
import { TrendingUp, AlertTriangle, XCircle, Target } from 'lucide-react';
import Card from '../common/Card';
import { formatCurrency } from '../../utils/helpers';

const Recommendations = ({ data }) => {
  if (!data || data.length === 0) return null;

  const lowRiskCars = data.filter(car => car.risk === 'LOW');
  const mediumRiskCars = data.filter(car => car.risk === 'MEDIUM');
  const highRiskCars = data.filter(car => car.risk === 'HIGH');

  const lowRiskProfit = lowRiskCars.reduce((sum, car) => sum + car.profit, 0);
  const mediumRiskProfit = mediumRiskCars.reduce((sum, car) => sum + car.profit, 0);
  const totalProfit = data.reduce((sum, car) => sum + car.profit, 0);

  const lowRiskPercent = ((lowRiskProfit / totalProfit) * 100).toFixed(0);

  return (
    <Card
      title=" Smart Investment Recommendations"
      icon={<Target className="w-6 h-6" />}
    >
      <div className="space-y-6">
        {/* Recommended Strategy */}
        {lowRiskCars.length > 0 && (
          <div className="p-4 bg-success bg-opacity-10 rounded-lg border-l-4 border-success">
            <div className="flex items-start space-x-3">
              <TrendingUp className="w-6 h-6 text-success flex-shrink-0 mt-1" />
              <div className="flex-1">
                <h4 className="font-semibold text-success mb-2">
                   RECOMMENDED STRATEGY:
                </h4>
                <p className="text-sm text-gray-500 mb-3">
                  Focus on Low-Risk Vehicles ({lowRiskCars.length} cars):
                </p>
                <div className="space-y-1 text-sm">
                  {lowRiskCars.slice(0, 5).map((car, index) => (
                    <div key={index} className="flex justify-between items-center">
                      <span className="text-gray-500">
                        {index + 1}. {car.make} {car.model}
                      </span>
                      <span className="font-semibold text-success">
                        {formatCurrency(car.profit)} - {car.confidence}% conf
                      </span>
                    </div>
                  ))}
                </div>
                <div className="mt-3 pt-3 border-t border-success border-opacity-30">
                  <div className="flex justify-between items-center">
                    <span className="text-sm font-semibold text-gray-500">Expected Safe Profit:</span>
                    <span className="text-lg font-bold text-success">{formatCurrency(lowRiskProfit)}</span>
                  </div>
                  <p className="text-xs text-gray-400 mt-1">
                    ({lowRiskPercent}% of total potential profit)
                  </p>
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Medium Risk */}
        {mediumRiskCars.length > 0 && (
          <div className="p-4 bg-warning bg-opacity-10 rounded-lg border-l-4 border-warning">
            <div className="flex items-start space-x-3">
              <AlertTriangle className="w-6 h-6 text-warning flex-shrink-0 mt-1" />
              <div className="flex-1">
                <h4 className="font-semibold text-warning mb-2">
                   CONSIDER WITH CAUTION:
                </h4>
                <p className="text-sm text-gray-500 mb-2">
                  Medium-Risk Vehicles ({mediumRiskCars.length} cars):
                </p>
                <ul className="text-sm text-gray-500 space-y-1 list-disc list-inside">
                  <li>Moderate profit potential ({formatCurrency(mediumRiskProfit)} total)</li>
                  <li>Lower confidence ({mediumRiskCars[0]?.confidence}% average)</li>
                  <li>Suitable for portfolio diversification</li>
                </ul>
              </div>
            </div>
          </div>
        )}

        {/* High Risk */}
        {highRiskCars.length > 0 && (
          <div className="p-4 bg-danger bg-opacity-10 rounded-lg border-l-4 border-danger">
            <div className="flex items-start space-x-3">
              <XCircle className="w-6 h-6 text-danger flex-shrink-0 mt-1" />
              <div className="flex-1">
                <h4 className="font-semibold text-danger mb-2">
                   AVOID OR MONITOR CLOSELY:
                </h4>
                <p className="text-sm text-gray-500 mb-2">
                  High-Risk Vehicles ({highRiskCars.length} cars):
                </p>
                <ul className="text-sm text-gray-500 space-y-1 list-disc list-inside">
                  {highRiskCars.map((car, index) => (
                    <li key={index}>
                      {car.make} {car.model} - Very low confidence ({car.confidence}%)
                    </li>
                  ))}
                  <li>Only purchase if you have specific market demand</li>
                </ul>
              </div>
            </div>
          </div>
        )}

        {/* Portfolio Suggestion */}
        <div className="p-4 bg-secondary bg-opacity-10 rounded-lg border-l-4 border-secondary">
          <div className="flex items-start space-x-3">
            <Target className="w-6 h-6 text-secondary flex-shrink-0 mt-1" />
            <div className="flex-1">
              <h4 className="font-semibold text-secondary mb-2">
                 PORTFOLIO SUGGESTION:
              </h4>
              <p className="text-sm text-gray-500 mb-2">Balanced Approach:</p>
              <div className="grid grid-cols-3 gap-4 text-sm">
                <div className="text-center">
                  <div className="text-2xl font-bold text-success mb-1">70%</div>
                  <div className="text-xs text-gray-400">Low Risk</div>
                  <div className="text-xs text-gray-500">{lowRiskCars.length} units</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-warning mb-1">25%</div>
                  <div className="text-xs text-gray-400">Medium Risk</div>
                  <div className="text-xs text-gray-500">{Math.ceil(mediumRiskCars.length * 0.6)} units</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-danger mb-1">5%</div>
                  <div className="text-xs text-gray-400">High Risk</div>
                  <div className="text-xs text-gray-500">1 unit max</div>
                </div>
              </div>
              <p className="text-xs text-gray-400 mt-3 italic">
                Expected ROI: 12-15% with controlled risk
              </p>
            </div>
          </div>
        </div>
      </div>
    </Card>
  );
};

export default Recommendations;