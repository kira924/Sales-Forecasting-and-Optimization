import axios from 'axios';
import { API_BASE_URL } from '../utils/constants';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor (add auth token if needed)
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor (handle errors)
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    if (error.response?.status === 401) {
      // Unauthorized - redirect to login
      localStorage.removeItem('authToken');
      localStorage.removeItem('isAuthenticated');
      window.location.href = '/signin';
    }
    return Promise.reject(error);
  }
);

// ============================================
// MOCK DATA GENERATORS (Replace with real API calls in production)
// ============================================

const generateMockForecastData = () => {
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const baseValue = 1400000;
  
  const monthlyForecast = months.map((month, index) => {
    const seasonalFactor = 1 + Math.sin((index / 12) * Math.PI * 2) * 0.15;
    const randomVariation = 0.95 + Math.random() * 0.1;
    const forecast = baseValue * seasonalFactor * randomVariation;
    
    return {
      month: month + ' 2025',
      forecast: Math.round(forecast),
      lowerBound: Math.round(forecast * 0.85),
      upperBound: Math.round(forecast * 1.15),
    };
  });

  const totalForecast = monthlyForecast.reduce((sum, m) => sum + m.forecast, 0);
  const total2024 = totalForecast * 0.95;

  return {
    totalForecast,
    total2024,
    growthRate: ((totalForecast - total2024) / total2024) * 100,
    monthlyForecast,
  };
};

const generateMockRankingData = (cars, targetMonth, targetYear, region, profitMargin) => {
  const rankings = cars.map((car, index) => {
    // Base profit calculation (mock)
    let baseProfit = 5000;
    
    // Adjust by make
    const makeMultipliers = {
      'Mercedes': 2.5,
      'BMW': 2.2,
      'Audi': 2.0,
      'Toyota': 1.5,
      'Honda': 1.4,
      'Ford': 1.2,
      'Hyundai': 1.0,
      'Nissan': 1.1,
      'Chevrolet': 1.1,
      'Kia': 0.9,
    };
    baseProfit *= (makeMultipliers[car.make] || 1);
    
    // Adjust by year (newer = higher)
    const carAge = 2025 - parseInt(car.year);
    baseProfit *= Math.max(0.5, 1 - (carAge * 0.15));
    
    // Add randomness
    baseProfit *= (0.8 + Math.random() * 0.4);
    
    // Calculate confidence (decreases with age)
    const confidence = Math.max(5, Math.min(70, 70 - (carAge * 10) + (Math.random() * 15)));
    
    // Determine risk
    let risk = 'MEDIUM';
    if (confidence > 50 && baseProfit > 6000) risk = 'LOW';
    else if (confidence < 20 || baseProfit < 3000) risk = 'HIGH';
    
    return {
      make: car.make,
      model: car.model,
      year: car.year,
      age: carAge,
      quantity: car.quantity,
      profit: Math.round(baseProfit * car.quantity),
      confidence: Math.round(confidence),
      risk,
    };
  });

  // Sort by profit (descending)
  rankings.sort((a, b) => b.profit - a.profit);

  return { rankings };
};

// ============================================
// API FUNCTIONS
// ============================================

/**
 * Generate sales forecast for next 12 months
 */
export const generateSalesForecast = async () => {
  try {
    // In production, uncomment this:
    // const response = await api.post('/forecast/sales');
    // return response;
    
    // For demo, return mock data
    await new Promise(resolve => setTimeout(resolve, 500));
    return generateMockForecastData();
  } catch (error) {
    console.error('Error generating sales forecast:', error);
    throw error;
  }
};

/**
 * Generate priority ranking for cars
 */
export const generatePriorityRanking = async (data) => {
  try {
    // In production, uncomment this:
    // const response = await api.post('/ranking/priority', data);
    // return response;
    
    // For demo, return mock data
    await new Promise(resolve => setTimeout(resolve, 500));
    return generateMockRankingData(
      data.cars,
      data.targetMonth,
      data.targetYear,
      data.region,
      data.profitMargin
    );
  } catch (error) {
    console.error('Error generating priority ranking:', error);
    throw error;
  }
};

/**
 * User authentication
 */
export const signIn = async (email, password) => {
  try {
    // In production:
    // const response = await api.post('/auth/signin', { email, password });
    // localStorage.setItem('authToken', response.token);
    // return response;
    
    // For demo
    await new Promise(resolve => setTimeout(resolve, 500));
    return { success: true, user: { email } };
  } catch (error) {
    console.error('Error signing in:', error);
    throw error;
  }
};

export const signUp = async (userData) => {
  try {
    // In production:
    // const response = await api.post('/auth/signup', userData);
    // return response;
    
    // For demo
    await new Promise(resolve => setTimeout(resolve, 500));
    return { success: true };
  } catch (error) {
    console.error('Error signing up:', error);
    throw error;
  }
};

export default api;