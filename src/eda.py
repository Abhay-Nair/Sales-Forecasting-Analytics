"""
Exploratory Data Analysis for Sales Forecasting Project

This module performs basic EDA on cleaned sales data:
- Aggregates sales to monthly level
- Visualizes sales trends over time
- Provides summary statistics

Usage:
    python src/eda.py
"""
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt
import sys
from config import CLEANED_SALES_FILE, FIGURE_SIZE

def load_clean_data(path: Path) -> pd.DataFrame:
    """
    Load cleaned sales data from CSV file.
    
    Args:
        path: Path to the cleaned CSV file
    
    Returns:
        DataFrame with cleaned sales data
    
    Raises:
        FileNotFoundError: If cleaned data doesn't exist
        ValueError: If required columns are missing
    """
    try:
        if not path.exists():
            raise FileNotFoundError(
                f"Cleaned data file not found: {path}\n"
                f"Please run data_cleaning.py first"
            )
        
        df = pd.read_csv(path, parse_dates=["order_date"])
        
        if df.empty:
            raise ValueError("Loaded data is empty")
        
        if "order_date" not in df.columns or "sales" not in df.columns:
            raise ValueError("Required columns (order_date, sales) not found")
        
        print(f"✓ Successfully loaded {len(df)} rows")
        return df
    
    except FileNotFoundError as e:
        print(f"✗ Error: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"✗ Error loading data: {e}")
        sys.exit(1)

def monthly_sales_trend(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate sales data to monthly level.
    
    Args:
        df: DataFrame with order_date and sales columns
    
    Returns:
        DataFrame with monthly aggregated sales
    """
    monthly_sales = (
        df
        .set_index("order_date")
        .resample("M")["sales"]
        .sum()
        .reset_index()
    )
    return monthly_sales

def plot_monthly_sales(monthly_sales: pd.DataFrame):
    """
    Plot monthly sales trend over time.
    
    Args:
        monthly_sales: DataFrame with order_date and sales columns
    """
    plt.figure(figsize=FIGURE_SIZE)
    plt.plot(monthly_sales["order_date"], monthly_sales["sales"])
    plt.title("Monthly Sales Trend")
    plt.xlabel("Date")
    plt.ylabel("Total Sales")
    plt.grid(True)
    plt.show()

def main():
    try:
        print("=" * 50)
        print("EXPLORATORY DATA ANALYSIS")
        print("=" * 50)
        
        df = load_clean_data(CLEANED_SALES_FILE)
        monthly_sales = monthly_sales_trend(df)

        print("\n--- Monthly Sales (Top 10 Rows) ---")
        print(monthly_sales.head(10))

        print(f"\nTotal months: {len(monthly_sales)}")
        print(f"Date range: {monthly_sales['order_date'].min()} to {monthly_sales['order_date'].max()}")

        plot_monthly_sales(monthly_sales)
        
        print("\n✓ EDA completed successfully")
        
    except Exception as e:
        print(f"\n✗ EDA failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
