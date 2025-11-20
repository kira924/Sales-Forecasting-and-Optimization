import React, { useState } from 'react';
import { Download, AlertCircle, Plus, Trash2 } from 'lucide-react';
import Button from '../common/Button';
import Card from '../common/Card';
import { ProgressSpinner } from '../common/LoadingSpinner';
import { useToast } from '../common/Toast';
import RankingForm from './RankingForm';
import RankingResults from './RankingResults';
import { generatePriorityRanking } from '../../services/api';
import { generateId } from '../../utils/helpers';

const PriorityRankingPage = () => {
  const { success, error: showError } = useToast();
  const [cars, setCars] = useState([
    { id: generateId(), make: '', model: '', year: '', quantity: 1 }
  ]);
  const [formData, setFormData] = useState({
    targetMonth: '',
    targetYear: new Date().getFullYear() + 1,
    region: 'East',
    profitMargin: 0.15,
  });
  const [loading, setLoading] = useState(false);
  const [loadingStep, setLoadingStep] = useState(0);
  const [results, setResults] = useState(null);
  const [errors, setErrors] = useState({});

  const loadingSteps = [
    'Engineering features...',
    'Running XGBoost model...',
    'Calculating risk levels...',
    'Ranking results...',
  ];

  const handleAddCar = () => {
    setCars([...cars, { id: generateId(), make: '', model: '', year: '', quantity: 1 }]);
  };

  const handleRemoveCar = (id) => {
    if (cars.length > 1) {
      setCars(cars.filter(car => car.id !== id));
    }
  };

  const handleCarChange = (id, field, value) => {
    setCars(cars.map(car => 
      car.id === id ? { ...car, [field]: value } : car
    ));
    // Clear error for this car
    if (errors[`car_${id}_${field}`]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[`car_${id}_${field}`];
        return newErrors;
      });
    }
  };

  const handleFormChange = (field, value) => {
    setFormData(prev => ({ ...prev, [field]: value }));
    if (errors[field]) {
      setErrors(prev => {
        const newErrors = { ...prev };
        delete newErrors[field];
        return newErrors;
      });
    }
  };

  const validate = () => {
    const newErrors = {};

    // Validate cars
    cars.forEach((car, index) => {
      if (!car.make) {
        newErrors[`car_${car.id}_make`] = 'Car make is required';
      }
      if (!car.model) {
        newErrors[`car_${car.id}_model`] = 'Car model is required';
      }
      if (!car.year) {
        newErrors[`car_${car.id}_year`] = 'Car year is required';
      }
      if (!car.quantity || car.quantity < 1 || car.quantity > 100) {
        newErrors[`car_${car.id}_quantity`] = 'Quantity must be between 1 and 100';
      }
    });

    // Validate form data
    if (!formData.targetMonth) {
      newErrors.targetMonth = 'Target month is required';
    }
    if (!formData.targetYear || formData.targetYear < 2025 || formData.targetYear > 2026) {
      newErrors.targetYear = 'Year must be between 2025 and 2026';
    }

    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = async () => {
    if (!validate()) {
      showError('Please fill in all required fields correctly');
      return;
    }

    setLoading(true);
    setLoadingStep(0);

    try {
      // Simulate step-by-step loading
      for (let i = 0; i < loadingSteps.length; i++) {
        setLoadingStep(i + 1);
        await new Promise(resolve => setTimeout(resolve, 1000));
      }

      // Call API
      const data = await generatePriorityRanking({
        cars,
        ...formData,
      });
      
      setResults(data);
      success('Priority ranking generated successfully!');
      
      // Scroll to results
      setTimeout(() => {
        document.getElementById('results-section')?.scrollIntoView({ 
          behavior: 'smooth',
          block: 'start'
        });
      }, 100);
    } catch (err) {
      showError('Failed to generate ranking. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
      setLoadingStep(0);
    }
  };

  const handleClearAll = () => {
    setCars([{ id: generateId(), make: '', model: '', year: '', quantity: 1 }]);
    setFormData({
      targetMonth: '',
      targetYear: new Date().getFullYear() + 1,
      region: 'East',
      profitMargin: 0.15,
    });
    setResults(null);
    setErrors({});
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-primary mb-2">
             Car Inventory Priority Ranking System
          </h1>
          <p className="text-gray-400 text-lg">
            Identify the most profitable cars for your next purchase
          </p>
        </div>

        {/* Important Notice */}
        <Card className="mb-8 border-l-4 border-warning">
          <div className="flex items-start space-x-3">
            <AlertCircle className="w-6 h-6 text-warning flex-shrink-0 mt-1" />
            <div>
              <h3 className="font-semibold text-warning mb-2">
                 PREDICTION ACCURACY NOTE:
              </h3>
              <ul className="text-sm text-gray-500 space-y-1">
                <li>• <strong>Highest accuracy:</strong> Next 1-3 months (Confidence: 60%+)</li>
                <li>• <strong>Good accuracy:</strong> Months 4-6 (Confidence: 40-60%)</li>
                <li>• <strong>Moderate accuracy:</strong> Months 7-12 (Confidence: 20-40%)</li>
              </ul>
              <p className="text-sm text-gray-500 mt-2">
                Recommendations are most reliable for near-term inventory decisions.
              </p>
            </div>
          </div>
        </Card>

        {/* Input Form */}
        <Card title=" Input Car Details" className="mb-8">
          <RankingForm
            cars={cars}
            formData={formData}
            errors={errors}
            onCarChange={handleCarChange}
            onFormChange={handleFormChange}
            onAddCar={handleAddCar}
            onRemoveCar={handleRemoveCar}
          />

          {/* Action Buttons */}
          <div className="mt-6 flex flex-col sm:flex-row items-center space-y-4 sm:space-y-0 sm:space-x-4">
            <Button
              variant="secondary"
              fullWidth
              onClick={handleClearAll}
              leftIcon={<Trash2 className="w-5 h-5" />}
            >
              Clear All
            </Button>
            <Button
              variant="primary"
              fullWidth
              onClick={handleSubmit}
              loading={loading}
              leftIcon={<Plus className="w-5 h-5" />}
            >
              Predict Priority
            </Button>
          </div>
        </Card>

        {/* Loading State */}
        {loading && (
          <Card>
            <ProgressSpinner
              steps={loadingSteps}
              currentStep={loadingStep}
              text="Analyzing Car Profitability..."
            />
          </Card>
        )}

        {/* Results */}
        {!loading && results && (
          <div id="results-section">
            <RankingResults data={results} profitMargin={formData.profitMargin} />
          </div>
        )}

        {/* Empty State */}
        {!loading && !results && (
          <Card>
            <div className="text-center py-12">
              <Plus className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <h3 className="text-xl font-semibold text-gray-400 mb-2">
                No predictions yet
              </h3>
              <p className="text-gray-400 mb-6">
                Fill in the form above and click "Predict Priority" to see results
              </p>
            </div>
          </Card>
        )}
      </div>
    </div>
  );
};

export default PriorityRankingPage;