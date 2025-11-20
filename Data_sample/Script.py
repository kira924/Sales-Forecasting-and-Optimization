#### Extract a sample representing the population

import pandas as pd
import numpy as np
from scipy import stats

# We take 100,000 random rows to represent the data.
df = pd.read_csv("car_sales_Next_Year_Sales_prediction_ML_df.csv")
df_sample = df.sample(n=100000, random_state=4)

# calculate sample statistics
def calculate_sample_stats(df_sample, num_cols):
    stats_dict = {}
    for col in num_cols:
        sample = df_sample[col]
        stats_dict[col] = {
            "mean": sample.mean(),
            "std": sample.std(),
            "n": len(sample)
        }
    return stats_dict

# 2. Calculate population means 
population_means = df.select_dtypes(include=['int64', 'float64']).mean().to_dict()

# 3. Calculate sample statistics
num_cols = df_sample.select_dtypes(include=[np.number]).columns
sample_stats = calculate_sample_stats(df_sample, num_cols)


# Hypothesis Testing: Two-Tailed One-Sample Z-Test 
z_test_results = []

for col in num_cols:
    # Get the pre-calculated statistics
    sample_mean = sample_stats[col]["mean"]
    sample_std = sample_stats[col]["std"]
    n = sample_stats[col]["n"]
    pop_mean = population_means.get(col, None)

    # Calculate Z-score and p-value
    if sample_std != 0:
        z_score = (sample_mean - pop_mean) / (sample_std / np.sqrt(n))
        p_value = 2 * (1 - stats.norm.cdf(abs(z_score))) # two-tailed
        test_used = "Z-Test"
        
        z_test_results.append({
            "Column": col,
            "Population Mean": round(pop_mean, 3),
            "Sample Mean": round(sample_mean, 3),
            "Test": test_used,
            "Z/T Score": round(z_score, 3),
            "p-value": round(p_value, 4),
            "Representative?": "Yes" if p_value > 0.05 else "No"
        })

z_df = pd.DataFrame(z_test_results)
print("Z-Test Results:")
print(z_df)

# Confidence Interval Calculation
ci_results = []

for col in num_cols:
    # Get the pre-calculated statistics
    sample_mean = sample_stats[col]["mean"]
    sample_std = sample_stats[col]["std"]
    n = sample_stats[col]["n"]
    pop_mean = population_means.get(col, None)

    # Calculate Confidence Interval
    confidence = 0.95
    se = sample_std / np.sqrt(n)
    z_val = stats.norm.ppf(1 - (1 - confidence) / 2)
    lower = sample_mean - z_val * se
    upper = sample_mean + z_val * se
    inside = lower <= pop_mean <= upper if pop_mean is not None else None
    
    ci_results.append({
        "Column": col,
        "Sample Mean": round(sample_mean, 3),
        f"{int(confidence*100)}% CI Lower": round(lower, 3),
        f"{int(confidence*100)}% CI Upper": round(upper, 3),
        "Population Mean": round(pop_mean, 3),
        "Inside Interval?": inside
    })

ci_df = pd.DataFrame(ci_results)
print("\nConfidence Interval Results:")
print(ci_df)

# Save Sample Dataset 
df_sample.to_csv("car_sales_Next_Year_Sales_prediction_ML_df_sample_100k.csv", index=False)
print("Sample dataset saved")
