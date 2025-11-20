import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import joblib
import json
import os
import warnings
warnings.filterwarnings('ignore')

# ============================================
# CAR DEALERSHIP PRIORITY RANKING SYSTEM
# ============================================

print("=" * 70)
print(" CAR DEALERSHIP PRIORITY RANKING SYSTEM ")
print("=" * 70)

# ============================================
# STEP 1: Load All Trained Artifacts
# ============================================
MODEL_DIR = 'models/'

try:
    print("\n Loading trained model and artifacts...")
    

    trained_model = joblib.load(os.path.join(MODEL_DIR, 'priority_ranking_model.pkl'))
    

    preprocessor = joblib.load(os.path.join(MODEL_DIR, 'full_preprocessor.pkl'))
    

    with open(os.path.join(MODEL_DIR, 'model_features.json'), 'r') as f:
        feature_columns = json.load(f)
        

    with open(os.path.join(MODEL_DIR, 'historical_averages.json'), 'r') as f:
        historical_data = json.load(f)

    print(f" Model loaded successfully.")
    print(f" Preprocessor loaded successfully.")
    print(f" Required features: {len(feature_columns)}")

except FileNotFoundError:
    print(f"Can't find the model files'{MODEL_DIR}'.")
    print("Should play first 'model_selection_and_saving.py'")
    exit()
except Exception as e:
    print(f"Error while loading the model {e}")
    exit()


# ============================================
# STEP 2: Car Inventory Builder Function
# ============================================
def build_car_inventory(car_makes, car_models, car_years, quantities, 
                          target_month, target_year, sales_region='East', 
                          customer_age=45.0, is_weekend=0):
    
    n_cars = len(car_makes)
    month_mapping = {
        'January': 1, 'February': 2, 'March': 3, 'April': 4,
        'May': 5, 'June': 6, 'July': 7, 'August': 8,
        'September': 9, 'October': 10, 'November': 11, 'December': 12
    }
    if isinstance(target_month, str):
        target_month_num = month_mapping.get(target_month, 1)
        target_month_name = target_month
    else:
        target_month_num = target_month
        target_month_name = list(month_mapping.keys())[target_month - 1]
    
    season_mapping = {
        12: 'Winter', 1: 'Winter', 2: 'Winter', 3: 'Spring', 4: 'Spring', 5: 'Spring',
        6: 'Summer', 7: 'Summer', 8: 'Summer', 9: 'Fall', 10: 'Fall', 11: 'Fall'
    }
    season = season_mapping[target_month_num]
    quarter = (target_month_num - 1) // 3 + 1
    
    inventory_df = pd.DataFrame({
        'Car_Make': car_makes, 'Car_Model': car_models, 'Car Year': car_years,
        'Quantity': quantities, 'Sale Year': target_year, 'Sale Month': target_month_name,
        'Sale Month Num': target_month_num, 'Sale Quarter': quarter, 'Season': season,
        'Sales Region': sales_region, 'Is Weekend': is_weekend,
        'Car Age': target_year - np.array(car_years),
        'Customer Age': customer_age,
        'Customer Gender': np.random.choice(['Male', 'Female'], size=n_cars, p=[0.6, 0.4]),
        'Payment Method': np.random.choice(['Credit Card', 'Cash', 'Online'], size=n_cars)
    })
    
    inventory_df['Car_Model_Freq'] = historical_data.get('overall_mean', 4000) 
    
    return inventory_df

# ============================================
# STEP 3: Feature Engineering Pipeline (Production)
# ============================================
def engineer_features(inventory_df, historical_data, feature_columns):
    
    df = inventory_df.copy()
    
    
    # 1. Using the Historical Averages 
    overall_mean = historical_data.get('overall_mean', 4000)
    df['Historical_Make_Avg_Profit'] = df['Car_Make'].map(historical_data['make_avg_profit']).fillna(overall_mean)
    
    age_bins = [0, 1, 2, 3, 5, 100]
    age_labels = ['New', '1-2Y', '2-3Y', '3-5Y', '5Y+']
    df['Car_Age_Group_Temp'] = pd.cut(df['Car Age'], bins=age_bins, labels=age_labels)
    # df['Historical_Age_Avg_Profit'] = df['Car_Age_Group_Temp'].map(historical_data['age_avg_profit']).fillna(overall_mean)
    
    # This prevents the "Cannot setitem on a Categorical" error
    mapped_values = df['Car_Age_Group_Temp'].map(historical_data['age_avg_profit'])
    df['Historical_Age_Avg_Profit'] = mapped_values.astype(float).fillna(overall_mean)

    
    df['Historical_Season_Avg_Profit'] = df['Season'].map(historical_data['season_avg_profit']).fillna(overall_mean)
    
    # 2. Interaction features
    df['Quantity_x_CarAge'] = df['Quantity'] * df['Car Age']
    df['CarYear_x_SaleYear'] = df['Car Year'] * df['Sale Year']
    df['ModelFreq_x_Quantity'] = df['Car_Model_Freq'] * df['Quantity']
    df['Weekend_x_Quarter'] = df['Is Weekend'] * df['Sale Quarter']
    df['CustomerAge_x_CarAge'] = df['Customer Age'] * df['Car Age']
    
    # 3. Polynomial features
    df['Car_Age_Squared'] = df['Car Age'] ** 2
    df['Quantity_Squared'] = df['Quantity'] ** 2
    df['Customer_Age_Squared'] = df['Customer Age'] ** 2
    df['Log_Car_Model_Freq'] = np.log1p(df['Car_Model_Freq'])
    df['Log_Customer_Age'] = np.log1p(df['Customer Age'])
    
    # 4. Time features
    df['Years_Since_New'] = df['Sale Year'] - df['Car Year']
    df['Is_Recent_Year'] = (df['Sale Year'] >= 2023).astype(int)
    df['Is_New_Car'] = (df['Car Age'] <= 1).astype(int)
    df['Quarter_Sin'] = np.sin(2 * np.pi * df['Sale Quarter'] / 4)
    df['Quarter_Cos'] = np.cos(2 * np.pi * df['Sale Quarter'] / 4)
    df['Month_Sin'] = np.sin(2 * np.pi * df['Sale Month Num'] / 12)
    df['Month_Cos'] = np.cos(2 * np.pi * df['Sale Month Num'] / 12)

# (Adding the columns manually created in the first file)
# This ensures the processor sees everything
    for col in [c for c in feature_columns if c.startswith('Make_') or c.startswith('Season_') or c.startswith('Day_')]:
        df[col] = 0 # It will be ignored by the processor but it must be present
    
    # (We only select the original columns that the processor expects)
    final_df = df.reindex(columns=feature_columns, fill_value=0)
    
    return final_df, df

# ============================================
# STEP 4: Priority Ranking Function
# ============================================
def rank_cars_by_profit(
    car_makes, car_models, car_years, quantities,
    target_month, target_year, sales_region='East', top_n=None
):
    
    print(f"\n{'='*70}\nPREDICTING PROFITS FOR {target_month.upper()} {target_year}\n{'='*70}")
    
    # 1. Build inventory
    print(f"\n Building inventory of {len(car_makes)} cars...")
    inventory_df = build_car_inventory(
        car_makes, car_models, car_years, quantities,
        target_month, target_year, sales_region
    )
    
    # 2. Engineer features 
    print(f" Engineering features...")
    features_df, full_df = engineer_features(inventory_df, historical_data, feature_columns)
    
    print(f" Preprocessing data for model...")
    features_processed = preprocessor.transform(features_df)
    
    # 4. Make predictions
    print(f" Making predictions using loaded model...")
    predictions = trained_model.predict(features_processed)
    
    full_df['Predicted_Profit'] = predictions
    
    model_mae = 4432 
    full_df['Prediction_Error_Ratio'] = model_mae / full_df['Predicted_Profit']
    full_df['Confidence'] = np.clip(100 * (1 - full_df['Prediction_Error_Ratio']), 0, 100)
    
    def calculate_risk(row):
        profit = row['Predicted_Profit']
        confidence = row['Confidence']
        car_age = row['Car Age']
        if profit > 6000: profit_risk = 0
        elif profit > 4500: profit_risk = 1
        elif profit > 3000: profit_risk = 2
        else: profit_risk = 3
        if confidence > 60: confidence_risk = 0
        elif confidence > 40: confidence_risk = 1
        elif confidence > 20: confidence_risk = 2
        else: confidence_risk = 3
        if car_age == 0: age_risk = 0
        elif car_age <= 2: age_risk = 1
        elif car_age <= 4: age_risk = 2
        else: age_risk = 3
        total_risk = profit_risk + confidence_risk + age_risk
        if total_risk <= 3: return 'Low'
        elif total_risk <= 6: return 'Medium'
        else: return 'High'
    
    full_df['Risk_Level'] = full_df.apply(calculate_risk, axis=1)
    
    ranked_df = full_df.sort_values('Predicted_Profit', ascending=False).reset_index(drop=True)
    
    output_cols = [
        'Car_Make', 'Car_Model', 'Car Year', 'Car Age', 'Quantity', 
        'Sale Month', 'Season', 'Sales Region',
        'Predicted_Profit', 'Confidence', 'Risk_Level'
    ]
    result_df = ranked_df[output_cols].copy()
    result_df['Rank'] = range(1, len(result_df) + 1)
    
    if top_n:
        result_df = result_df.head(top_n)
    
    print(f"\n Predictions complete! {len(result_df)} cars ranked.")
    return result_df

# ============================================
# STEP 5: EXAMPLE USAGE
# ============================================
if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("EXAMPLE: NEXT MONTH CAR INVENTORY RANKING")
    print("=" * 70)

    current_date = datetime.now()
    next_month_date = current_date + timedelta(days=32)
    next_month_date = next_month_date.replace(day=1)
    next_month_name = next_month_date.strftime('%B')
    next_month_year = next_month_date.year

    example_cars = {
        'makes': ['Toyota', 'BMW', 'Mercedes', 'Honda', 'Ford', 'Hyundai', 'Toyota', 'BMW', 'Mercedes', 'Audi'],
        'models': ['Camry', 'X5', 'C-Class', 'Civic', 'Fusion', 'Elantra', 'Corolla', '3 Series', 'E-Class', 'A4'],
        'years': [2023, 2022, 2023, 2024, 2022, 2024, 2024, 2023, 2022, 2023],
        'quantities': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    }

    priority_list = rank_cars_by_profit(
        car_makes=example_cars['makes'], car_models=example_cars['models'],
        car_years=example_cars['years'], quantities=example_cars['quantities'],
        target_month=next_month_name, target_year=next_month_year,
        sales_region='East', top_n=10
    )

    print("\n" + "=" * 70)
    print("TOP 10 CARS BY EXPECTED PROFIT")
    print("=" * 70)
    
    print(priority_list.to_string(index=False))