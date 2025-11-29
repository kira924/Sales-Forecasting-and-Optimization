// API Configuration
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api';

// Car Makes
export const CAR_MAKES = [
  'Toyota',
  'BMW',
  'Mercedes',
  'Honda',
  'Ford',
  'Hyundai',
  'Nissan',
  'Chevrolet',
  'Audi',
  'Kia'
];

// Car Models by Make
export const CAR_MODELS = {
  Toyota: ['Camry', 'Corolla', 'RAV4', 'Highlander', 'Prius'],
  BMW: ['3 Series', 'X5', '5 Series', 'X3', '7 Series'],
  Mercedes: ['C-Class', 'E-Class', 'GLE', 'S-Class', 'GLC'],
  Honda: ['Civic', 'Accord', 'CR-V', 'Pilot', 'HR-V'],
  Ford: ['Fusion', 'Escape', 'Explorer', 'F-150', 'Mustang'],
  Hyundai: ['Elantra', 'Sonata', 'Tucson', 'Santa Fe', 'Kona'],
  Nissan: ['Altima', 'Rogue', 'Sentra', 'Pathfinder', 'Murano'],
  Chevrolet: ['Malibu', 'Equinox', 'Silverado', 'Traverse', 'Camaro'],
  Audi: ['A4', 'Q5', 'A6', 'Q7', 'A3'],
  Kia: ['Optima', 'Sorento', 'Sportage', 'Soul', 'Forte']
};

// Sales Regions
export const REGIONS = ['East', 'West', 'North', 'South', 'Central'];

// Months
export const MONTHS = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December'
];

// Years
export const YEARS = [2020, 2021, 2022, 2023, 2024, 2025, 2026];

// Profit Margin Options
export const PROFIT_MARGINS = [
  { value: null, label: 'Raw predictions (full values)' },
  { value: 0.10, label: '10% margin (competitive market)' },
  { value: 0.15, label: '15% margin (realistic dealer profit)' },
  { value: 0.20, label: '20% margin (premium market)' }
];

// Forecast View Options
export const FORECAST_VIEWS = [
  { value: 'quick', label: 'Quick Preview (Next 3 Months)' },
  { value: 'full', label: 'Full Year Forecast (Next 12 Months)' }
];

// Risk Levels
export const RISK_LEVELS = {
  LOW: { label: 'Low', color: 'success', emoji: '🟢' },
  MEDIUM: { label: 'Medium', color: 'warning', emoji: '🟡' },
  HIGH: { label: 'High', color: 'danger', emoji: '🔴' }
};

// Confidence Thresholds
export const CONFIDENCE_THRESHOLDS = {
  HIGH: 60,
  MEDIUM: 30,
  LOW: 0
};

// Chart Colors
export const CHART_COLORS = {
  primary: '#3498DB',
  success: '#27AE60',
  warning: '#F39C12',
  danger: '#E74C3C',
  gray: '#95A5A6',
  lightBlue: '#AED6F1',
  lightGreen: '#A9DFBF',
};

// Date Formats
export const DATE_FORMATS = {
  DISPLAY: 'MMM DD, YYYY',
  API: 'YYYY-MM-DD',
  MONTH_YEAR: 'MMMM YYYY'
};

// Table Page Sizes
export const PAGE_SIZES = [10, 25, 50, 100];

// Toast Durations (ms)
export const TOAST_DURATION = {
  SUCCESS: 3000,
  ERROR: 5000,
  WARNING: 4000,
  INFO: 3000
};