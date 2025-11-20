import joblib
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict
import os
import json
import logging
import pickle

from app.models.schemas import CarInput, CarRanking, MonthlyForecast
from app.config import settings

logger = logging.getLogger(__name__)

class MLService:
    def __init__(self):
        # Priority Ranking Model (XGBoost)
        self.profit_model = None
        self.preprocessor = None
        self.feature_columns = None
        self.historical_data = None
        
        # Sales Forecasting Model (Prophet)
        self.prophet_model = None
        self.prophet_scaler = None
        
        # Load all models
        self.load_models()
    
    def load_models(self):
        """Load all trained models"""
        try:
            MODEL_DIR = 'models/'
            
            # ============================================
            # 1. PRIORITY RANKING MODEL (XGBoost)
            # ============================================
            
            # Load XGBoost model
            model_path = os.path.join(MODEL_DIR, 'priority_ranking_model.pkl')
            if os.path.exists(model_path):
                self.profit_model = joblib.load(model_path)
                logger.info(" Priority ranking model loaded")
            else:
                logger.warning(f" Model not found: {model_path}")
            
            # Load Preprocessor
            preprocessor_path = os.path.join(MODEL_DIR, 'full_preprocessor.pkl')
            if os.path.exists(preprocessor_path):
                self.preprocessor = joblib.load(preprocessor_path)
                logger.info(" Preprocessor loaded")
            else:
                logger.warning(f" Preprocessor not found: {preprocessor_path}")
            
            # Load Feature Columns
            features_path = os.path.join(MODEL_DIR, 'model_features.json')
            if os.path.exists(features_path):
                with open(features_path, 'r') as f:
                    self.feature_columns = json.load(f)
                logger.info(f" Feature columns loaded: {len(self.feature_columns)} features")
            else:
                logger.warning(f" Features file not found: {features_path}")
            
            # Load Historical Averages
            historical_path = os.path.join(MODEL_DIR, 'historical_averages.json')
            if os.path.exists(historical_path):
                with open(historical_path, 'r') as f:
                    self.historical_data = json.load(f)
                logger.info(" Historical averages loaded")
            else:
                logger.warning(f" Historical data not found: {historical_path}")
            
            # ============================================
            # 2. SALES FORECASTING MODEL (Prophet)
            # ============================================
            
            # Load Prophet model
            prophet_path = os.path.join(MODEL_DIR, 'sales_forecast_model.pkl')
            if os.path.exists(prophet_path):
                self.prophet_model = joblib.load(prophet_path)

                logger.info(" Prophet sales forecast model loaded")
            else:
                logger.warning(f" Prophet model not found: {prophet_path}")
            
            # Load Prophet scaler (if exists)
            scaler_path = os.path.join(MODEL_DIR, 'prophet_scaler.pkl')
            if os.path.exists(scaler_path):
                self.prophet_scaler = joblib.load(scaler_path)
                logger.info(" Prophet scaler loaded")
            else:
                logger.info(" Prophet scaler not found (optional)")
            
            # ============================================
            # CHECK STATUS
            # ============================================
            
            ranking_ready = all([
                self.profit_model, 
                self.preprocessor, 
                self.feature_columns, 
                self.historical_data
            ])
            
            forecast_ready = self.prophet_model is not None
            
            if ranking_ready and forecast_ready:
                logger.info("All models loaded successfully!")
            elif ranking_ready:
                logger.warning(" Priority Ranking ready, Sales Forecast using fallback")
            elif forecast_ready:
                logger.warning("Sales Forecast ready, Priority Ranking using fallback")
            else:
                logger.warning(" All models using fallback mode")
                
        except Exception as e:
            logger.error(f" Error loading models: {e}")
            logger.warning(" Falling back to mock predictions")
    
    # ============================================
    # SALES FORECASTING (Prophet)
    # ============================================
    
    def generate_sales_forecast(self, view_type: str = "full") -> Dict:
        """Generate sales forecast using Prophet model"""
        logger.info(f" Generating forecast (view: {view_type})")
        
        try:
            if self.prophet_model:
                return self._prophet_forecast(view_type)
            else:
                return self._fallback_forecast(view_type)
        except Exception as e:
            logger.error(f" Error in forecast: {e}")
            return self._fallback_forecast(view_type)
    
    def _prophet_forecast(self, view_type: str) -> Dict:
        """Generate forecast using Prophet model"""
        try:
            # Create future dates for 2025
            future_dates = pd.date_range(
                start='2025-01-01',
                end='2025-12-31',
                freq='MS'  # Month Start
            )
            
            # Create DataFrame for Prophet
            future_df = pd.DataFrame({'ds': future_dates})
            
            # Generate predictions
            forecast = self.prophet_model.predict(future_df)
            
            # Extract predictions
            monthly_forecast = []
            for idx, row in forecast.iterrows():
                month_name = row['ds'].strftime('%b %Y')
                
                # Scale back if scaler was used
                if self.prophet_scaler:
                    yhat = self.prophet_scaler.inverse_transform([[row['yhat']]])[0][0]
                    yhat_lower = self.prophet_scaler.inverse_transform([[row['yhat_lower']]])[0][0]
                    yhat_upper = self.prophet_scaler.inverse_transform([[row['yhat_upper']]])[0][0]
                else:
                    yhat = row['yhat']
                    yhat_lower = row['yhat_lower']
                    yhat_upper = row['yhat_upper']
                
                monthly_forecast.append({
                    'month': month_name,
                    'forecast': round(float(yhat), 2),
                    'lower_bound': round(float(yhat_lower), 2),
                    'upper_bound': round(float(yhat_upper), 2),
                })
            
            # Calculate totals
            total_forecast = sum(m['forecast'] for m in monthly_forecast)
            
            # Estimate 2024 total (you can replace with actual data)
            total_2024 = total_forecast * 0.95  # Assuming 5% growth
            
            # Filter based on view type
            if view_type == 'quick':
                monthly_forecast = monthly_forecast[:3]  # First 3 months
            
            return {
                'total_forecast': round(total_forecast, 2),
                'total_2024': round(total_2024, 2),
                'growth_rate': round(((total_forecast - total_2024) / total_2024) * 100, 2),
                'monthly_forecast': monthly_forecast,
                'model_used': 'Prophet'
            }
            
        except Exception as e:
            logger.error(f" Prophet forecast error: {e}")
            return self._fallback_forecast(view_type)
    
    def _fallback_forecast(self, view_type: str) -> Dict:
        """Fallback forecast using simple logic"""
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 
                  'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        base_value = 1_450_000
        
        monthly_forecast = []
        for idx, month in enumerate(months):
            seasonal_factor = 1 + np.sin((idx / 12) * np.pi * 2) * 0.15
            random_variation = 0.95 + np.random.random() * 0.1
            forecast = base_value * seasonal_factor * random_variation
            
            monthly_forecast.append({
                'month': f"{month} 2025",
                'forecast': round(forecast, 2),
                'lower_bound': round(forecast * 0.85, 2),
                'upper_bound': round(forecast * 1.15, 2),
            })
        
        total_forecast = sum(m['forecast'] for m in monthly_forecast)
        total_2024 = 17_500_000
        
        # Filter based on view type
        if view_type == 'quick':
            monthly_forecast = monthly_forecast[:3]
        
        return {
            'total_forecast': round(total_forecast, 2),
            'total_2024': round(total_2024, 2),
            'growth_rate': round(((total_forecast - total_2024) / total_2024) * 100, 2),
            'monthly_forecast': monthly_forecast,
            'model_used': 'Fallback'
        }
    
    # ============================================
    # PRIORITY RANKING (XGBoost)
    # ============================================
    
    def generate_priority_ranking(self, cars: List[CarInput], 
                                   target_month: str, target_year: int,
                                   region: str, profit_margin: float = None) -> Dict:
        """Generate priority ranking using trained model"""
        try:
            if self.profit_model and self.preprocessor and self.feature_columns and self.historical_data:
                logger.info(f" Using trained model for {len(cars)} cars")
                return self._model_ranking(cars, target_month, target_year, region, profit_margin)
            else:
                logger.warning(" Model not available, using fallback")
                return self._fallback_ranking(cars, target_month, target_year, region, profit_margin)
        except Exception as e:
            logger.error(f" Error in ranking: {e}")
            return self._fallback_ranking(cars, target_month, target_year, region, profit_margin)
    
    def _model_ranking(self, cars: List[CarInput], target_month: str,
                       target_year: int, region: str, profit_margin: float) -> Dict:
        """Use YOUR trained model for ranking"""
        
        # Build inventory DataFrame
        inventory_df = self._build_car_inventory(
            [c.make for c in cars],
            [c.model for c in cars],
            [c.year for c in cars],
            [c.quantity for c in cars],
            target_month,
            target_year,
            region
        )
        
        # Engineer features
        features_df, full_df = self._engineer_features(inventory_df)
        
        # Preprocess
        features_processed = self.preprocessor.transform(features_df)
        
        # Predict
        predictions = self.profit_model.predict(features_processed)
        
        # Apply profit margin if specified
        if profit_margin:
            predictions = predictions * profit_margin
        
        # Calculate confidence and risk
        rankings = []
        model_mae = 4432  # From your training results
        
        for idx, car in enumerate(cars):
            predicted_profit = float(predictions[idx] * car.quantity)
            car_age = target_year - car.year
            
            # Confidence calculation
            confidence_raw = 100 * (1 - (model_mae / max(predictions[idx], 1)))
            confidence = max(0, min(100, confidence_raw))
            
            # Risk calculation
            risk = self._calculate_risk(predicted_profit / car.quantity, confidence, car_age)
            
            rankings.append({
                'make': car.make,
                'model': car.model,
                'year': car.year,
                'age': car_age,
                'quantity': car.quantity,
                'profit': round(predicted_profit, 2),
                'confidence': round(confidence, 1),
                'risk': risk
            })
        
        # Sort by profit
        rankings.sort(key=lambda x: x['profit'], reverse=True)
        
        return {
            'rankings': rankings,
            'model_used': 'XGBoost'
        }
    
    def _build_car_inventory(self, car_makes, car_models, car_years, quantities,
                             target_month, target_year, sales_region):
        """Build inventory DataFrame"""
        n_cars = len(car_makes)
        
        month_mapping = {
            'January': 1, 'February': 2, 'March': 3, 'April': 4,
            'May': 5, 'June': 6, 'July': 7, 'August': 8,
            'September': 9, 'October': 10, 'November': 11, 'December': 12
        }
        target_month_num = month_mapping.get(target_month, 1)
        
        season_mapping = {
            12: 'Winter', 1: 'Winter', 2: 'Winter', 3: 'Spring', 4: 'Spring', 5: 'Spring',
            6: 'Summer', 7: 'Summer', 8: 'Summer', 9: 'Fall', 10: 'Fall', 11: 'Fall'
        }
        season = season_mapping[target_month_num]
        quarter = (target_month_num - 1) // 3 + 1
        
        inventory_df = pd.DataFrame({
            'Car_Make': car_makes,
            'Car_Model': car_models,
            'Car Year': car_years,
            'Quantity': quantities,
            'Sale Year': target_year,
            'Sale Month': target_month,
            'Sale Month Num': target_month_num,
            'Sale Quarter': quarter,
            'Season': season,
            'Sales Region': sales_region,
            'Is Weekend': 0,
            'Car Age': target_year - np.array(car_years),
            'Customer Age': 45.0,
            'Customer Gender': np.random.choice(['Male', 'Female'], size=n_cars, p=[0.6, 0.4]),
            'Payment Method': np.random.choice(['Credit Card', 'Cash', 'Online'], size=n_cars)
        })
        
        overall_mean = self.historical_data.get('overall_mean', 4000)
        inventory_df['Car_Model_Freq'] = overall_mean
        
        return inventory_df
    
    def _engineer_features(self, inventory_df):
        """Engineer features"""
        df = inventory_df.copy()
        overall_mean = self.historical_data.get('overall_mean', 4000)
        
        # Historical averages
        df['Historical_Make_Avg_Profit'] = df['Car_Make'].map(
            self.historical_data['make_avg_profit']
        ).fillna(overall_mean)
        
        age_bins = [0, 1, 2, 3, 5, 100]
        age_labels = ['New', '1-2Y', '2-3Y', '3-5Y', '5Y+']
        df['Car_Age_Group_Temp'] = pd.cut(df['Car Age'], bins=age_bins, labels=age_labels)
        
        mapped_values = df['Car_Age_Group_Temp'].map(self.historical_data['age_avg_profit'])
        df['Historical_Age_Avg_Profit'] = mapped_values.astype(float).fillna(overall_mean)
        
        df['Historical_Season_Avg_Profit'] = df['Season'].map(
            self.historical_data['season_avg_profit']
        ).fillna(overall_mean)
        
        # Interaction features
        df['Quantity_x_CarAge'] = df['Quantity'] * df['Car Age']
        df['CarYear_x_SaleYear'] = df['Car Year'] * df['Sale Year']
        df['ModelFreq_x_Quantity'] = df['Car_Model_Freq'] * df['Quantity']
        df['Weekend_x_Quarter'] = df['Is Weekend'] * df['Sale Quarter']
        df['CustomerAge_x_CarAge'] = df['Customer Age'] * df['Car Age']
        
        # Polynomial features
        df['Car_Age_Squared'] = df['Car Age'] ** 2
        df['Quantity_Squared'] = df['Quantity'] ** 2
        df['Customer_Age_Squared'] = df['Customer Age'] ** 2
        df['Log_Car_Model_Freq'] = np.log1p(df['Car_Model_Freq'])
        df['Log_Customer_Age'] = np.log1p(df['Customer Age'])
        
        # Time features
        df['Years_Since_New'] = df['Sale Year'] - df['Car Year']
        df['Is_Recent_Year'] = (df['Sale Year'] >= 2023).astype(int)
        df['Is_New_Car'] = (df['Car Age'] <= 1).astype(int)
        df['Quarter_Sin'] = np.sin(2 * np.pi * df['Sale Quarter'] / 4)
        df['Quarter_Cos'] = np.cos(2 * np.pi * df['Sale Quarter'] / 4)
        df['Month_Sin'] = np.sin(2 * np.pi * df['Sale Month Num'] / 12)
        df['Month_Cos'] = np.cos(2 * np.pi * df['Sale Month Num'] / 12)
        
        # Add missing columns
        for col in self.feature_columns:
            if col not in df.columns:
                df[col] = 0
        
        # Reindex to match training features
        final_df = df.reindex(columns=self.feature_columns, fill_value=0)
        
        return final_df, df
    
    def _fallback_ranking(self, cars: List[CarInput], target_month: str,
                          target_year: int, region: str, profit_margin: float) -> Dict:
        """Fallback ranking (if model not available)"""
        rankings = []
        
        make_multipliers = {
            'Mercedes': 2.5, 'BMW': 2.2, 'Audi': 2.0,
            'Toyota': 1.5, 'Honda': 1.4, 'Ford': 1.2,
            'Hyundai': 1.0, 'Nissan': 1.1, 'Chevrolet': 1.1, 'Kia': 0.9
        }
        
        for car in cars:
            base_profit = 5000
            base_profit *= make_multipliers.get(car.make, 1.0)
            car_age = target_year - car.year
            base_profit *= max(0.5, 1 - (car_age * 0.15))
            base_profit *= (0.8 + np.random.random() * 0.4)
            
            if profit_margin:
                base_profit *= profit_margin
            
            confidence = max(5, min(70, 70 - (car_age * 10) + (np.random.random() * 15)))
            risk = self._calculate_risk(base_profit, confidence, car_age)
            
            rankings.append({
                'make': car.make,
                'model': car.model,
                'year': car.year,
                'age': car_age,
                'quantity': car.quantity,
                'profit': round(base_profit * car.quantity, 2),
                'confidence': round(confidence, 1),
                'risk': risk
            })
        
        rankings.sort(key=lambda x: x['profit'], reverse=True)
        return {
            'rankings': rankings,
            'model_used': 'Fallback'
        }
    
    def _calculate_risk(self, profit: float, confidence: float, age: int) -> str:
        """Calculate risk level"""
        score = 0
        
        if profit > 6000: score += 0
        elif profit > 4500: score += 1
        elif profit > 3000: score += 2
        else: score += 3
        
        if confidence > 60: score += 0
        elif confidence > 40: score += 1
        elif confidence > 20: score += 2
        else: score += 3
        
        if age == 0: score += 0
        elif age <= 2: score += 1
        elif age <= 4: score += 2
        else: score += 3
        
        if score <= 3: return 'LOW'
        elif score <= 6: return 'MEDIUM'
        else: return 'HIGH'

# Create singleton instance
ml_service = MLService()