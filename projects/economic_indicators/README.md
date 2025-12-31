# Economic Indicator Forecasting Platform

![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Status](https://img.shields.io/badge/status-active-success.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

<p align="center">
  <img src="results/images/econ_app_dashboard.png" alt="Dashboard Screenshot" width="700"/>
</p>

## 🎯 Project Overview

Interactive forecasting platform for US economic indicators (unemployment, inflation, GDP) using time series analysis and machine learning. Achieved **1.39% MAPE** on Consumer Price Index predictions.

**🔗 Live Demo:** [https://econ-indicators.streamlit.app](https://econ-indicators.streamlit.app)

## ✨ Key Features

- Real-time data collection from FRED API
- Multiple forecasting models (Prophet, ARIMA, LSTM)
- Interactive Streamlit dashboard
- Model performance comparison
- 3-24 month forecast horizons
- Confidence intervals and prediction analysis

## 🎬 Demo

<p align="center">
  <img src="results/images/demo.gif" alt="Demo" width="700"/>
</p>

*Interactive dashboard showing unemployment forecasting*

## 📊 Results

| Model | MAPE | RMSE | R² Score |
|-------|------|------|----------|
| Prophet | 1.4% | 5.2 | 0.59 |
| ARIMA | 3.1% | 11.2 | -0.87 |
| LSTM | 2.02% | 6.54 | -0.56 |

**Key Findings:**
- Prophet model performed best with seasonal data
- 12-month forecasts most reliable (MAPE < 3%)
- CPI predictions most accurate during stable periods

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- FRED API key (free from [https://fred.stlouisfed.org/docs/api/api_key.html](https://fred.stlouisfed.org/docs/api/api_key.html))

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/economic-forecasting.git
cd economic-forecasting

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Usage

#### Run Streamlit Dashboard
```bash
streamlit run app.py
```

#### Run Jupyter Notebooks
```bash
jupyter notebook notebooks/
```

#### Use as Python Module
```python
from src.models import ProphetForecaster

# Initialize forecaster
forecaster = ProphetForecaster(data)

# Make predictions
forecast = forecaster.predict(periods=12)
```

## 📁 Project Structure

```
economic-forecasting/
├── notebooks/          # Analysis notebooks (start here!)
├── src/               # Source code modules
├── app.py            # Streamlit dashboard
├── data/             # Data storage
└── results/          # Outputs and visualizations
```

## 🛠️ Technologies Used

- **Data Collection:** FRED API, yfinance
- **Data Processing:** Pandas, NumPy
- **Modeling:** Prophet, Statsmodels (ARIMA), TensorFlow (LSTM)
- **Visualization:** Plotly, Matplotlib, Seaborn
- **Dashboard:** Streamlit
- **Deployment:** Streamlit Cloud

## 🔬 Methodology

### 1. Data Collection
- Collected 30+ years of monthly data from FRED API
- Indicators: Unemployment rate, CPI, GDP, interest rates

### 2. Exploratory Data Analysis
- Time series decomposition
- Stationarity testing (ADF test)
- Correlation analysis

### 3. Feature Engineering
- Lagged features (1, 3, 6, 12 months)
- Moving averages
- Rate of change indicators
- Economic regime indicators

### 4. Model Development
- **Prophet:** Handles seasonality and trends automatically
- **ARIMA:** Captures autocorrelation patterns
- **LSTM:** Deep learning approach for complex patterns

### 5. Evaluation
- Walk-forward validation
- Multiple accuracy metrics (MAPE, RMSE, R²)
- Residual analysis

## 📈 Key Visualizations

<table>
  <tr>
    <td><img src="results/images/plot comparison.png" alt="Forecast Comparison" width="400"/></td>
    <td><img src="results/images/model comparision.png" alt="Model Performance" width="400"/></td>
  </tr>
  <tr>
    <td align="center"><i>Model Comparison</i></td>
    <td align="center"><i>Performance Metrics</i></td>
  </tr>
</table>

## 🎓 What I Learned

- Working with time series data and handling seasonality
- Implementing multiple forecasting algorithms
- Deploying ML applications with Streamlit
- API integration and automated data pipelines
- Model evaluation and selection for production

## 🔮 Future Enhancements

- [ ] Add more economic indicators
- [ ] Implement ensemble methods
- [ ] Real-time alerts for significant changes
- [ ] Integration with economic news sentiment
- [ ] Mobile-responsive design improvements

## 📝 Blog Post

Read the detailed project walkthrough: [Building an Economic Forecasting Platform](https://yourusername.github.io/blog/economic-forecasting-project)

## 🤝 Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

## 📄 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 👤 Author

**Jessica Bean**
- Portfolio: [[https://github.com/jessicabriandebean/jessicabriandebean.github.io](https://github.com/jessicabriandebean/jessicabriandebean.github.io)
- LinkedIn: [linkedin.com/in/jessicabbean](https://linkedin.com/in/jessicabbean)
- Email: jessicabbean@gmail.com

## 🙏 Acknowledgments

- Data source: Federal Reserve Economic Data (FRED)
- Inspired by economic research from [source]
- Built with guidance from [resource]

---

⭐ **If you found this project helpful, please give it a star!** ⭐


## This is the template for each project

# 📊 Project Title

## 🧩 Overview
Brief summary of the project, its goals, and relevance.

## 📂 Dataset
- Source: [Kaggle/UCI/etc.]
- Size: X rows, Y columns
- Features: List key variables
- Preprocessing steps

## 🔍 Exploratory Data Analysis (EDA)
- Summary statistics
- Visualizations (histograms, boxplots, correlation heatmaps)
- Insights discovered

## 🤖 Modeling (ML/NLP)
- Problem type: Regression / Classification / Clustering / NLP
- Algorithms used: e.g., Random Forest, XGBoost, LSTM
- Evaluation metrics: Accuracy, F1-score, RMSE, etc.
- Model performance summary

## 📈 Visualization
- Tools: Matplotlib, Seaborn, Plotly, Tableau, Power BI
- Interactive dashboards or static plots
- Key takeaways

## 🧪 Technical Stack
- Languages: Python, R, SQL
- Libraries: pandas, scikit-learn, NLTK, spaCy, TensorFlow, etc.
- Tools: Jupyter, VS Code, Git, Docker (if applicable)

## 📁 File Structure
