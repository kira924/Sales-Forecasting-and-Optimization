import React from 'react';
import { X } from 'lucide-react';
import Button from '../common/Button';
import Tooltip from '../common/Tooltip';
import { CAR_MAKES, CAR_MODELS, YEARS, REGIONS, MONTHS, PROFIT_MARGINS } from '../../utils/constants';

const RankingForm = ({
  cars,
  formData,
  errors,
  onCarChange,
  onFormChange,
  onAddCar,
  onRemoveCar,
}) => {
  return (
    <div className="space-y-6">
      {/* Cars Input */}
      {cars.map((car, index) => (
        <div key={car.id} className="border-2 border-gray-100 rounded-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h4 className="text-lg font-semibold text-primary">
              Car #{index + 1}
            </h4>
            {cars.length > 1 && (
              <button
                onClick={() => onRemoveCar(car.id)}
                className="text-danger hover:text-danger-dark transition-colors"
              >
                <X className="w-5 h-5" />
              </button>
            )}
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {/* Car Make */}
            <div>
              <label className="block text-sm font-medium text-gray-500 mb-2">
                Car Make <Tooltip content="Select the car manufacturer" />
              </label>
              <select
                value={car.make}
                onChange={(e) => onCarChange(car.id, 'make', e.target.value)}
                className={`input-field ${errors[`car_${car.id}_make`] ? 'input-error' : ''}`}
              >
                <option value="">Select make...</option>
                {CAR_MAKES.map(make => (
                  <option key={make} value={make}>{make}</option>
                ))}
              </select>
              {errors[`car_${car.id}_make`] && (
                <p className="mt-1 text-sm text-danger">{errors[`car_${car.id}_make`]}</p>
              )}
            </div>

            {/* Car Model */}
            <div>
              <label className="block text-sm font-medium text-gray-500 mb-2">
                Car Model <Tooltip content="Select the car model (filtered by make)" />
              </label>
              <select
                value={car.model}
                onChange={(e) => onCarChange(car.id, 'model', e.target.value)}
                disabled={!car.make}
                className={`input-field ${errors[`car_${car.id}_model`] ? 'input-error' : ''}`}
              >
                <option value="">Select model...</option>
                {car.make && CAR_MODELS[car.make]?.map(model => (
                  <option key={model} value={model}>{model}</option>
                ))}
              </select>
              {errors[`car_${car.id}_model`] && (
                <p className="mt-1 text-sm text-danger">{errors[`car_${car.id}_model`]}</p>
              )}
            </div>

            {/* Car Year */}
            <div>
              <label className="block text-sm font-medium text-gray-500 mb-2">
                Car Year <Tooltip content="Manufacturing year of the vehicle" />
              </label>
              <select
                value={car.year}
                onChange={(e) => onCarChange(car.id, 'year', e.target.value)}
                className={`input-field ${errors[`car_${car.id}_year`] ? 'input-error' : ''}`}
              >
                <option value="">Select year...</option>
                {YEARS.map(year => (
                  <option key={year} value={year}>{year}</option>
                ))}
              </select>
              {errors[`car_${car.id}_year`] && (
                <p className="mt-1 text-sm text-danger">{errors[`car_${car.id}_year`]}</p>
              )}
            </div>

            {/* Quantity */}
            <div>
              <label className="block text-sm font-medium text-gray-500 mb-2">
                Quantity <Tooltip content="Number of units to purchase (1-100)" />
              </label>
              <input
                type="number"
                min="1"
                max="100"
                value={car.quantity}
                onChange={(e) => onCarChange(car.id, 'quantity', parseInt(e.target.value) || 1)}
                className={`input-field ${errors[`car_${car.id}_quantity`] ? 'input-error' : ''}`}
                placeholder="1"
              />
              {errors[`car_${car.id}_quantity`] && (
                <p className="mt-1 text-sm text-danger">{errors[`car_${car.id}_quantity`]}</p>
              )}
            </div>
          </div>
        </div>
      ))}

      {/* Add Another Car */}
      <Button
        variant="secondary"
        fullWidth
        onClick={onAddCar}
        leftIcon={<span className="text-xl">+</span>}
      >
        Add Another Car
      </Button>

      {/* Divider */}
      <div className="border-t-2 border-gray-100 pt-6">
        <h4 className="text-lg font-semibold text-primary mb-4">
          Forecast Period
        </h4>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {/* Target Month */}
          <div>
            <label className="block text-sm font-medium text-gray-500 mb-2">
              Target Month <Tooltip content="Month when you expect to sell" />
            </label>
            <select
              value={formData.targetMonth}
              onChange={(e) => onFormChange('targetMonth', e.target.value)}
              className={`input-field ${errors.targetMonth ? 'input-error' : ''}`}
            >
              <option value="">Select month...</option>
              {MONTHS.map(month => (
                <option key={month} value={month}>{month}</option>
              ))}
            </select>
            {errors.targetMonth && (
              <p className="mt-1 text-sm text-danger">{errors.targetMonth}</p>
            )}
          </div>

          {/* Target Year */}
          <div>
            <label className="block text-sm font-medium text-gray-500 mb-2">
              Target Year <Tooltip content="Year of expected sale (2025-2026)" />
            </label>
            <input
              type="number"
              min="2025"
              max="2026"
              value={formData.targetYear}
              onChange={(e) => onFormChange('targetYear', parseInt(e.target.value))}
              className={`input-field ${errors.targetYear ? 'input-error' : ''}`}
              placeholder="2025"
            />
            {errors.targetYear && (
              <p className="mt-1 text-sm text-danger">{errors.targetYear}</p>
            )}
          </div>

          {/* Sales Region */}
          <div>
            <label className="block text-sm font-medium text-gray-500 mb-2">
              Sales Region <Tooltip content="Geographic region for sales" />
            </label>
            <select
              value={formData.region}
              onChange={(e) => onFormChange('region', e.target.value)}
              className="input-field"
            >
              {REGIONS.map(region => (
                <option key={region} value={region}>{region}</option>
              ))}
            </select>
          </div>

          {/* Profit Margin */}
          <div>
            <label className="block text-sm font-medium text-gray-500 mb-2">
              Profit Margin Factor <Tooltip content="Adjusts predictions to realistic dealer profit" />
            </label>
            <select
              value={formData.profitMargin || ''}
              onChange={(e) => onFormChange('profitMargin', e.target.value ? parseFloat(e.target.value) : null)}
              className="input-field"
            >
              {PROFIT_MARGINS.map(option => (
                <option key={option.label} value={option.value || ''}>
                  {option.label}
                </option>
              ))}
            </select>
          </div>
        </div>
      </div>
    </div>
  );
};

export default RankingForm;