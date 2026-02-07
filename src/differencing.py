"""
Time Series Differencing

This module applies first-order differencing to remove trend
and make the time series stationary for SARIMA modeling.

Differencing: Y'(t) = Y(t) - Y(t-1)

Usage:
    python src/differencing.py
"""
import pandas as pd
from pathlib import Path
from statsmodels.tsa.stattools import adfuller
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

def difference_series(series):
    """
    Apply first-order differencing to remove trend.
    
    Computes Y(t) - Y(t-1) to stabilize the mean.
    
    Args:
        series: Time series data
    
    Returns:
        Differenced series with NaN values removed
    """
    return series.diff().dropna()

def adf_test(series, title=""):
    """
    Perform Augmented Dickey-Fuller test for stationarity.
    
    Args:
        series: Time series data to test
        title: Optional title for the test results
    
    Prints:
        ADF statistic and p-value
    """
    result = adfuller(series)
    print(f"\n--- ADF Test Results {title} ---")
    print(f"ADF Statistic: {result[0]}")
    print(f"p-value: {result[1]}")

def main():
    sales = load_monthly_sales()
    diff_sales = difference_series(sales)

    adf_test(sales, "Before Differencing")
    adf_test(diff_sales, "After Differencing")

if __name__ == "__main__":
    main()
