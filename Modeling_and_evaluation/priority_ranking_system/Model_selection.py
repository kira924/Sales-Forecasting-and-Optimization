import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import LabelEncoder
from sklearn.compose import ColumnTransformer, make_column_selector
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from xgboost import XGBRegressor
from lightgbm import LGBMRegressor
import time
import joblib
import warnings
warnings.filterwarnings('ignore')
from Data_preparation import X_train, X_test, X_train_enhanced, X_test_enhanced, y_test, y_train


# 1. Define the comprehensive preprocessor
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), 
         make_column_selector(dtype_include='object')),
        ('num', StandardScaler(), 
         make_column_selector(dtype_include=np.number))
    ],
    remainder='passthrough',
    n_jobs=-1,
    verbose=True
)

# 2. Fit the preprocessor on the training data
print("Fitting preprocessor on X_train_enhanced...")
preprocessor.fit(X_train_enhanced)

# 3. Save the fitted preprocessor
joblib.dump(preprocessor, 'full_preprocessor.pkl')
print("\nPreprocessor fitted and saved as 'full_preprocessor.pkl'")

# 4. Apply the preprocessor to create fully numeric datasets
print("\nTransforming data...")
X_train_processed = preprocessor.transform(X_train_enhanced)
X_test_processed = preprocessor.transform(X_test_enhanced)

print(f"Data transformed successfully. New shape: {X_train_processed.shape}")

# ============================================
# STEP 2: Define Models to Compare
# ============================================

print("\n" + "=" * 60)
print("MODEL TRAINING & COMPARISON")
print("=" * 60)

models = {
    'Linear Regression': LinearRegression(),
    'Random Forest': RandomForestRegressor(
        n_estimators=100,
        max_depth=20,
        min_samples_split=10,
        min_samples_leaf=5,
        random_state=42,
        n_jobs=-1
    ),
    'Gradient Boosting': GradientBoostingRegressor(
        n_estimators=100,
        max_depth=7,
        learning_rate=0.1,
        random_state=42
    ),
    'XGBoost': XGBRegressor(
        n_estimators=100,
        max_depth=7,
        learning_rate=0.1,
        random_state=42,
        n_jobs=-1
    ),
    'LightGBM': LGBMRegressor(
        n_estimators=100,
        max_depth=7,
        learning_rate=0.1,
        random_state=42,
        n_jobs=-1,
        verbose=-1
    )
}

# ============================================
# STEP 3: Train and Evaluate Each Model
# ============================================

results = []

for name, model in models.items():
    print(f"\n{'='*60}")
    print(f"Training: {name}")
    print(f"{'='*60}")
    
    # Start timer
    start_time = time.time()

    
    # # Train model
    model.fit(X_train_processed, y_train)


    # Make predictions
    y_pred_train = model.predict(X_train_processed)
    y_pred_test = model.predict(X_test_processed)

    
    # Calculate metrics
    train_mae = mean_absolute_error(y_train, y_pred_train)
    test_mae = mean_absolute_error(y_test, y_pred_test)
    
    train_rmse = np.sqrt(mean_squared_error(y_train, y_pred_train))
    test_rmse = np.sqrt(mean_squared_error(y_test, y_pred_test))
    
    train_r2 = r2_score(y_train, y_pred_train)
    test_r2 = r2_score(y_test, y_pred_test)
    
    # Calculate MAPE (Mean Absolute Percentage Error)
    train_mape = np.mean(np.abs((y_train - y_pred_train) / y_train)) * 100
    test_mape = np.mean(np.abs((y_test - y_pred_test) / y_test)) * 100
    
    # Training time
    training_time = time.time() - start_time
    
    # Store results
    results.append({
        'Model': name,
        'Train MAE': train_mae,
        'Test MAE': test_mae,
        'Train RMSE': train_rmse,
        'Test RMSE': test_rmse,
        'Train R²': train_r2,
        'Test R²': test_r2,
        'Train MAPE': train_mape,
        'Test MAPE': test_mape,
        'Training Time (s)': training_time
    })
    
    # Print results
    print(f"\nResults:")
    print(f"  Train MAE:  ${train_mae:,.2f}")
    print(f"  Test MAE:   ${test_mae:,.2f}")
    print(f"  Train RMSE: ${train_rmse:,.2f}")
    print(f"  Test RMSE:  ${test_rmse:,.2f}")
    print(f"  Train R²:   {train_r2:.4f}")
    print(f"  Test R²:    {test_r2:.4f}")
    print(f"  Train MAPE: {train_mape:.2f}%")
    print(f"  Test MAPE:  {test_mape:.2f}%")
    print(f"  Time:       {training_time:.2f}s")

# ============================================
# STEP 4: Compare Results
# ============================================

results_df = pd.DataFrame(results)
results_df = results_df.sort_values('Test R²', ascending=False).reset_index(drop=True)

print("\n" + "=" * 60)
print("MODEL COMPARISON SUMMARY")
print("=" * 60)
print(results_df.to_string(index=False))

# ============================================
# STEP 5: Visualize Model Comparison
# ============================================

fig, axes = plt.subplots(2, 2, figsize=(16, 10))

# 1. R² Score Comparison
ax1 = axes[0, 0]
x_pos = np.arange(len(results_df))
width = 0.35
ax1.bar(x_pos - width/2, results_df['Train R²'], width, label='Train R²', alpha=0.8)
ax1.bar(x_pos + width/2, results_df['Test R²'], width, label='Test R²', alpha=0.8)
ax1.set_xlabel('Model', fontweight='bold')
ax1.set_ylabel('R² Score', fontweight='bold')
ax1.set_title('R² Score Comparison (Higher is Better)', fontsize=12, fontweight='bold')
ax1.set_xticks(x_pos)
ax1.set_xticklabels(results_df['Model'], rotation=45, ha='right')
ax1.legend()
ax1.grid(axis='y', alpha=0.3)

# 2. MAE Comparison
ax2 = axes[0, 1]
ax2.bar(x_pos - width/2, results_df['Train MAE'], width, label='Train MAE', alpha=0.8)
ax2.bar(x_pos + width/2, results_df['Test MAE'], width, label='Test MAE', alpha=0.8)
ax2.set_xlabel('Model', fontweight='bold')
ax2.set_ylabel('MAE ($)', fontweight='bold')
ax2.set_title('Mean Absolute Error (Lower is Better)', fontsize=12, fontweight='bold')
ax2.set_xticks(x_pos)
ax2.set_xticklabels(results_df['Model'], rotation=45, ha='right')
ax2.legend()
ax2.grid(axis='y', alpha=0.3)

# 3. MAPE Comparison
ax3 = axes[1, 0]
ax3.bar(x_pos, results_df['Test MAPE'], alpha=0.8, color='coral')
ax3.set_xlabel('Model', fontweight='bold')
ax3.set_ylabel('MAPE (%)', fontweight='bold')
ax3.set_title('Mean Absolute Percentage Error on Test Set', fontsize=12, fontweight='bold')
ax3.set_xticks(x_pos)
ax3.set_xticklabels(results_df['Model'], rotation=45, ha='right')
ax3.grid(axis='y', alpha=0.3)

# 4. Training Time
ax4 = axes[1, 1]
ax4.bar(x_pos, results_df['Training Time (s)'], alpha=0.8, color='lightgreen')
ax4.set_xlabel('Model', fontweight='bold')
ax4.set_ylabel('Time (seconds)', fontweight='bold')
ax4.set_title('Training Time Comparison', fontsize=12, fontweight='bold')
ax4.set_xticks(x_pos)
ax4.set_xticklabels(results_df['Model'], rotation=45, ha='right')
ax4.grid(axis='y', alpha=0.3)

plt.tight_layout()
plt.show()

# ============================================
# STEP 6: Select Best Model
# ============================================

best_model_name = results_df.iloc[0]['Model']
best_model = models[best_model_name]

print("\n" + "=" * 60)
print("BEST MODEL SELECTED")
print("=" * 60)
print(f"Model: {best_model_name}")
print(f"Test R²: {results_df.iloc[0]['Test R²']:.4f}")
print(f"Test MAE: ${results_df.iloc[0]['Test MAE']:,.2f}")
print(f"Test MAPE: {results_df.iloc[0]['Test MAPE']:.2f}%")

# ============================================
# STEP 7: Feature Importance (for tree-based models)
# ============================================

if hasattr(best_model, 'feature_importances_'):
    print("\n" + "=" * 60)
    print("TOP 15 MOST IMPORTANT FEATURES")
    print("=" * 60)

    try:
        feature_names = preprocessor.get_feature_names_out()
    except Exception:
        print("Could not get feature names from preprocessor, using generic names.")
        feature_names = [f"feature_{i}" for i in range(len(best_model.feature_importances_))]

    feature_importance = pd.DataFrame({ 'Feature': feature_names, 
                                       'Importance': best_model.feature_importances_ }
                                       ).sort_values('Importance', ascending=False)
     
    print(feature_importance.head(15).to_string(index=False))
    # Visualize top 15 features
    plt.figure(figsize=(12, 6))
    top_features = feature_importance.head(15)
    plt.barh(range(len(top_features)), top_features['Importance'])
    plt.yticks(range(len(top_features)), top_features['Feature'])
    plt.xlabel('Importance', fontweight='bold')
    plt.title(f'Top 15 Feature Importances - {best_model_name}', fontsize=14, fontweight='bold')
    plt.gca().invert_yaxis()
    plt.grid(axis='x', alpha=0.3)
    plt.tight_layout()
    plt.show()

# ============================================
# STEP 8: Prediction vs Actual Plot
# ============================================

plt.figure(figsize=(10, 6))
sample_size = min(5000, len(y_test))
sample_indices = np.random.choice(len(y_test), sample_size, replace=False)

plt.scatter(y_test.iloc[sample_indices], 
           best_model.predict(X_test_processed.iloc[sample_indices]),
           alpha=0.3, s=10)
plt.plot([y_test.min(), y_test.max()], 
         [y_test.min(), y_test.max()], 
         'r--', lw=2, label='Perfect Prediction')
plt.xlabel('Actual Profit', fontweight='bold')
plt.ylabel('Predicted Profit', fontweight='bold')
plt.title(f'Actual vs Predicted Profit - {best_model_name}', fontsize=14, fontweight='bold')
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()

print("\n" + "=" * 60)
print("MODEL TRAINING PHASE COMPLETE")
print("=" * 60)
print("\nNext Step: Build Priority Ranking System")

# ============================================
# STEP 9: best_model saving 
# ============================================

joblib.dump(best_model, 'xgboost_profit_model.pkl')
print("best model saved")