import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
import time
import joblib
import os
import json
from datetime import datetime
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from Data_preparation import X_train, X_test, X_train_enhanced, X_test_enhanced, y_test, y_train
import warnings
warnings.filterwarnings('ignore')



# ============================================
# STEP 1: Create and Fit a Full Preprocessor
# ============================================
print("=" * 60)
print("CREATING AND FITTING PREPROCESSOR")
print("=" * 60)

preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), 
         make_column_selector(dtype_include='object')),
        ('num', StandardScaler(), 
         make_column_selector(dtype_include=np.number))
    ],
    remainder='passthrough',
    n_jobs=1,              
    verbose=True 
)

print("Fitting preprocessor on X_train_enhanced...")
preprocessor.fit(X_train_enhanced)

# Create a "models" folder if it doesn't already exist
output_dir = 'models/'
os.makedirs(output_dir, exist_ok=True)

joblib.dump(preprocessor, os.path.join(output_dir, 'full_preprocessor.pkl'))
print("\nPreprocessor fitted and saved as 'models/full_preprocessor.pkl'")

print("\nTransforming data...")
X_train_processed = preprocessor.transform(X_train_enhanced)
X_test_processed = preprocessor.transform(X_test_enhanced)
print(f"Data transformed successfully. New shape: {X_train_processed.shape}")


# ============================================
# STEP 2: Define Models to Compare
# ============================================
models = {
    'Linear Regression': LinearRegression(),
    'Random Forest': RandomForestRegressor(n_estimators=100, max_depth=20, min_samples_split=10, min_samples_leaf=5, random_state=42, n_jobs=-1),
    'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, max_depth=7, learning_rate=0.1, random_state=42),
    'XGBoost': XGBRegressor(n_estimators=100, max_depth=7, learning_rate=0.1, random_state=42, n_jobs=-1),
    'LightGBM': LGBMRegressor(n_estimators=100, max_depth=7, learning_rate=0.1, random_state=42, n_jobs=-1, verbose=-1)
}

# ============================================
# STEP 3: Train and Evaluate Each Model
# ============================================
results = []
for name, model in models.items():
    print(f"\n{'='*60}")
    print(f"Training: {name}")
    print(f"{'='*60}")
    start_time = time.time()
    
    model.fit(X_train_processed, y_train)
    
    y_pred_train = model.predict(X_train_processed)
    y_pred_test = model.predict(X_test_processed)
    
    train_mae = mean_absolute_error(y_train, y_pred_train)
    test_mae = mean_absolute_error(y_test, y_pred_test)
    train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
    test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
    train_r2 = r2_score(y_train, y_pred_train)
    test_r2 = r2_score(y_test, y_pred_test)
    train_mape = np.mean(np.abs((y_train - y_pred_train) / y_train)) * 100
    test_mape = np.mean(np.abs((y_test - y_pred_test) / y_test)) * 100
    training_time = time.time() - start_time
    results.append({'Model': name, 'Train MAE': train_mae, 'Test MAE': test_mae, 'Train RMSE': train_rmse, 'Test RMSE': test_rmse, 'Train R²': train_r2, 'Test R²': test_r2, 'Train MAPE': train_mape, 'Test MAPE': test_mape, 'Training Time (s)': training_time})
    print(f"\nResults:\n  Train MAE:  ${train_mae:,.2f}\n  Test MAE:   ${test_mae:,.2f}\n  Train RMSE: ${train_rmse:,.2f}\n  Test RMSE:  ${test_rmse:,.2f}\n  Train R²:   {train_r2:.4f}\n  Test R²:    {test_r2:.4f}\n  Train MAPE: {train_mape:.2f}%\n  Test MAPE:  {test_mape:.2f}%\n  Time:       {training_time:.2f}s")

# ============================================
# STEP 4: Compare Results
# ============================================
results_df = pd.DataFrame(results).sort_values('Test R²', ascending=False).reset_index(drop=True)
print("\n" + "=" * 60)
print("MODEL COMPARISON SUMMARY")
print("=" * 60)
print(results_df.to_string(index=False))


# ============================================
# STEP 6: Select Best Model
# ============================================
best_model_name = results_df.iloc[0]['Model']
best_model = models[best_model_name]
best_model_r2 = results_df.iloc[0]['Test R²']
best_model_mae = results_df.iloc[0]['Test MAE']
print(f"\nBest Model Selected: {best_model_name}")

# ============================================
# STEP 7: Feature Importance
# ============================================
if hasattr(best_model, 'feature_importances_'):
    print("\n" + "=" * 60)
    print("TOP 15 MOST IMPORTANT FEATURES")
    print("=" * 60)
    
    feature_names = preprocessor.get_feature_names_out()
    
    feature_importance = pd.DataFrame({
        'Feature': feature_names,
        'Importance': best_model.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    print(feature_importance.head(15).to_string(index=False))


# ============================================
# SAVING RANKING MODEL AND ARTIFACTS
# ============================================
print("\n" + "=" * 70)
print("SAVING RANKING MODEL AND ARTIFACTS")
print("=" * 70)

# 1. Save the best model
joblib.dump(best_model, os.path.join(output_dir, 'priority_ranking_model.pkl'))
print(f"Best model ({best_model_name}) saved: priority_ranking_model.pkl")

# 2. Save feature columns
feature_columns = X_train_enhanced.columns.tolist()
with open(os.path.join(output_dir, 'model_features.json'), 'w') as f:
    json.dump(feature_columns, f)
print(f"{len(feature_columns)} Original features saved: model_features.json")

# 3. Save historical averages
print("Calculating and saving historical averages...")
historical_data = {
    'make_avg_profit': {}, 'age_avg_profit': {}, 'season_avg_profit': {},
    'quarter_avg_profit': {}, 'year_avg_profit': {},
    'overall_mean': float(y_train.mean())
}

X_temp = X_train_enhanced.reset_index(drop=True)
y_temp = y_train.reset_index(drop=True)

# By Make
for make_col in [col for col in X_temp.columns if col.startswith('Make_')]:
    make_name = make_col.replace('Make_', '')
    mask = X_temp[make_col] == 1
    if mask.sum() > 0:
        historical_data['make_avg_profit'][make_name] = float(y_temp[mask].mean())

# By Age Group
age_bins = [0, 1, 2, 3, 5, 100]
age_labels = ['New', '1-2Y', '2-3Y', '3-5Y', '5Y+']
X_temp['Car_Age_Group'] = pd.cut(X_temp['Car Age'], bins=age_bins, labels=age_labels)
for age_group in age_labels:
    mask = X_temp['Car_Age_Group'] == age_group
    if mask.sum() > 0:
        historical_data['age_avg_profit'][age_group] = float(y_temp[mask].mean())

# By Season
for season in ['Fall', 'Spring', 'Summer', 'Winter']:
    season_col = f'Season_{season}'
    if season_col in X_temp.columns:
        mask = X_temp[season_col] == 1
        if mask.sum() > 0:
            historical_data['season_avg_profit'][season] = float(y_temp[mask].mean())

with open(os.path.join(output_dir, 'historical_averages.json'), 'w') as f:
    json.dump(historical_data, f, indent=2)
print("Historical data saved: historical_averages.json")

# 4. Save Combined Metadata
print("Saving combined system metadata...")
system_metadata = {
    'system_name': 'Car Dealership Analytics System', 'version': '1.0.0',
    'created_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    'models': {
        'priority_ranking': {
            'type': best_model_name,
            'file': 'priority_ranking_model.pkl',
            'test_r2': best_model_r2,
            'test_mae': best_model_mae,
            'features_count': len(feature_names) 
        },
        'sales_forecast': {
            'type': 'Prophet', 'file': 'prophet_sales_model.pkl'
        }
    }
}
with open(os.path.join(output_dir, 'system_metadata.json'), 'w') as f:
    json.dump(system_metadata, f, indent=2)
print("System metadata saved: system_metadata.json")

# 5. Create Requirements File
print("Creating Requirements File...")
requirements = """# Core ML Libraries
pandas
numpy
scikit-learn
xgboost
lightgbm
prophet
joblib

# Web Framework (choose one)
streamlit
# OR
fastapi
uvicorn
pydantic
"""
with open('requirements.txt', 'w') as f:
    f.write(requirements)
print("Requirements saved: requirements.txt")

print("\n" + "=" * 70)
print("The best model/Ranking training and saving complete!")
print("=" * 70)