import React from 'react';
import { useNavigate } from 'react-router-dom';
import { TrendingUp, Award, BarChart3, Target, ArrowRight, CheckCircle } from 'lucide-react';
import Button from '../common/Button';
import { StatCard } from '../common/Card';
import { formatCurrency } from '../../utils/helpers';

const HomePage = () => {
  const navigate = useNavigate();

  const stats = [
    {
      title: '2025 Sales Forecast',
      value: '$16.1B',
      change: 5.2,
      changeType: 'positive',
      icon: <TrendingUp className="w-6 h-6" />,
      color: 'primary',
    },
    {
      title: 'Top Car',
      value: 'Mercedes C-Class',
      icon: <Award className="w-6 h-6" />,
      color: 'success',
    },
    {
      title: 'Growth Rate',
      value: '+5.2%',
      change: 2.1,
      changeType: 'positive',
      icon: <BarChart3 className="w-6 h-6" />,
      color: 'warning',
    },
    {
      title: 'Predictions',
      value: 'Ready',
      icon: <Target className="w-6 h-6" />,
      color: 'success',
    },
  ];

  const features = [
    {
      icon: <BarChart3 className="w-8 h-8" />,
      title: 'Interactive Charts',
      description: 'Visualize trends and patterns with beautiful, interactive charts that make data easy to understand.',
    },
    {
      icon: <Target className="w-8 h-8" />,
      title: 'Smart Recommendations',
      description: 'Get actionable insights automatically based on AI-powered predictions and historical data.',
    },
    {
      icon: <TrendingUp className="w-8 h-8" />,
      title: 'Accurate Forecasts',
      description: 'Predict sales for the next 12 months with confidence intervals and seasonal breakdowns.',
    },
    {
      icon: <Award className="w-8 h-8" />,
      title: 'Priority Ranking',
      description: 'Identify the most profitable cars to stock based on expected profit and risk levels.',
    },
  ];

  const models = [
    {
      title: 'Sales Forecasting',
      subtitle: 'Predict Future Sales',
      description: 'Forecast your total sales for the next 12 months using advanced Prophet AI model with seasonal patterns and trend analysis.',
      icon: <TrendingUp className="w-12 h-12" />,
      color: 'secondary',
      route: '/sales-forecast',
      features: [
        'Monthly predictions',
        'Confidence intervals',
        'Seasonal patterns',
        'Growth analysis',
      ],
    },
    {
      title: 'Priority Ranking',
      subtitle: 'Optimize Inventory',
      description: 'Rank cars by expected profit and risk level to make smarter inventory purchasing decisions with XGBoost predictions.',
      icon: <Award className="w-12 h-12" />,
      color: 'secondary',
      route: '/priority-ranking',
      features: [
        'Profit predictions',
        'Risk assessment',
        'Smart recommendations',
        'Multi-car comparison',
      ],
    },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="bg-gradient-to-br from-secondary to-primary text-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center">
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold mb-6 animate-fade-in">
              AI-Powered Sales Forecasting
            </h1>
            <p className="text-xl md:text-2xl text-white text-opacity-90 mb-8 max-w-3xl mx-auto animate-fade-in">
              Make smarter decisions with predictive analytics for car dealerships
            </p>
            <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-4 animate-fade-in">
              <Button
                variant="primary"
                size="lg"
                onClick={() => navigate('/sales-forecast')}
                rightIcon={<ArrowRight className="w-5 h-5" />}
                className="border-white text-white hover:bg-white hover:text-secondary"
              >
                Sales Forecast
              </Button>
              <Button
                variant="primary"
                size="lg"
                onClick={() => navigate('/priority-ranking')}
                rightIcon={<ArrowRight className="w-5 h-5" />}
                className="border-white text-white hover:bg-white hover:text-secondary"
              >
                Priority Ranking
              </Button>
            </div>
          </div>
        </div>
      </section>

      {/* Stats Cards */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 -mt-10">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {stats.map((stat, index) => (
            <StatCard key={index} {...stat} />
          ))}
        </div>
      </section>

      {/* About Section */}
      <section className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20">
        <div className="text-center mb-12">
          <h2 className="section-title text-center">About This System</h2>
          <p className="text-gray-400 text-lg max-w-3xl mx-auto">
            Our AI-powered platform combines two specialized models to help car dealerships 
            optimize inventory and forecast sales with confidence.
          </p>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {models.map((model, index) => (
            <div
              key={index}
              className="card-bordered hover:shadow-lg cursor-pointer"
              onClick={() => navigate(model.route)}
            >
              <div className={`w-20 h-20 rounded-lg bg-${model.color} bg-opacity-10 flex items-center justify-center mb-6`}>
                <div className={`text-${model.color}`}>
                  {model.icon}
                </div>
              </div>
              
              <h3 className="text-2xl font-bold text-primary mb-2">
                {model.title}
              </h3>
              <p className="text-sm font-medium text-secondary mb-4">
                {model.subtitle}
              </p>
              <p className="text-gray-400 mb-6">
                {model.description}
              </p>

              <ul className="space-y-2 mb-6">
                {model.features.map((feature, i) => (
                  <li key={i} className="flex items-center text-sm text-gray-500">
                    <CheckCircle className="w-4 h-4 text-success mr-2 flex-shrink-0" />
                    {feature}
                  </li>
                ))}
              </ul>

              <Button
                variant="secondary"
                fullWidth
                rightIcon={<ArrowRight className="w-5 h-5" />}
              >
                Learn More
              </Button>
            </div>
          ))}
        </div>
      </section>

      {/* Features Section */}
      <section className="bg-white py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-12">
            <h2 className="section-title text-center">Key Features</h2>
            <p className="text-gray-400 text-lg max-w-3xl mx-auto">
              Everything you need to make data-driven inventory and sales decisions
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
            {features.map((feature, index) => (
              <div key={index} className="text-center">
                <div className="w-16 h-16 rounded-lg bg-secondary bg-opacity-10 flex items-center justify-center mx-auto mb-4">
                  <div className="text-secondary">
                    {feature.icon}
                  </div>
                </div>
                <h3 className="text-lg font-semibold text-primary mb-2">
                  {feature.title}
                </h3>
                <p className="text-gray-400 text-sm">
                  {feature.description}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="bg-gradient-to-r from-secondary to-primary py-16">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <h2 className="text-3xl md:text-4xl font-bold text-white mb-4">
            Ready to get started?
          </h2>
          <p className="text-xl text-white text-opacity-90 mb-8">
            Start making smarter inventory decisions today
          </p>
          <div className="flex flex-col sm:flex-row items-center justify-center space-y-4 sm:space-y-0 sm:space-x-4">
            <Button
              variant="primary"
              size="lg"
              onClick={() => navigate('/sales-forecast')}
              className="border-white text-white hover:bg-white hover:text-secondary"
            >
              Generate Sales Forecast
            </Button>
            <Button
              variant="primary"
              size="lg"
              onClick={() => navigate('/priority-ranking')}
              className="border-white text-white hover:bg-white hover:text-secondary"
            >
              Rank Your Inventory
            </Button>
          </div>
        </div>
      </section>
    </div>
  );
};

export default HomePage;