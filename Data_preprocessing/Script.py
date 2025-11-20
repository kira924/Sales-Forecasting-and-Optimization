import pandas as pd
import numpy as np




# 1. Load the dataset
file_path = "car_sales_2018_2024.csv"
df_dirty = pd.read_csv(file_path)

# Make a copy to work on
df = df_dirty.copy()


# Section 3: Data Cleaning
# ----------- ------------
#### - Handle missing values
#### - Remove duplicates
#### - Handle Data Type Issues
#### - Handle Formatting Issues
#### - Handle outliers

# Visualize missingness
print("Missing values per column:")
print(df.isnull().sum())

# Handle missing values
for col in df.columns:
    if df[col].dtype in ["int64", "float64"]:
        df[col] = df[col].fillna(df[col].median())  # numeric => median
    else:
        df[col] = df[col].fillna(df[col].mode()[0])  # categorical => mode

print("After fixing missing values:")
print(df.isnull().sum())


# 2. Remove duplicates
duplicates = df.duplicated().sum()
print(f"Number of duplicate rows: {duplicates}")

if duplicates > 0:
    df = df.drop_duplicates()
    print("Duplicates removed.")
    duplicates = df.duplicated().sum()
    print(f"Number of duplicate rows: {duplicates}")


# 4. Check Data Type Issues
df.dtypes

# Date: object to datetime64
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")

# Car Year: float64 to Int64 (nullable int)
df["Car Year"] = df["Car Year"].astype("Int64")

# Sale Year: float64 to Int64
df["Sale Year"] = df["Sale Year"].astype("Int64")

# Sale Quarter: float64 to Int64
df["Sale Quarter"] = df["Sale Quarter"].astype("Int64")

# Sale Month: object to Categorical
df["Sale Month"] = df["Sale Month"].astype("category")

# Add a new numeric column for months (1–12)
month_map = {
    "January": 1, "February": 2, "March": 3, "April": 4,
    "May": 5, "June": 6, "July": 7, "August": 8,
    "September": 9, "October": 10, "November": 11, "December": 12
}
df["Sale Month Num"] = df["Sale Month"].map(month_map)


# 5. Formatting Issues
print(df["Car Make"].unique())

df["Car Make"] = df["Car Make"].str.strip()
df["Car Make"] = df["Car Make"].str.title()
df["Car Make"].replace(["Nan", "NaN", ""], np.nan, inplace=True)
df = df.dropna(subset=["Car Make"])
print(df["Car Make"].unique())

# 6. Outliers Detection
numeric_cols = ['Car Year', 'Quantity', 'Sale Price' , 'Cost', 'Profit', 'Discount',
                 'Commission Rate', 'Commission Earned' , 'Sale Quarter', 'Sale Year']

Outliers = ['Profit', 'Sale Price', 'Cost']

# Remove outliers using IQR
for col in Outliers:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower = Q1 - 1.5 * IQR
    upper = Q3 + 1.5 * IQR
    df = df[(df[col] >= lower) & (df[col] <= upper)]

# If the profit is negative, we will consider it a loss.
df['Loss'] = df['Profit'].apply(lambda x: abs(x) if x < 0 else 0)
# if the profit is positive, it remains a profit.
df['Profit_Clean'] = df['Profit'].apply(lambda x: x if x > 0 else 0)

# Remove outliers based on domain knowledge
salesperson_counts = df["Salesperson"].value_counts()
print("Top 10 Salespersons by number of sales:")
print(salesperson_counts.head(10))

df = df[df["Salesperson"] != "Nancy Mercado"]

print("Top 10 Salespersons by number of sales:")
print(salesperson_counts.head(10))

df = df[df["Customer Name"] != "Michael Smith"]

# 7. Final Check
print("Final Shape:", df.shape)
df.info()
df.describe(include="all")

# Save cleaned dataset
df.to_csv("car_sales_2018_2024_Cleaned.csv", index=False)
print(" Cleaned dataset saved")