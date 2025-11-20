import pandas as pd
import numpy as np
from datetime import datetime
from Data_preparation import X_train_enhanced, y_train
from Model_selection import best_model
import warnings
warnings.filterwarnings('ignore')

# ============================================
# CAR DEALERSHIP PRIORITY RANKING SYSTEM
# Predict & Rank Cars by Expected Profit
# ============================================

print("=" * 70)
print(" CAR DEALERSHIP PRIORITY RANKING SYSTEM ")
print("=" * 70)

# ============================================
# STEP 1: Prepare the Trained Model & Encoders
# ============================================

print("\n Loading trained model and feature engineering pipeline...")

# Assume best_model (XGBoost) is already trained
# In production, you would load it like this:
# import joblib
# best_model = joblib.load('xgboost_profit_model.pkl')
# scaler = joblib.load('feature_scaler.pkl')
# X_train_enhanced columns saved for reference

# For now, we'll use the existing trained model
trained_model = best_model  # From previous training
feature_columns = X_train_enhanced.columns.tolist()

print(f"✓ Model loaded: XGBoost with R² = 0.7063")
print(f"✓ Features required: {len(feature_columns)}")

# Print diagnostic information about profit distribution
print("\n" + "=" * 70)
print(" PROFIT ANALYSIS FROM TRAINING DATA")
print("=" * 70)

y_temp = y_train.reset_index(drop=True)

print(f"\n Overall Profit Statistics:")
print(f"   Mean:     ${y_temp.mean():>10,.2f}")
print(f"   Median:   ${y_temp.median():>10,.2f}")
print(f"   Std Dev:  ${y_temp.std():>10,.2f}")
print(f"   Min:      ${y_temp.min():>10,.2f}")
print(f"   Max:      ${y_temp.max():>10,.2f}")

print(f"\n Profit Percentiles:")
for p in [10, 25, 50, 75, 90, 95, 99]:
    val = y_temp.quantile(p/100)
    print(f"   {p:2d}th percentile: ${val:>10,.2f}")

# Show averages by Make with counts
print("\n Average Profit by Car Make:")
X_temp = X_train_enhanced.reset_index(drop=True)
make_stats = []
for make_col in sorted([col for col in X_temp.columns if col.startswith('Make_')]):
    make_name = make_col.replace('Make_', '')
    mask = X_temp[make_col] == 1
    if mask.sum() > 0:
        avg = y_temp[mask].mean()
        median = y_temp[mask].median()
        count = mask.sum()
        make_stats.append({
            'Make': make_name,
            'Avg_Profit': avg,
            'Median': median,
            'Count': count
        })

make_df = pd.DataFrame(make_stats).sort_values('Avg_Profit', ascending=False)
for _, row in make_df.iterrows():
    print(f"   {row['Make']:12s}: Avg=${row['Avg_Profit']:>8,.0f}  Median=${row['Median']:>8,.0f}  ({row['Count']:>6,} cars)")

# Realistic profit check
realistic_min = 1000
realistic_max = 8000
realistic_count = ((y_temp >= realistic_min) & (y_temp <= realistic_max)).sum()
realistic_pct = realistic_count / len(y_temp) * 100

print(f"\n Reality Check:")
print(f"   Cars with profit ${realistic_min:,}-${realistic_max:,}: {realistic_count:,} ({realistic_pct:.1f}%)")
print(f"   Cars with profit > ${realistic_max:,}: {(y_temp > realistic_max).sum():,} ({(y_temp > realistic_max).sum()/len(y_temp)*100:.1f}%)")
print(f"   Cars with profit < ${realistic_min:,}: {(y_temp < realistic_min).sum():,} ({(y_temp < realistic_min).sum()/len(y_temp)*100:.1f}%)")

# ============================================
# STEP 2: Car Inventory Builder Function
# ============================================

def build_car_inventory(
    car_makes,
    car_models, 
    car_years,
    quantities,
    target_month,
    target_year,
    sales_region='East',
    customer_age_group='Adult',
    is_weekend=0
):
    """
    Build a DataFrame of cars to predict profits for
    
    Parameters:
    -----------
    car_makes : list
        List of car makes (e.g., ['Toyota', 'BMW', 'Honda'])
    car_models : list
        List of car models (e.g., ['Camry', 'X5', 'Civic'])
    car_years : list
        List of manufacturing years (e.g., [2023, 2022, 2024])
    quantities : list
        List of quantities (e.g., [1, 1, 2])
    target_month : str or int
        Target prediction month (e.g., 'November' or 11)
    target_year : int
        Target prediction year (e.g., 2024)
    sales_region : str
        Sales region (default: 'East')
    customer_age_group : str
        Customer age group (default: 'Adult')
    is_weekend : int
        0 for weekday, 1 for weekend (default: 0)
    
    Returns:
    --------
    DataFrame with all required features for prediction
    """
    
    # Validate inputs
    n_cars = len(car_makes)
    assert len(car_models) == n_cars, "car_models must match car_makes length"
    assert len(car_years) == n_cars, "car_years must match car_makes length"
    assert len(quantities) == n_cars, "quantities must match car_makes length"
    
    # Convert month to number if string
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
    
    # Determine season
    season_mapping = {
        12: 'Winter', 1: 'Winter', 2: 'Winter',
        3: 'Spring', 4: 'Spring', 5: 'Spring',
        6: 'Summer', 7: 'Summer', 8: 'Summer',
        9: 'Fall', 10: 'Fall', 11: 'Fall'
    }
    season = season_mapping[target_month_num]
    
    # Determine quarter
    quarter = (target_month_num - 1) // 3 + 1
    
    # Build base dataframe
    inventory_df = pd.DataFrame({
        'Car_Make': car_makes,
        'Car_Model': car_models,
        'Car Year': car_years,
        'Quantity': quantities,
        'Sale Year': target_year,
        'Sale Month': target_month_name,
        'Sale Month Num': target_month_num,
        'Sale Quarter': quarter,
        'Season': season,
        'Sales Region': sales_region,
        'Customer Age Group': customer_age_group,
        'Is Weekend': is_weekend
    })
    
    # Calculate Car Age
    inventory_df['Car Age'] = target_year - inventory_df['Car Year']
    
    # Add Customer Age (default average)
    inventory_df['Customer Age'] = 45.0  # Default average age
    
    # Add Customer Gender (default distribution: 60% Male, 40% Female)
    inventory_df['Customer Gender'] = np.random.choice([1, 0], size=n_cars, p=[0.6, 0.4])
    
    # Get Car_Model_Freq from training data (if available)
    # In production, you'd have a lookup table
    # For now, we'll use the average from training
    if 'Car_Model_Freq' in X_train_enhanced.columns:
        avg_freq = X_train_enhanced['Car_Model_Freq'].mean()
        inventory_df['Car_Model_Freq'] = avg_freq
    else:
        inventory_df['Car_Model_Freq'] = 100.0  # Default value
    
    return inventory_df

# ============================================
# STEP 3: Feature Engineering Pipeline
# ============================================

def engineer_features(inventory_df, historical_data=None):
    """
    Apply the same feature engineering as training
    
    Parameters:
    -----------
    inventory_df : DataFrame
        Raw inventory data
    historical_data : DataFrame (optional)
        Historical data for calculating averages
        
    Returns:
    --------
    DataFrame with all engineered features
    """
    
    df = inventory_df.copy()
    
    # One-hot encode Car Make
    make_dummies = pd.get_dummies(df['Car_Make'], prefix='Make')
    
    # Ensure all makes from training are present
    all_makes = [col.replace('Make_', '') for col in feature_columns if col.startswith('Make_')]
    for make in all_makes:
        col_name = f'Make_{make}'
        if col_name not in make_dummies.columns:
            make_dummies[col_name] = 0
    
    df = pd.concat([df, make_dummies], axis=1)
    
    # One-hot encode Season
    season_dummies = pd.get_dummies(df['Season'], prefix='Season')
    for season in ['Fall', 'Spring', 'Summer', 'Winter']:
        col_name = f'Season_{season}'
        if col_name not in season_dummies.columns:
            season_dummies[col_name] = 0
    
    df = pd.concat([df, season_dummies], axis=1)
    
    # One-hot encode Day (all zeros for now, can be customized)
    for day in ['Friday', 'Monday', 'Saturday', 'Sunday', 'Thursday', 'Tuesday', 'Wednesday']:
        df[f'Day_{day}'] = 0
    
    # Historical Averages (CRITICAL: Use actual training data!)
    # Calculate real averages from training data
    
    # Reset indices to avoid mismatch
    X_train_temp = X_train_enhanced.reset_index(drop=True)
    y_train_temp = y_train.reset_index(drop=True)
    
    # 1. Historical Make Average Profit
    make_profit_avg = {}
    for make_col in [col for col in X_train_temp.columns if col.startswith('Make_')]:
        make_name = make_col.replace('Make_', '')
        # Get average profit for this make from training data
        mask = X_train_temp[make_col] == 1
        if mask.sum() > 0:
            make_profit_avg[make_name] = y_train_temp[mask].mean()
        else:
            make_profit_avg[make_name] = y_train_temp.mean()
    
    # Apply to current inventory
    df['Historical_Make_Avg_Profit'] = df['Car_Make'].map(make_profit_avg).fillna(y_train_temp.mean())
    
    # 2. Historical Age Group Average
    age_bins = [0, 1, 2, 3, 5, 100]
    age_labels = ['New', '1-2Y', '2-3Y', '3-5Y', '5Y+']
    
    X_train_temp['Car_Age_Group'] = pd.cut(
        X_train_temp['Car Age'], 
        bins=age_bins, 
        labels=age_labels
    )
    
    age_profit_avg = {}
    for age_group in age_labels:
        mask = X_train_temp['Car_Age_Group'] == age_group
        if mask.sum() > 0:
            age_profit_avg[age_group] = y_train_temp[mask].mean()
        else:
            age_profit_avg[age_group] = y_train_temp.mean()
    
    df['Car_Age_Group_Temp'] = pd.cut(df['Car Age'], bins=age_bins, labels=age_labels)
    # Map first, then convert to float to allow fillna
    df['Historical_Age_Avg_Profit'] = df['Car_Age_Group_Temp'].map(age_profit_avg)
    df['Historical_Age_Avg_Profit'] = df['Historical_Age_Avg_Profit'].astype(float).fillna(y_train_temp.mean())
    df = df.drop(columns=['Car_Age_Group_Temp'])
    
    # 3. Historical Season Average
    season_profit_avg = {}
    for season in ['Fall', 'Spring', 'Summer', 'Winter']:
        season_col = f'Season_{season}'
        if season_col in X_train_temp.columns:
            mask = X_train_temp[season_col] == 1
            if mask.sum() > 0:
                season_profit_avg[season] = y_train_temp[mask].mean()
            else:
                season_profit_avg[season] = y_train_temp.mean()
    
    df['Historical_Season_Avg_Profit'] = df['Season'].map(season_profit_avg).fillna(y_train_temp.mean())
    
    # 4. Historical Quarter Average
    quarter_profit_avg = {}
    for quarter in X_train_temp['Sale Quarter'].unique():
        mask = X_train_temp['Sale Quarter'] == quarter
        if mask.sum() > 0:
            quarter_profit_avg[quarter] = y_train_temp[mask].mean()
        else:
            quarter_profit_avg[quarter] = y_train_temp.mean()
    
    df['Historical_Quarter_Avg_Profit'] = df['Sale Quarter'].map(quarter_profit_avg).fillna(y_train_temp.mean())
    
    # 5. Historical Year Average
    year_profit_avg = {}
    for year in X_train_temp['Sale Year'].unique():
        mask = X_train_temp['Sale Year'] == year
        if mask.sum() > 0:
            year_profit_avg[year] = y_train_temp[mask].mean()
        else:
            year_profit_avg[year] = y_train_temp.mean()
    
    df['Historical_Year_Avg_Profit'] = df['Sale Year'].map(year_profit_avg).fillna(y_train_temp.mean())
    
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
    
    # Log features
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
    
    # Select only required features in correct order
    feature_df = df[feature_columns].copy()
    
    # Fill any missing columns with 0
    for col in feature_columns:
        if col not in feature_df.columns:
            feature_df[col] = 0
    
    return feature_df, df

# ============================================
# STEP 4: Priority Ranking Function
# ============================================

def rank_cars_by_profit(
    car_makes,
    car_models,
    car_years,
    quantities,
    target_month,
    target_year,
    sales_region='East',
    top_n=None
):
    """
    Rank cars by predicted profit for given month
    
    Returns:
    --------
    DataFrame with cars ranked by predicted profit (highest first)
    """
    
    print(f"\n{'='*70}")
    print(f"PREDICTING PROFITS FOR {target_month.upper()} {target_year}")
    print(f"{'='*70}")
    
    # Build inventory
    print(f"\n Building inventory of {len(car_makes)} cars...")
    inventory_df = build_car_inventory(
        car_makes, car_models, car_years, quantities,
        target_month, target_year, sales_region
    )
    
    # Engineer features
    print(f"Engineering features...")
    features_df, full_df = engineer_features(inventory_df)
    
    # Make predictions
    print(f"Making predictions using XGBoost...")
    predictions = trained_model.predict(features_df)
    
    # Add predictions to dataframe
    full_df['Predicted_Profit'] = predictions
    
    # Calculate confidence score based on prediction uncertainty
    # Use model's feature importance and historical variance
    model_mae = 4432  # From training
    model_std = 5928  # Test RMSE from training
    
    # Calculate relative confidence (0-100%)
    # Higher profit relative to error = higher confidence
    full_df['Prediction_Error_Ratio'] = model_mae / full_df['Predicted_Profit']
    full_df['Confidence'] = np.clip(100 * (1 - full_df['Prediction_Error_Ratio']), 0, 100)
    
    # Calculate risk level based on BOTH profit AND prediction uncertainty
    # ADJUSTED FOR REALISTIC CAR DEALER PROFITS ($2K-$5K typical)
    def calculate_risk(row):
        profit = row['Predicted_Profit']
        confidence = row['Confidence']
        car_age = row['Car Age']
        
        # Factor 1: Profit level (REALISTIC dealer margins)
        if profit > 6000:           # Excellent profit (top 10%)
            profit_risk = 0         # Low risk
        elif profit > 4500:         # Good profit (above average)
            profit_risk = 1         # Medium risk
        elif profit > 3000:         # Acceptable profit
            profit_risk = 2         # Medium-High risk
        else:                       # Below average profit
            profit_risk = 3         # High risk
        
        # Factor 2: Confidence level (prediction accuracy)
        if confidence > 60:         # High confidence
            confidence_risk = 0     # Low risk
        elif confidence > 40:       # Moderate confidence
            confidence_risk = 1     # Medium risk
        elif confidence > 20:       # Low confidence
            confidence_risk = 2     # Medium-High risk
        else:                       # Very low confidence
            confidence_risk = 3     # High risk
        
        # Factor 3: Car age (newer = more predictable)
        if car_age == 0:            # Brand new
            age_risk = 0            # Low risk
        elif car_age <= 2:          # Nearly new
            age_risk = 1            # Medium risk
        elif car_age <= 4:          # Used
            age_risk = 2            # Medium-High risk
        else:                       # Old
            age_risk = 3            # High risk
        
        # Calculate overall risk score (0-9 scale)
        total_risk = profit_risk + confidence_risk + age_risk
        
        # Map to risk levels (ADJUSTED for more balanced distribution)
        if total_risk <= 3:         # 0-3: Low risk
            return 'Low'
        elif total_risk <= 6:       # 4-6: Medium risk
            return 'Medium'
        else:                       # 7-9: High risk
            return 'High'
    
    full_df['Risk_Level'] = full_df.apply(calculate_risk, axis=1)
    
    # Sort by predicted profit (descending)
    ranked_df = full_df.sort_values('Predicted_Profit', ascending=False).reset_index(drop=True)
    
    # Select relevant columns for output
    output_cols = [
        'Car_Make', 'Car_Model', 'Car Year', 'Car Age', 
        'Quantity', 'Sale Month', 'Season', 'Sales Region',
        'Predicted_Profit', 'Confidence', 'Risk_Level'
    ]
    
    result_df = ranked_df[output_cols].copy()
    result_df['Rank'] = range(1, len(result_df) + 1)
    
    # Limit to top N if specified
    if top_n:
        result_df = result_df.head(top_n)
    
    print(f"\nPredictions complete!")
    print(f" {len(result_df)} cars ranked by expected profit")
    
    return result_df

# ============================================
# STEP 5: EXAMPLE USAGE
# ============================================

print("\n" + "=" * 70)
print("EXAMPLE: NEXT MONTH CAR INVENTORY RANKING")
print("=" * 70)

# Get current date and calculate next month
from datetime import datetime, timedelta

current_date = datetime.now()
next_month_date = current_date + timedelta(days=32)
next_month_date = next_month_date.replace(day=1)

# Get month name and year
next_month_name = next_month_date.strftime('%B')
next_month_year = next_month_date.year

print(f"\n Current Date: {current_date.strftime('%B %d, %Y')}")
print(f"Predicting for: {next_month_name} {next_month_year}")

# Example: Dealership wants to buy these cars for next month
example_cars = {
    'makes': ['Toyota', 'BMW', 'Mercedes', 'Honda', 'Ford', 
              'Hyundai', 'Toyota', 'BMW', 'Mercedes', 'Audi'],
    'models': ['Camry', 'X5', 'C-Class', 'Civic', 'Fusion',
               'Elantra', 'Corolla', '3 Series', 'E-Class', 'A4'],
    'years': [2023, 2022, 2023, 2024, 2022,
              2024, 2024, 2023, 2022, 2023],
    'quantities': [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
}

# Get priority ranking for NEXT MONTH
priority_list = rank_cars_by_profit(
    car_makes=example_cars['makes'],
    car_models=example_cars['models'],
    car_years=example_cars['years'],
    quantities=example_cars['quantities'],
    target_month=next_month_name,
    target_year=next_month_year,
    sales_region='East',
    top_n=10
)

print("\n" + "=" * 70)
print("TOP 10 CARS BY EXPECTED PROFIT")
print("=" * 70)

# Add visual risk indicators
def risk_emoji(risk):
    if risk == 'Low':
        return 'Low'
    elif risk == 'Medium':
        return 'Medium'
    else:
        return 'High'

priority_display = priority_list.copy()
priority_display['Risk_Level'] = priority_display['Risk_Level'].apply(risk_emoji)
print(priority_display.to_string(index=False))

print("\n" + "=" * 70)
print(" SUMMARY STATISTICS")
print("=" * 70)
print(f"Total Expected Profit: ${priority_list['Predicted_Profit'].sum():,.2f}")
print(f"Average Profit per Car: ${priority_list['Predicted_Profit'].mean():,.2f}")
print(f"Highest Profit: ${priority_list['Predicted_Profit'].max():,.2f} ({priority_list.iloc[0]['Car_Make']} {priority_list.iloc[0]['Car_Model']})")
print(f"Lowest Profit: ${priority_list['Predicted_Profit'].min():,.2f}")
print(f"Average Confidence: {priority_list['Confidence'].mean():.1f}%")

print(f"\n Risk Distribution:")
risk_counts = priority_list['Risk_Level'].value_counts()
for risk_level in ['Low', 'Medium', 'High']:
    count = risk_counts.get(risk_level, 0)
    percentage = (count / len(priority_list) * 100) if len(priority_list) > 0 else 0
    emoji = 'L' if risk_level == 'Low' else 'M' if risk_level == 'Medium' else 'H'
    print(f"   {emoji} {risk_level:8s}: {count} cars ({percentage:.0f}%)")

# Investment recommendation
total_profit = priority_list['Predicted_Profit'].sum()
low_risk_profit = priority_list[priority_list['Risk_Level'] == 'Low']['Predicted_Profit'].sum()
medium_risk_profit = priority_list[priority_list['Risk_Level'] == 'Medium']['Predicted_Profit'].sum()

print(f"\n Investment Insights:")
print(f"    Low Risk Cars: ${low_risk_profit:,.2f} ({low_risk_profit/total_profit*100:.0f}% of total)")
print(f"    Medium Risk Cars: ${medium_risk_profit:,.2f} ({medium_risk_profit/total_profit*100:.0f}% of total)")

# Recommendations
low_risk_count = (priority_list['Risk_Level'] == 'Low').sum()
if low_risk_count >= 3:
    print(f"\n RECOMMENDATION: Focus on the {low_risk_count} low-risk vehicles for stable returns")
elif (priority_list['Risk_Level'] == 'Medium').sum() >= 5:
    print(f"\n  RECOMMENDATION: Portfolio has good balance but monitor medium-risk vehicles")
else:
    print(f"\n  RECOMMENDATION: High-risk portfolio - consider diversifying with premium brands")

print("\n" + "=" * 70)
print("✓ PRIORITY RANKING SYSTEM READY FOR DEPLOYMENT")
print("=" * 70)