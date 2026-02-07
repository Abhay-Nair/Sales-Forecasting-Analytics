"""
Stationarity Check for Time Series Data

This module performs the Augmented Dickey-Fuller (ADF) test
to check if the sales time series is stationary.

A stationary series has:
- Constant mean over time
- Constant variance over time
- No seasonality

Usage:
    python src/stationarity_check.py
"""
import pandas as pd
from statsmodels.tsa.stattools import adfuller
from pathlib import Path
from config import CLEANED_SALES_FILE

def load_monthly_sales():
    """
    Load and aggregate sales data to monthly level.
    
    Returns:
        Series with monthly aggregated sales indexed by date
    """
    df = pd.read_csv(CLEANED_SALES_FILE, parse_dates=["order_date"])
    monthly_sales = (
        df.set_index("order_date")
          .resample("M")["sales"]
          .sum()
    )
    return monthly_sales

def adf_test(series):
    """
    Perform Augmented Dickey-Fuller test for stationarity.
    
    Tests the null hypothesis that a unit root is present (non-stationary).
    
    Args:
        series: Time series data to test
    
    Prints:
        ADF statistic, p-value, and critical values
    """
    result = adfuller(series)
    print("\n--- ADF Test Results ---")
    print(f"ADF Statistic: {result[0]}")
    print(f"p-value: {result[1]}")
    print("Critical Values:")
    for key, value in result[4].items():
        print(f"   {key}: {value}")

def main():
    monthly_sales = load_monthly_sales()
    adf_test(monthly_sales)

if __name__ == "__main__":
    main()
