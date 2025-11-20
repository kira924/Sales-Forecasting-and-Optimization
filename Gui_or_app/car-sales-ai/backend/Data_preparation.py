import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

# ============================================
# STEP 1: Load and Explore Data
# ============================================

# Load your data
df = pd.read_csv("car_sales_Next_Year_Sales_prediction_ML_df.csv")

# Basic info
print("=" * 60)
print("DATA OVERVIEW")
print("=" * 60)
print(f"Total Records: {len(df):,}")
print(f"Total Features: {df.shape[1]}")
print(f"\nTarget Variable Statistics (Profit_Clean):")
print(df['Profit_Clean'].describe())

# ============================================
# STEP 2: Check for Missing Values & Outliers
# ============================================

print("\n" + "=" * 60)
print("DATA QUALITY CHECK")
print("=" * 60)

# Missing values
missing = df.isnull().sum()
if missing.sum() > 0:
    print("\nMissing Values Found:")
    print(missing[missing > 0])
else:
    print("\n✓ No missing values found!")

# Check for outliers in target variable using IQR method
Q1 = df['Profit_Clean'].quantile(0.25)
Q3 = df['Profit_Clean'].quantile(0.75)
IQR = Q3 - Q1
lower_bound = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR

outliers = df[(df['Profit_Clean'] < lower_bound) | (df['Profit_Clean'] > upper_bound)]
print(f"\nOutliers in Profit_Clean: {len(outliers):,} ({len(outliers)/len(df)*100:.2f}%)")

# ============================================
# STEP 3: Feature Selection
# ============================================

print("\n" + "=" * 60)
print("FEATURE SELECTION")
print("=" * 60)

# Define features to use for modeling
# Exclude: Date, Names, and target variable
exclude_cols = [
    # Identifiers and dates
    'Date', 'Salesperson', 'Customer Name',
    
    # Target variables
    'Profit', 'Profit_Clean',
    
    # LEAKAGE FEATURES (calculated from or directly related to profit)
    'Sale Price',           # Profit = Sale Price - Cost
    'Cost',                 # Directly used to calculate profit
    'Total_Sales',          # Derived from Sale Price
    'Commission Earned',    # Calculated from profit
    'Profit Margin',        # Profit / Sale Price
    'Loss',                 # Inverse of profit
    'Discount',             # Affects final price (leakage)
    'Commission Rate',      # Related to commission/profit
    'Discount per Car Age', # Derived feature with discount
    
    # Categorical (will encode separately or exclude)
    'Sale Month', 'Season', 'Customer Age Group', 
    # 'Sale Month Num',
    'Discount_Bracket', 'Payment Method', 'Sales Region'
    # ,'Customer Age','Customer Gender'
]

# Select numeric and boolean features
feature_cols = [col for col in df.columns if col not in exclude_cols]

print(f"\nTotal Features Selected: {len(feature_cols)}")
print("\nFeature Categories:")
print(f"  - Numerical: {len([col for col in feature_cols if df[col].dtype in ['float64', 'int64']])}")
print(f"  - Boolean: {len([col for col in feature_cols if df[col].dtype == 'bool'])}")

# Display selected features
print("\nSelected Features:")
for i, col in enumerate(feature_cols, 1):
    print(f"  {i}. {col} ({df[col].dtype})")

# ============================================
# STEP 4: Prepare X and y
# ============================================

X = df[feature_cols].copy()
y = df['Profit_Clean'].copy()

# Convert boolean columns to int (0/1)
bool_cols = X.select_dtypes(include=['bool']).columns
X[bool_cols] = X[bool_cols].astype(int)

print("\n" + "=" * 60)
print("DATASET PREPARATION COMPLETE")
print("=" * 60)
print(f"\nX shape: {X.shape}")
print(f"y shape: {y.shape}")
print(f"\nX dtypes summary:")
print(X.dtypes.value_counts())

# ============================================
# STEP 5: Train-Test Split
# ============================================

X_train, X_test, y_train, y_test = train_test_split(
    X, y, 
    test_size=0.2, 
    random_state=42,
    shuffle=True
)

print("\n" + "=" * 60)
print("TRAIN-TEST SPLIT")
print("=" * 60)
print(f"Training Set: {X_train.shape[0]:,} samples ({X_train.shape[0]/len(X)*100:.1f}%)")
print(f"Testing Set:  {X_test.shape[0]:,} samples ({X_test.shape[0]/len(X)*100:.1f}%)")

# ============================================
# STEP 6: Feature Scaling 
# ============================================

# Identify columns that need scaling (exclude already scaled boolean features)
cols_to_scale = X_train.select_dtypes(include=['float64', 'int64']).columns.tolist()

scaler = StandardScaler()
X_train_scaled = X_train.copy()
X_test_scaled = X_test.copy()

X_train_scaled[cols_to_scale] = scaler.fit_transform(X_train[cols_to_scale])
X_test_scaled[cols_to_scale] = scaler.transform(X_test[cols_to_scale])

print("\n" + "=" * 60)
print("FEATURE SCALING COMPLETE")
print("=" * 60)
print(f"Scaled {len(cols_to_scale)} numerical features")

# ============================================
# STEP 7: Quick EDA on Target Variable
# ============================================

fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Distribution of Profit_Clean
axes[0].hist(df['Profit_Clean'], bins=50, edgecolor='black', alpha=0.7)
axes[0].set_title('Distribution of Profit_Clean', fontsize=14, fontweight='bold')
axes[0].set_xlabel('Profit')
axes[0].set_ylabel('Frequency')
axes[0].axvline(df['Profit_Clean'].mean(), color='red', linestyle='--', label=f'Mean: {df["Profit_Clean"].mean():.2f}')
axes[0].axvline(df['Profit_Clean'].median(), color='green', linestyle='--', label=f'Median: {df["Profit_Clean"].median():.2f}')
axes[0].legend()
axes[0].grid(alpha=0.3)

# Box plot
axes[1].boxplot(df['Profit_Clean'], vert=True)
axes[1].set_title('Boxplot of Profit_Clean', fontsize=14, fontweight='bold')
axes[1].set_ylabel('Profit')
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()

print("\n" + "=" * 60)
print("✓ DATA PREPARATION PHASE COMPLETE")
print("=" * 60)
print("\nNext Step: Model Training & Evaluation")
print("Ready to proceed with Phase 2!")




# ============================================
# ADVANCED FEATURE ENGINEERING
# Goal: Create predictive features WITHOUT data leakage
# ============================================

print("=" * 60)
print("ADVANCED FEATURE ENGINEERING")
print("=" * 60)

# ============================================
# STEP 1: Historical Aggregates (Target Encoding)
# CRITICAL: Calculate on training data only to avoid leakage!
# ============================================

def create_target_encoding_features(df_train, df_test, target_col='Profit_Clean'):
    """
    Create historical average profit features for different groups
    MUST be calculated on training data only!
    """
    
    df_train_copy = df_train.copy()
    df_test_copy = df_test.copy()
    
    # 1. Average Profit by Car Make (historical)
    make_cols = [col for col in df_train.columns if col.startswith('Make_')]
    
    for make_col in make_cols:
        make_name = make_col.replace('Make_', '')
        # Calculate mean profit for this make in training data
        make_avg_profit = df_train_copy[df_train_copy[make_col] == 1][target_col].mean()
        
        # Apply to both train and test
        df_train_copy[f'Avg_Profit_{make_name}'] = df_train_copy[make_col] * make_avg_profit
        df_test_copy[f'Avg_Profit_{make_name}'] = df_test_copy[make_col] * make_avg_profit
    
    # Combine all make averages into single column
    make_avg_cols = [col for col in df_train_copy.columns if col.startswith('Avg_Profit_')]
    df_train_copy['Historical_Make_Avg_Profit'] = df_train_copy[make_avg_cols].sum(axis=1)
    df_test_copy['Historical_Make_Avg_Profit'] = df_test_copy[make_avg_cols].sum(axis=1)
    
    # Drop individual make average columns
    df_train_copy = df_train_copy.drop(columns=make_avg_cols)
    df_test_copy = df_test_copy.drop(columns=make_avg_cols)
    
    # 2. Average Profit by Car Age Group
    df_train_copy['Car_Age_Group'] = pd.cut(df_train_copy['Car Age'], 
                                              bins=[0, 1, 2, 3, 5, 100],
                                              labels=['New', '1-2Y', '2-3Y', '3-5Y', '5Y+'])
    df_test_copy['Car_Age_Group'] = pd.cut(df_test_copy['Car Age'], 
                                             bins=[0, 1, 2, 3, 5, 100],
                                             labels=['New', '1-2Y', '2-3Y', '3-5Y', '5Y+'])
    
    age_group_avg = df_train_copy.groupby('Car_Age_Group')[target_col].mean().to_dict()
    df_train_copy['Historical_Age_Avg_Profit'] = df_train_copy['Car_Age_Group'].map(age_group_avg)
    df_test_copy['Historical_Age_Avg_Profit'] = df_test_copy['Car_Age_Group'].map(age_group_avg)
    
    # 3. Average Profit by Season
    season_cols = [col for col in df_train.columns if col.startswith('Season_')]
    for season_col in season_cols:
        season_name = season_col.replace('Season_', '')
        season_avg = df_train_copy[df_train_copy[season_col] == 1][target_col].mean()
        
        df_train_copy[f'Avg_Profit_{season_name}'] = df_train_copy[season_col] * season_avg
        df_test_copy[f'Avg_Profit_{season_name}'] = df_test_copy[season_col] * season_avg
    
    season_avg_cols = [col for col in df_train_copy.columns if col.startswith('Avg_Profit_') and any(s in col for s in ['Fall', 'Spring', 'Summer', 'Winter'])]
    df_train_copy['Historical_Season_Avg_Profit'] = df_train_copy[season_avg_cols].sum(axis=1)
    df_test_copy['Historical_Season_Avg_Profit'] = df_test_copy[season_avg_cols].sum(axis=1)
    
    df_train_copy = df_train_copy.drop(columns=season_avg_cols)
    df_test_copy = df_test_copy.drop(columns=season_avg_cols)
    
    # 4. Average Profit by Quarter
    quarter_avg = df_train_copy.groupby('Sale Quarter')[target_col].mean().to_dict()
    df_train_copy['Historical_Quarter_Avg_Profit'] = df_train_copy['Sale Quarter'].map(quarter_avg)
    df_test_copy['Historical_Quarter_Avg_Profit'] = df_test_copy['Sale Quarter'].map(quarter_avg)
    
    # 5. Average Profit by Year
    year_avg = df_train_copy.groupby('Sale Year')[target_col].mean().to_dict()
    df_train_copy['Historical_Year_Avg_Profit'] = df_train_copy['Sale Year'].map(year_avg)
    df_test_copy['Historical_Year_Avg_Profit'] = df_test_copy['Sale Year'].map(year_avg)
    
    # Drop temporary column
    df_train_copy = df_train_copy.drop(columns=['Car_Age_Group'])
    df_test_copy = df_test_copy.drop(columns=['Car_Age_Group'])
    
    return df_train_copy, df_test_copy

# ============================================
# STEP 2: Interaction Features
# ============================================

def create_interaction_features(df):
    """
    Create meaningful interaction features
    """
    df_copy = df.copy()
    
    # 1. Quantity × Car Age (older cars bought in bulk might have different profit)
    df_copy['Quantity_x_CarAge'] = df_copy['Quantity'] * df_copy['Car Age']
    
    # 2. Car Year × Sale Year (newer models in recent years)
    df_copy['CarYear_x_SaleYear'] = df_copy['Car Year'] * df_copy['Sale Year']
    
    # 3. Car Model Frequency × Quantity (popular models bought in quantity)
    df_copy['ModelFreq_x_Quantity'] = df_copy['Car_Model_Freq'] * df_copy['Quantity']
    
    # 4. Weekend × Quarter (weekend sales in different quarters)
    df_copy['Weekend_x_Quarter'] = df_copy['Is Weekend'] * df_copy['Sale Quarter']
    
    # 5. Customer Age × Car Age (age matching)
    df_copy['CustomerAge_x_CarAge'] = df_copy['Customer Age'] * df_copy['Car Age']
    
    return df_copy

# ============================================
# STEP 3: Polynomial Features (Limited)
# ============================================

def create_polynomial_features(df):
    """
    Create polynomial features for key variables
    """
    df_copy = df.copy()
    
    # Square of important features
    df_copy['Car_Age_Squared'] = df_copy['Car Age'] ** 2
    df_copy['Quantity_Squared'] = df_copy['Quantity'] ** 2
    df_copy['Customer_Age_Squared'] = df_copy['Customer Age'] ** 2
    
    # Log transformations (for skewed features)
    df_copy['Log_Car_Model_Freq'] = np.log1p(df_copy['Car_Model_Freq'])
    df_copy['Log_Customer_Age'] = np.log1p(df_copy['Customer Age'])
    
    return df_copy

# ============================================
# STEP 4: Time-based Features
# ============================================

def create_time_features(df):
    """
    Create time-based features
    """
    df_copy = df.copy()
    
    # 1. Years since car was new
    df_copy['Years_Since_New'] = df_copy['Sale Year'] - df_copy['Car Year']
    
    # 2. Is Recent Sale Year (2023-2024)
    df_copy['Is_Recent_Year'] = (df_copy['Sale Year'] >= 2023).astype(int)
    
    # 3. Is New Car (less than 1 year old)
    df_copy['Is_New_Car'] = (df_copy['Car Age'] <= 1).astype(int)
    
    # 4. Quarter Sin/Cos encoding (cyclical)
    df_copy['Quarter_Sin'] = np.sin(2 * np.pi * df_copy['Sale Quarter'] / 4)
    df_copy['Quarter_Cos'] = np.cos(2 * np.pi * df_copy['Sale Quarter'] / 4)
    
    # 5. Month Sin/Cos encoding (cyclical)
    df_copy['Month_Sin'] = np.sin(2 * np.pi * df_copy['Sale Month Num'] / 12)
    df_copy['Month_Cos'] = np.cos(2 * np.pi * df_copy['Sale Month Num'] / 12)
    
    return df_copy

# ============================================
# STEP 5: Apply All Feature Engineering
# ============================================

# IMPORTANT: Add target column temporarily for target encoding
X_train_with_target = X_train.copy()
X_train_with_target['Profit_Clean'] = y_train

X_test_with_target = X_test.copy()
X_test_with_target['Profit_Clean'] = y_test

print("\n1. Creating Target Encoding Features (Historical Averages)...")
X_train_enhanced, X_test_enhanced = create_target_encoding_features(
    X_train_with_target, 
    X_test_with_target, 
    'Profit_Clean'
)

# Remove the target column after feature engineering
X_train_enhanced = X_train_enhanced.drop(columns=['Profit_Clean'])
X_test_enhanced = X_test_enhanced.drop(columns=['Profit_Clean'])

print(f"   ✓ Added {X_train_enhanced.shape[1] - X_train.shape[1]} new features")

print("\n2. Creating Interaction Features...")
X_train_enhanced = create_interaction_features(X_train_enhanced)
X_test_enhanced = create_interaction_features(X_test_enhanced)
print(f"   ✓ Added 5 interaction features")

print("\n3. Creating Polynomial Features...")
X_train_enhanced = create_polynomial_features(X_train_enhanced)
X_test_enhanced = create_polynomial_features(X_test_enhanced)
print(f"   ✓ Added 5 polynomial features")

print("\n4. Creating Time-based Features...")
X_train_enhanced = create_time_features(X_train_enhanced)
X_test_enhanced = create_time_features(X_test_enhanced)
print(f"   ✓ Added 8 time features")

# ============================================
# STEP 6: Handle Missing Values (NaN)
# ============================================

print("\n5. Checking for Missing Values...")

# Check for NaN in train and test
train_nan_count = X_train_enhanced.isnull().sum().sum()
test_nan_count = X_test_enhanced.isnull().sum().sum()

if train_nan_count > 0 or test_nan_count > 0:
    print(f"   ⚠ Found {train_nan_count} NaN values in train, {test_nan_count} in test")
    print("   ✓ Handling NaN values...")
    
    # Fill NaN differently based on column type
    for col in X_train_enhanced.columns:
        if X_train_enhanced[col].dtype.name == 'category':
            # For categorical columns, drop them (they're temporary)
            print(f"   ⚠ Dropping categorical column: {col}")
            X_train_enhanced = X_train_enhanced.drop(columns=[col])
            X_test_enhanced = X_test_enhanced.drop(columns=[col])
        elif X_train_enhanced[col].isnull().any():
            # For numeric columns, fill with 0
            X_train_enhanced[col] = X_train_enhanced[col].fillna(0)
            X_test_enhanced[col] = X_test_enhanced[col].fillna(0)
    
    print("   ✓ All NaN values handled!")
else:
    print("   ✓ No missing values found!")

# Convert boolean columns to int (if any)
bool_cols = X_train_enhanced.select_dtypes(include=['bool']).columns
if len(bool_cols) > 0:
    X_train_enhanced[bool_cols] = X_train_enhanced[bool_cols].astype(int)
    X_test_enhanced[bool_cols] = X_test_enhanced[bool_cols].astype(int)

print("\n" + "=" * 60)
print("FEATURE ENGINEERING SUMMARY")
print("=" * 60)
print(f"Original Features:  {X_train.shape[1]}")
print(f"Enhanced Features:  {X_train_enhanced.shape[1]}")
print(f"New Features Added: {X_train_enhanced.shape[1] - X_train.shape[1]}")

print("\nNew Feature Categories:")
new_features = [col for col in X_train_enhanced.columns if col not in X_train.columns]
print(f"  - Historical Averages: {len([f for f in new_features if 'Historical' in f or 'Avg' in f])}")
print(f"  - Interactions: {len([f for f in new_features if '_x_' in f])}")
print(f"  - Polynomial: {len([f for f in new_features if 'Squared' in f or 'Log' in f])}")
print(f"  - Time-based: {len([f for f in new_features if any(x in f for x in ['Years', 'Recent', 'New', 'Sin', 'Cos'])])}")

print("\n" + "=" * 60)
print("✓ ADVANCED FEATURE ENGINEERING COMPLETE")
print("=" * 60)
print("\nReady for Model Training!")

# Display data quality
print("\nData Quality Check:")
print(f"  Train Shape: {X_train_enhanced.shape}")
print(f"  Test Shape:  {X_test_enhanced.shape}")
print(f"  Train NaN:   {X_train_enhanced.isnull().sum().sum()}")
print(f"  Test NaN:    {X_test_enhanced.isnull().sum().sum()}")
print(f"  Train Inf:   {np.isinf(X_train_enhanced.select_dtypes(include=[np.number])).sum().sum()}")
print(f"  Test Inf:    {np.isinf(X_test_enhanced.select_dtypes(include=[np.number])).sum().sum()}")