import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from prophet import Prophet
from prophet.plot import plot_plotly
from prophet.diagnostics import cross_validation, performance_metrics
import plotly.io as pio
from sklearn.preprocessing import StandardScaler
import joblib


# 1. Load the dataset
prophet_df = pd.read_csv("car_sales_2018_2024_prophet_df.csv")

prophet_df.info()

# Rename columns for Prophet
prophet_df.rename(columns={"Date": "ds", "Total_Sales": "y"}, inplace=True)

# Convert 'Season' to dummy variables for categorical regressors
season_dummies = pd.get_dummies(prophet_df["Season"], prefix="Season")
prophet_df = pd.concat([prophet_df, season_dummies], axis=1)
prophet_df.drop(columns=["Season"], inplace=True)


scaler = StandardScaler()
scaled_features = scaler.fit_transform(
    prophet_df[
        ["Sales_t-1", "Sales_t-3", "Rolling_3M", "Rolling_6M", "Cumulative_Sales"]
    ]
)
scaled_df = pd.DataFrame(
    scaled_features,
    columns=["Sales_t-1", "Sales_t-3", "Rolling_3M", "Rolling_6M", "Cumulative_Sales"],
)

# Create the Prophet model
model = Prophet(
    yearly_seasonality=True,
    weekly_seasonality=True,
    daily_seasonality=False,
    growth="linear",
    interval_width=0.9,
)

# Fit the model on the prepared data
model.fit(prophet_df)

df_cv = cross_validation(
    model, initial="1095 days", period="365 days", horizon="365 days"
)

df_p = performance_metrics(df_cv)
print(df_p.head())

# Create future DataFrame for next 12 months
future = model.make_future_dataframe(periods=12, freq="MS")  # MS = Month Start

# Make predictions
forecast = model.predict(future)
forecast[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(12)

# Plot the forecast
model.plot(forecast)
plt.show()

fig2 = model.plot_components(forecast)
plt.show()