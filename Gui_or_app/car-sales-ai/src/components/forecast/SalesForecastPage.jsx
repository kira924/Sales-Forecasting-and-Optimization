import React, { useState } from 'react';
import { Download, TrendingUp, AlertCircle } from 'lucide-react';
import Button from '../common/Button';
import Card from '../common/Card';
import LoadingSpinner, { ProgressSpinner } from '../common/LoadingSpinner';
import { useToast } from '../common/Toast';
import TrendChart from './TrendChart';
import SeasonalityChart from './SeasonalityChart';
import MonthlyTable from './MonthlyTable';
import { formatCurrency, formatPercentage, calculateGrowth } from '../../utils/helpers';
import { generateSalesForecast } from '../../services/api';

const SalesForecastPage = () => {
  const { success, error: showError } = useToast();
  const [forecastView, setForecastView] = useState('full'); // 'quick' or 'full'
  const [loading, setLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState(0);
  const [results, setResults] = useState(null);

  const loadingSteps = [
    'Analyzing historical data...',
    'Identifying seasonal patterns...',
    'Running Prophet model...',
    'Generating predictions...',
  ];

  const handleGenerateForecast = async () => {
    setLoading(true);
    setLoadingStep(0);

    try {
      // Simulate step-by-step loading
      for (let i = 0; i < loadingSteps.length; i++) {
        setLoadingStep(i + 1);
        await new Promise(resolve => setTimeout(resolve, 1000));
      }

      // Call API
      const data = await generateSalesForecast();
      setResults(data);
      success('Forecast generated successfully!');
    } catch (err) {
      showError('Failed to generate forecast. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
      setLoadingStep(0);
    }
  };

  const handleExportPDF = () => {
    success('PDF export feature coming soon!');
  };

  const handleExportExcel = () => {
    success('Excel export feature coming soon!');
  };

  const displayMonths = forecastView === 'quick' ? 3 : 12;
  const displayData = results ? {
    ...results,
    monthlyForecast: results.monthlyForecast.slice(0, displayMonths)
  } : null;

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-primary mb-2">
             Sales Forecasting for 2026
          </h1>
          <p className="text-gray-400 text-lg">
            Predict your total sales for the next 12 months
          </p>
        </div>

        {/* Configuration Card */}
        <Card className="mb-8">
          <div className="space-y-6">
            <div>
              <h3 className="text-lg font-semibold text-primary mb-4">
                 Forecast Configuration
              </h3>
              
              {/* Forecast View */}
              <div className="space-y-3">
                <label className="block text-sm font-medium text-gray-500">
                  Forecast View:
                </label>
                <div className="space-y-2">
                  <label className="flex items-center">
                    <input
                      type="radio"
                      name="forecastView"
                      value="quick"
                      checked={forecastView === 'quick'}
                      onChange={(e) => setForecastView(e.target.value)}
                      className="w-4 h-4 text-secondary border-gray-200 focus:ring-secondary"
                    />
                    <span className="ml-2 text-sm text-gray-500">
                      Quick Preview (Next 3 Months)
                    </span>
                  </label>
                  <label className="flex items-center">
                    <input
                      type="radio"
                      name="forecastView"
                      value="full"
                      checked={forecastView === 'full'}
                      onChange={(e) => setForecastView(e.target.value)}
                      className="w-4 h-4 text-secondary border-gray-200 focus:ring-secondary"
                    />
                    <span className="ml-2 text-sm text-gray-500">
                      Full Year Forecast (Next 12 Months) <span className="text-secondary">Recommended</span>
                    </span>
                  </label>
                </div>
              </div>

              {/* Info Note */}
              <div className="mt-4 p-4 bg-secondary bg-opacity-10 rounded-lg flex items-start space-x-3">
                <AlertCircle className="w-5 h-5 text-secondary flex-shrink-0 mt-0.5" />
                <div className="text-sm text-secondary">
                  <strong>Note:</strong> Model automatically generates a 12-month forecast. 
                  Choose "Quick Preview" to see only the first 3 months.
                </div>
              </div>
            </div>

            {/* Generate Button */}
            <Button
              variant="primary"
              size="lg"
              fullWidth
              onClick={handleGenerateForecast}
              loading={loading}
              leftIcon={<TrendingUp className="w-5 h-5" />}
            >
              Generate Forecast
            </Button>
          </div>
        </Card>

        {/* Loading State */}
        {loading && (
          <Card>
            <ProgressSpinner
              steps={loadingSteps}
              currentStep={loadingStep}
              text="Generating Forecast..."
            />
          </Card>
        )}

        {/* Results */}
        {!loading && displayData && (
          <>
            {/* Summary Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
              <div className="stat-card stat-card-primary">
                <p className="text-sm font-medium text-gray-400 mb-1">2026 Total Sales</p>
                <p className="text-3xl font-bold text-primary">
                  {formatCurrency(displayData.totalForecast, 1)}
                </p>
              </div>
              <div className="stat-card stat-card-success">
                <p className="text-sm font-medium text-gray-400 mb-1">Growth Rate</p>
                <p className="text-3xl font-bold text-primary">
                  {formatPercentage(displayData.growthRate)}
                </p>
                <p className="text-sm text-success mt-2">
                 vs 2025
                </p>
              </div>
              <div className="stat-card stat-card-secondary">
                <p className="text-sm font-medium text-gray-400 mb-1">Confidence</p>
                <p className="text-3xl font-bold text-primary">95%</p>
              </div>
              <div className="stat-card stat-card-warning">
                <p className="text-sm font-medium text-gray-400 mb-1">Peak Month</p>
                <p className="text-3xl font-bold text-primary">Nov</p>
                <p className="text-sm text-warning mt-2">
                  {formatCurrency(Math.max(...displayData.monthlyForecast.map(m => m.forecast)), 1)}
                </p>
              </div>
            </div>

            {/* Main Trend Chart */}
            <Card title=" Sales Trend & Forecast" className="mb-8">
              <TrendChart data={displayData} />
            </Card>

            {/* Seasonality Chart */}
            <Card title=" Seasonal Patterns" className="mb-8">
              <SeasonalityChart data={displayData} />
            </Card>

            {/* Monthly Breakdown Table */}
            <Card
              title=" Monthly Forecast Details"
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
              className="mb-8"
            >
              <MonthlyTable data={displayData.monthlyForecast} />
            </Card>

            {/* Recommendations */}
            <Card
              title=" Actionable Insights & Recommendations"
              icon={<TrendingUp className="w-6 h-6" />}
            >
              <div className="space-y-4">
                <div className="p-4 bg-success bg-opacity-10 rounded-lg">
                  <h4 className="font-semibold text-success mb-2">
                     Strong Growth Expected
                  </h4>
                  <p className="text-sm text-gray-500">
                    2025 forecast shows {formatPercentage(displayData.growthRate)} growth compared to 2024
                  </p>
                </div>

                <div className="p-4 bg-secondary bg-opacity-10 rounded-lg">
                  <h4 className="font-semibold text-secondary mb-2">
                     Peak Season Planning
                  </h4>
                  <ul className="text-sm text-gray-500 space-y-1 list-disc list-inside">
                    <li>November-December: Highest sales period</li>
                    <li>Increase inventory in October</li>
                    <li>Staff up for holiday season</li>
                  </ul>
                </div>

                <div className="p-4 bg-warning bg-opacity-10 rounded-lg">
                  <h4 className="font-semibold text-warning mb-2">
                     Low Season Strategy
                  </h4>
                  <ul className="text-sm text-gray-500 space-y-1 list-disc list-inside">
                    <li>June-August: Slower sales expected</li>
                    <li>Plan promotions and clearance events</li>
                    <li>Reduce operating costs during this period</li>
                  </ul>
                </div>

                <div className="p-4 bg-primary bg-opacity-10 rounded-lg">
                  <h4 className="font-semibold text-primary mb-2">
                     Inventory Management
                  </h4>
                  <ul className="text-sm text-gray-500 space-y-1 list-disc list-inside">
                    <li>Stock up 15% more inventory for Q4</li>
                    <li>Focus on popular models (see Priority Ranking)</li>
                  </ul>
                </div>
              </div>
            </Card>
          </>
        )}

        {/* Empty State */}
        {!loading && !results && (
          <Card>
            <div className="text-center py-12">
              <TrendingUp className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-gray-400 mb-2">
                No forecast yet
              </h3>
              <p className="text-gray-400 mb-6">
                Configure your settings above and click "Generate Forecast" to see predictions
              </p>
            </div>
          </Card>
        )}
      </div>
    </div>
  );
};

export default SalesForecastPage;