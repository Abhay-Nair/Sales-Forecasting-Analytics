"""
Data Cleaning Pipeline for Sales Forecasting Project

This module handles the complete data cleaning workflow:
- Loading raw sales data
- Standardizing column names and data types
- Validating data quality
- Removing invalid records
- Saving cleaned data for downstream analysis

Usage:
    python src/data_cleaning.py
"""
import pandas as pd
from pathlib import Path
import sys
from config import (
    RAW_SALES_FILE,
    CLEANED_SALES_FILE,
    NUMERIC_COLUMNS,
    DATE_COLUMNS,
    DUPLICATE_SUBSET
)
from logger import setup_logger, log_section, log_success, log_error, log_warning

logger = setup_logger(__name__)

def load_data(path: Path) -> pd.DataFrame:
    """
    Load raw sales data from CSV file.
    
    Args:
        path: Path to the raw CSV file
    
    Returns:
        DataFrame with raw sales data
    
    Raises:
        FileNotFoundError: If the data file doesn't exist
        ValueError: If the loaded data is empty
    """
    try:
        if not path.exists():
            raise FileNotFoundError(f"Data file not found: {path}")
        
        df = pd.read_csv(path)
        
        if df.empty:
            raise ValueError("Loaded data is empty")
        
        log_success(logger, f"Successfully loaded {len(df)} rows from {path.name}")
        return df
    
    except FileNotFoundError as e:
        log_error(logger, str(e))
        logger.info(f"  Please ensure the raw data file exists at: {path}")
        sys.exit(1)
    except pd.errors.EmptyDataError:
        log_error(logger, f"The file {path} is empty")
        sys.exit(1)
    except Exception as e:
        log_error(logger, f"Unexpected error loading data: {e}")
        sys.exit(1)

def standardize_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Standardize column names to snake_case.
    
    Args:
        df: DataFrame with raw column names
    
    Returns:
        DataFrame with standardized column names
    """
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )
    return df

def parse_dates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert date columns to datetime format.
    
    Args:
        df: DataFrame with date columns as strings
    
    Returns:
        DataFrame with parsed datetime columns
    """
    df["order_date"] = pd.to_datetime(df["order_date"], errors="coerce")
    df["ship_date"] = pd.to_datetime(df["ship_date"], errors="coerce")
    return df

def convert_numeric_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Convert numeric columns to proper dtypes.
    
    Removes currency symbols and commas, then converts to numeric.
    
    Args:
        df: DataFrame with numeric columns as strings
    
    Returns:
        DataFrame with properly typed numeric columns
    """
    for col in NUMERIC_COLUMNS:
        df[col] = (
            df[col]
            .astype(str)
            .str.replace(",", "", regex=False)
            .str.replace("$", "", regex=False)
        )
        df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

def clean_invalid_records(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove invalid rows based on business rules.
    
    Removes:
    - Zero or negative sales
    - Missing order dates
    - Duplicate order IDs for same product
    
    Args:
        df: DataFrame with potentially invalid records
    
    Returns:
        DataFrame with only valid records
    """

    initial_rows = len(df)

    # Remove zero or negative sales
    df = df[df["sales"] > 0]

    # Remove missing order dates
    df = df.dropna(subset=["order_date"])

    # Remove true duplicates (same order + same product)
    df = df.drop_duplicates(subset=DUPLICATE_SUBSET)

    final_rows = len(df)

    logger.info("\n--- Cleaning Summary ---")
    logger.info(f"Rows before cleaning: {initial_rows}")
    logger.info(f"Rows after cleaning:  {final_rows}")
    logger.info(f"Rows removed:        {initial_rows - final_rows}")

    return df

def validate_data(df: pd.DataFrame) -> None:
    """
    Run comprehensive data validation checks and log results.
    
    Checks for:
    - Negative quantities
    - Zero or negative sales
    - Missing order dates
    - Duplicate order IDs
    - Future dates
    - Date range boundaries
    
    Args:
        df: DataFrame to validate
    """
    logger.info("\n--- Validation Report ---")

    # Basic validations
    logger.info("\nNegative quantities:")
    neg_qty = (df["quantity"] < 0).sum()
    logger.info(neg_qty)
    if neg_qty > 0:
        log_warning(logger, f"Found {neg_qty} records with negative quantities")

    logger.info("\nZero or negative sales:")
    zero_sales = (df["sales"] <= 0).sum()
    logger.info(zero_sales)
    if zero_sales > 0:
        log_warning(logger, f"Found {zero_sales} records with zero/negative sales")

    logger.info("\nMissing order dates:")
    missing_dates = df["order_date"].isna().sum()
    logger.info(missing_dates)
    if missing_dates > 0:
        log_warning(logger, f"Found {missing_dates} records with missing dates")

    logger.info("\nDuplicate order IDs:")
    duplicates = df["order_id"].duplicated().sum()
    logger.info(duplicates)
    if duplicates > 0:
        log_warning(logger, f"Found {duplicates} duplicate order IDs")
    
    # Enhanced validations
    logger.info("\n--- Enhanced Validations ---")
    
    # Check for future dates
    from datetime import datetime
    today = datetime.now()
    future_dates = (df["order_date"] > today).sum()
    logger.info(f"\nFuture dates: {future_dates}")
    if future_dates > 0:
        log_warning(logger, f"Found {future_dates} records with future dates")
    
    # Check date range
    if not df["order_date"].isna().all():
        min_date = df["order_date"].min()
        max_date = df["order_date"].max()
        logger.info(f"\nDate range: {min_date} to {max_date}")
        
        # Check if date range is reasonable (e.g., not before 2000)
        if min_date.year < 2000:
            log_warning(logger, f"Minimum date ({min_date}) seems unusually old")
    
    # Check for extreme values in sales
    if "sales" in df.columns:
        sales_mean = df["sales"].mean()
        sales_std = df["sales"].std()
        outliers = ((df["sales"] - sales_mean).abs() > 3 * sales_std).sum()
        logger.info(f"\nStatistical outliers (>3 std): {outliers}")
        if outliers > 0:
            logger.info(f"  (This is normal - {outliers/len(df)*100:.1f}% of data)")
    
    # Summary
    total_issues = neg_qty + zero_sales + missing_dates + future_dates
    if total_issues == 0:
        log_success(logger, "No critical data quality issues found!")
    else:
        log_warning(logger, f"Total issues found: {total_issues}")

def main():
    try:
        log_section(logger, "SALES DATA CLEANING PIPELINE")
        
        df = load_data(RAW_SALES_FILE)
        df = standardize_columns(df)
        df = parse_dates(df)
        df = convert_numeric_columns(df)

        logger.info("\n--- Data Types After Standardization ---")
        logger.info(f"\n{df.dtypes}")

        validate_data(df)

        df = clean_invalid_records(df)

        # Ensure output directory exists
        CLEANED_SALES_FILE.parent.mkdir(parents=True, exist_ok=True)
        
        df.to_csv(CLEANED_SALES_FILE, index=False)
        log_success(logger, f"Cleaned data saved to {CLEANED_SALES_FILE}")
        log_section(logger, "CLEANING COMPLETED SUCCESSFULLY")
        
    except Exception as e:
        log_error(logger, f"Pipeline failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
