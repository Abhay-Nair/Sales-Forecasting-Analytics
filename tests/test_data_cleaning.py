"""
Unit tests for data cleaning module.
"""
import pytest
import pandas as pd
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

# Import only the functions we need, not modules that modify sys.stdout
import data_cleaning

class TestStandardizeColumns:
    """Tests for column standardization."""
    
    def test_standardize_columns_basic(self):
        """Test basic column name standardization."""
        df = pd.DataFrame({"Order Date": [1], "Sales Amount": [100]})
        result = data_cleaning.standardize_columns(df)
        assert "order_date" in result.columns
        assert "sales_amount" in result.columns
    
    def test_standardize_columns_strips_whitespace(self):
        """Test that whitespace is stripped."""
        df = pd.DataFrame({" Order Date ": [1], "Sales  ": [100]})
        result = data_cleaning.standardize_columns(df)
        assert "order_date" in result.columns
        assert "sales" in result.columns

class TestParseDates:
    """Tests for date parsing."""
    
    def test_parse_dates_valid(self):
        """Test parsing valid dates."""
        df = pd.DataFrame({
            "order_date": ["2024-01-01", "2024-01-02"],
            "ship_date": ["2024-01-03", "2024-01-04"]
        })
        result = data_cleaning.parse_dates(df)
        assert pd.api.types.is_datetime64_any_dtype(result["order_date"])
        assert pd.api.types.is_datetime64_any_dtype(result["ship_date"])
    
    def test_parse_dates_invalid(self):
        """Test parsing invalid dates returns NaT."""
        df = pd.DataFrame({
            "order_date": ["invalid", "2024-01-02"],
            "ship_date": ["2024-01-03", "also invalid"]
        })
        result = data_cleaning.parse_dates(df)
        assert pd.isna(result["order_date"].iloc[0])
        assert pd.isna(result["ship_date"].iloc[1])

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
