# Section 5: Feature Engineering
# ----------- ------------
#### - Extract features from date (Year, Month, Day, Weekday, etc.)
#### - Encode categorical variables
#### - Scaling if needed

import pandas as pd


# 1. Load the dataset
file_path = "car_sales_2018_2024_cleaned.csv"
df = pd.read_csv(file_path)

### Calculating Car Age
# This feature is crucial for identifying which older or newer
#  cars are in higher demand and understanding their impact on sales.

# Car Age
df['Car Age'] = df['Sale Year'] - df['Car Year']
invalid_car_age = df[df['Sale Year'] < df['Car Year']]
df.loc[df['Sale Year'] < df['Car Year'], 'Sale Year'] = df['Car Year']
df['Car Age'] = df['Sale Year'] - df['Car Year']


### Calculating Profit Margin per Sale
# This feature is key for identifying the most profitable sales 
# and where the dealership should focus its promotions.

# Profit Margin
df['Profit Margin'] = df['Profit'] / df['Sale Price']

df[df['Profit Margin'] < 0]
df[df['Profit Margin'] > 1]
df = df[(df["Profit Margin"] <= 1) & (df["Profit Margin"] >= 0)]

df[df['Profit Margin'] < 0]
df[df['Profit Margin'] > 1]
df['Profit Margin'] = df['Profit'] / df['Sale Price']


### Encoding Seasonal and Time-Based Features
# This helps in analyzing seasonality and sales trends throughout the year and week.

# Is Weekend
df['Is Weekend'] = df['Day of Week'].isin(['Saturday', 'Sunday']).astype(int)

# Season One-Hot Encoding
season_dummies = pd.get_dummies(df['Season'], prefix='Season')
df = pd.concat([df, season_dummies], axis=1)


### Customer Age Group Categorization
# Important for analyzing which age group buys which car type the most.

bins = [20, 30, 40, 50, 60, 71]
labels = ['20-30','31-40','41-50','51-60','61-70']
df['Customer Age Group'] = pd.cut(df['Customer Age'], bins=bins,
                                   labels=labels, right=False) # right=False includes left edge

### Discount relative to Car Age
# This shows the impact of discounts on profit, especially for older inventory.

df['Discount per Car Age'] = df['Discount'] / (df['Car Age'] + 1)  # +1 to avoid division by zero

# Check
print("Final Shape:", df.shape)
df.info()
df.describe(include="all")

### Save the dataset

df.to_csv("car_sales_2018_2024_Cleaned&EG.csv", index=False)
print(" EG dataset saved")


### Preparing the data for machine learning models


#### Sales forecasting "Prophet"

df = pd.read_csv("car_sales_2018_2024_Cleaned&Eg.csv")

df['Total_Sales'] = df['Sale Price'] * df['Quantity']

# 1. Aggregate monthly sales and keep useful columns from original df
monthly_sales = df.groupby(['Sale Year', 'Sale Month Num'], observed=False).agg({
    'Sale Price': 'sum'
}).reset_index()

# 2. Create a proper date column for time-series
monthly_sales['Date'] = pd.to_datetime(monthly_sales['Sale Year'].astype(str) + '-' + 
                                       monthly_sales['Sale Month Num'].astype(str) + '-01')

# 3. Sort by date
monthly_sales = monthly_sales.sort_values('Date')

# 4. Rename column for clarity
monthly_sales.rename(columns={'Sale Price': 'Total_Sales'}, inplace=True)

# 5. Create lag features (previous months sales)
monthly_sales['Sales_t-1'] = monthly_sales['Total_Sales'].shift(1)
monthly_sales['Sales_t-2'] = monthly_sales['Total_Sales'].shift(2)
monthly_sales['Sales_t-3'] = monthly_sales['Total_Sales'].shift(3)

def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Spring'
    elif month in [6, 7, 8]:
        return 'Summer'
    else:
        return 'Fall'

monthly_sales['Season'] = monthly_sales['Sale Month Num'].apply(get_season)

# 6. Create rolling mean features (moving averages)
monthly_sales['Rolling_3M'] = monthly_sales['Total_Sales'].rolling(window=3).mean()
monthly_sales['Rolling_6M'] = monthly_sales['Total_Sales'].rolling(window=6).mean()

# 7. Create the target: next month sales
monthly_sales['Next_Month_Sales'] = monthly_sales['Total_Sales'].shift(-1)

# 8. Drop rows with NaN values (first few rows because of lags/rolling)
monthly_sales = monthly_sales.dropna().reset_index(drop=True)

# Cumulative Sales per year
monthly_sales['Cumulative_Sales'] = monthly_sales.groupby('Sale Year')['Total_Sales'].cumsum()
monthly_sales['Sale Quarter'] = ((monthly_sales['Sale Month Num'].astype('int') - 1) // 3) + 1

# save the data for prophet
monthly_sales.to_csv("car_sales_2018_2024_prophet_df.csv", index=False)
print(" prophet dataset saved")


#### CAR DEALERSHIP PRIORITY RANKING SYSTEM
df = pd.read_csv("car_sales_2018_2024_Cleaned&Eg.csv")

# Target
df["Total_Sales"] = df["Quantity"] * df["Sale Price"]

features = [
    "Sale Year", "Sale Month Num", "Sale Quarter",
    "Day of Week", "Is Weekend",
    "Season_Fall","Season_Spring","Season_Summer","Season_Winter",
    "Car Make", "Car Model", "Car Year", "Car Age",
    "Discount", "Discount per Car Age", "Profit Margin",]

target = "Total_Sales"

ml_df = df[features + [target]].copy()

# One-Hot Encoding for Day of Week
day_encoded = pd.get_dummies(df['Day of Week'], prefix='Day')

# One-Hot Encoding for Car Make
car_make_encoded = pd.get_dummies(df['Car Make'], prefix='Make')

# Frequency Encoding for Car Model
car_model_encoded = df['Car Model'].map(df['Car Model'].value_counts(normalize=True)).to_frame()
car_model_encoded.columns = ['Car_Model_Freq']

# We collect the data together
df_encoded = pd.concat([df.drop(['Day of Week', 'Car Make', 'Car Model'], axis=1),
     day_encoded,
     car_make_encoded,
     car_model_encoded], axis=1)

print("Data after encoding is ready for ML")
print(df_encoded.head())

df_encoded.to_csv("car_sales_Next_Year_Sales_prediction_ML_df.csv", index=False)
print("ML dataset saved")