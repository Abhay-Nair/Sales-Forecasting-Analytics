# 📊 Sales Forecasting & Analytics

> End-to-end time-series forecasting pipeline with SARIMA modeling and interactive Power BI dashboard

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/abhay/sales-forecasting-project/graphs/commit-activity)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](http://makeapullrequest.com)

## 🎯 Project Overview

This project delivers a complete sales forecasting solution for business planning, combining statistical modeling with interactive visualization. Built to mirror real-world forecasting workflows used in industry.

**Business Problem:** Companies need reliable sales forecasts to optimize inventory, staffing, and revenue planning.

**Solution:** SARIMA-based forecasting pipeline that analyzes historical sales patterns and generates 12-month predictions with 90% accuracy (MAPE: 10.04%).

## 🚀 Key Features

- ✅ Automated data cleaning and validation pipeline
- ✅ Time-series stationarity testing (ADF test)
- ✅ Seasonal ARIMA (SARIMA) modeling
- ✅ Rigorous model evaluation with train-test split
- ✅ 12-month sales forecasting with confidence intervals
- ✅ Interactive Power BI dashboard for stakeholders
- ✅ Production-ready error handling and logging

## 📈 Results

| Metric | Value |
|--------|-------|
| **MAE** | 12,676 |
| **RMSE** | 16,069 |
| **MAPE** | 10.04% |
| **Forecast Horizon** | 12 months |
| **Model** | SARIMA(1,1,1)(1,1,1,12) |

## 🛠️ Tech Stack

- **Python 3.8+** - Core programming language
- **pandas** - Data manipulation and aggregation
- **statsmodels** - SARIMA modeling and statistical tests
- **matplotlib** - Data visualization
- **scikit-learn** - Model evaluation metrics
- **Power BI** - Interactive dashboard
- **joblib** - Model persistence

## 📁 Project Structure

```
sales-forecasting-project/
│
├── data/
│   ├── raw/                          # Original sales data
│   │   └── superstore_sales.csv
│   └── processed/                    # Cleaned and aggregated data
│       ├── superstore_sales_cleaned.csv
│       └── sales_forecast_12_months.csv
│
├── src/                              # Source code
│   ├── config.py                     # Configuration and constants
│   ├── data_cleaning.py              # Data cleaning pipeline
│   ├── eda.py                        # Exploratory data analysis
│   ├── stationarity_check.py         # ADF test for stationarity
│   ├── differencing.py               # Time-series differencing
│   ├── train_sarima.py               # SARIMA model training
│   ├── forecast.py                   # Generate forecasts
│   └── model_evaluation.py           # Model validation
│
├── PowerBI-Component/                # Dashboard files
│   ├── powerBI.pbix                  # Interactive dashboard
│   └── pics/                         # Dashboard screenshots
│
├── models/                           # Saved models (generated)
├── results/                          # Output plots (generated)
├── logs/                             # Execution logs (generated)
│
├── requirements.txt                  # Python dependencies
├── .gitignore                        # Git ignore rules
└── README.md                         # This file
```

## 🚦 Getting Started

### Prerequisites

- Python 3.8 or higher
- pip package manager
- Git (for cloning)
- (Optional) Power BI Desktop for dashboard viewing

### System Requirements

- **RAM:** 4GB minimum, 8GB recommended
- **Storage:** 500MB for project + dependencies
- **OS:** Windows, macOS, or Linux

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/abhay/sales-forecasting-project.git
cd sales-forecasting-project
```

2. **Create virtual environment** (recommended)
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

### Usage

Run the pipeline in sequence:

#### 1. Data Cleaning
```bash
python src/data_cleaning.py
```
- Loads raw sales data
- Standardizes columns and data types
- Removes invalid records and duplicates
- Outputs: `data/processed/superstore_sales_cleaned.csv`

#### 2. Exploratory Data Analysis
```bash
python src/eda.py
```
- Aggregates sales to monthly level
- Visualizes sales trends
- Identifies patterns

#### 3. Stationarity Check
```bash
python src/stationarity_check.py
```
- Performs Augmented Dickey-Fuller test
- Confirms non-stationarity in raw data

#### 4. Differencing
```bash
python src/differencing.py
```
- Applies first-order differencing
- Verifies stationarity after transformation

#### 5. Train SARIMA Model
```bash
python src/train_sarima.py
```
- Trains SARIMA(1,1,1)(1,1,1,12) model
- Displays model summary and diagnostics

#### 6. Model Evaluation
```bash
python src/model_evaluation.py
```
- Performs time-series train-test split
- Calculates MAE, RMSE, MAPE
- Visualizes actual vs predicted sales

#### 7. Generate Forecast
```bash
python src/forecast.py
```
- Generates 12-month forecast
- Creates confidence intervals
- Outputs: `data/processed/sales_forecast_12_months.csv`

## 📊 Power BI Dashboard

Open `PowerBI-Component/powerBI.pbix` in Power BI Desktop to explore:

- **Actual vs Forecasted Sales** - Time-series comparison
- **Key KPIs** - Total sales, average monthly sales, forecast accuracy
- **Year Slicer** - Filter by specific years (2011-2014)
- **Seasonal Patterns** - Identify peak sales periods

### Dashboard Screenshots

![Full Dashboard (Without Slicing)](PowerBI-Component/pics/Full-Graph(no-slicing).png)

*Additional screenshots available in `PowerBI-Component/pics/` folder showing year-by-year analysis and 2015 predictions.*

## 🧠 Methodology

### 1. Data Preparation
- Removed 31,241 invalid records (missing dates, zero sales, duplicates)
- Standardized 20,049 valid transactions
- Aggregated to 48 months of data (2011-2014)

### 2. Time-Series Analysis
- **ADF Test Result:** p-value = 0.70 (non-stationary)
- **After Differencing:** p-value < 0.01 (stationary ✓)
- **Seasonality:** 12-month cycle identified

### 3. Model Selection
**Why SARIMA?**
- Handles trend through differencing (d=1)
- Captures yearly seasonality (m=12)
- Industry-standard for monthly sales data
- Interpretable parameters

### 4. Validation Strategy
- **Train Set:** First 36 months
- **Test Set:** Last 12 months
- **Evaluation:** MAE, RMSE, MAPE on test set
- **Result:** 10.04% MAPE (excellent for business forecasting)

## 📌 Key Insights

1. **Stable Demand:** Forecast shows consistent sales without aggressive growth
2. **Seasonal Patterns:** Clear yearly cycles suitable for inventory planning
3. **Model Reliability:** 10.04% MAPE enables confident business decisions
4. **Actionable Output:** Dashboard translates predictions into stakeholder-friendly format

### Business Applications

- **Inventory Management:** Plan stock levels 12 months ahead
- **Revenue Planning:** Accurate financial forecasting
- **Staffing Decisions:** Align workforce with demand
- **Marketing Strategy:** Time campaigns with predicted peaks

## 🔧 Configuration

All parameters are centralized in `src/config.py`:

```python
# Forecasting parameters
FORECAST_HORIZON = 12  # months
TEST_SIZE = 12  # months for validation

# SARIMA parameters
SARIMA_ORDER = (1, 1, 1)  # (p, d, q)
SARIMA_SEASONAL_ORDER = (1, 1, 1, 12)  # (P, D, Q, m)
```

Modify these to experiment with different configurations.

### Hyperparameter Tuning

To find optimal SARIMA parameters:

```bash
python src/hyperparameter_tuning.py
```

This will test 729 parameter combinations and recommend the best model based on AIC/BIC criteria. Results are saved to `results/hyperparameter_tuning_results.csv`.

## 🧪 Testing

### Integration Testing (Recommended)

The most effective way to test this project is through integration testing:
```bash
# Test data cleaning
python src/data_cleaning.py

# Test model training
python src/train_sarima.py

# Test forecasting
python src/forecast.py

# Test model evaluation
python src/model_evaluation.py
```

Expected output:
```
✓ Successfully loaded 51290 rows
✓ Cleaned data saved to data/processed/superstore_sales_cleaned.csv
✓ Model trained successfully
✓ Forecast generated successfully
```

### Unit Tests

Unit test files are available in `tests/` directory demonstrating testing practices:
- `test_data_cleaning.py` - Data cleaning function tests
- `test_model_utils.py` - Model utility tests

**Note:** Due to a Windows-specific stdout encoding conflict with pytest, integration testing (running actual scripts) is recommended. See `tests/README.md` for details.

## 🔧 Troubleshooting

### Common Issues

**Issue:** `ModuleNotFoundError: No module named 'statsmodels'`  
**Solution:** Install dependencies: `pip install -r requirements.txt`

**Issue:** `FileNotFoundError: data/raw/superstore_sales.csv not found`  
**Solution:** Ensure raw data file exists in `data/raw/` directory

**Issue:** Model training takes too long  
**Solution:** This is normal for SARIMA. First training takes 30-60 seconds. Subsequent forecasts use saved model (instant).

**Issue:** Plots not displaying  
**Solution:** Plots are saved to `results/` folder, not displayed interactively

**Issue:** Unicode errors on Windows  
**Solution:** Already handled in logger.py with UTF-8 encoding

### Getting Help

1. Open an issue on GitHub with error details
2. Ensure you're using Python 3.8+

## 📝 Future Enhancements

- [x] Hyperparameter tuning (grid search for optimal SARIMA parameters) ✅
- [ ] Prophet model comparison
- [ ] LSTM/Deep Learning model comparison
- [ ] Automated retraining pipeline with scheduling
- [ ] REST API for forecast serving (FastAPI)
- [ ] Docker containerization
- [ ] CI/CD pipeline (GitHub Actions)
- [ ] Streamlit interactive dashboard
- [ ] Real-time data ingestion
- [ ] Model monitoring and drift detection

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

**What this means:**
- ✅ You can use this code for personal or commercial projects
- ✅ You can modify and distribute the code
- ✅ You can use it in private projects
- ⚠️ You must include the original license and copyright notice
- ⚠️ The software is provided "as is" without warranty

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -m 'Add improvement'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open a Pull Request

See [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.

## 👤 Author

**Abhay**
- GitHub: [@abhay](https://github.com/Abhay-Nair)
- LinkedIn: [Abhay](https://www.linkedin.com/in/abhay-nair-1b9293232/)

## 🙏 Acknowledgments

- **Dataset:** Superstore Sales Data
- **Inspiration:** Real-world business forecasting challenges
- **Tools:** Python data science ecosystem (pandas, statsmodels, scikit-learn)
- **Visualization:** Power BI for interactive dashboards

---

## 📚 Additional Resources

- [SARIMA Documentation](https://www.statsmodels.org/stable/generated/statsmodels.tsa.statespace.sarimax.SARIMAX.html)
- [Time Series Analysis Guide](https://otexts.com/fpp2/)
- [Project Improvements Tracker](IMPROVEMENTS.md)
- [Project Summary](PROJECT_SUMMARY.md)

---

## 📋 Quick Reference

### File Structure
```
src/
├── config.py              # All configuration parameters
├── data_cleaning.py       # Data preprocessing pipeline
├── eda.py                 # Exploratory analysis
├── stationarity_check.py  # ADF test
├── differencing.py        # Time series transformation
├── train_sarima.py        # Model training
├── forecast.py            # Generate predictions
├── model_evaluation.py    # Validate model
├── hyperparameter_tuning.py  # Parameter optimization
├── logger.py              # Logging utilities
├── model_utils.py         # Model persistence
└── visualization.py       # Plotting functions
```

### Key Commands
```bash
# Full pipeline
python src/data_cleaning.py && python src/train_sarima.py && python src/forecast.py

# Quick forecast (uses saved model)
python src/forecast.py

# Find best parameters
python src/hyperparameter_tuning.py

# Run tests
pytest tests/ -v
```

### Key Files
- **Model:** `models/sarima_model.pkl` (7.3MB)
- **Forecast:** `data/processed/sales_forecast_12_months.csv`
- **Plots:** `results/forecast_plot.png`, `results/model_evaluation.png`
- **Logs:** `logs/sales_forecasting.log`

---

**⭐ If you found this project helpful, please give it a star!**

**📧 Questions or suggestions?** Open an issue or reach out via LinkedIn.
