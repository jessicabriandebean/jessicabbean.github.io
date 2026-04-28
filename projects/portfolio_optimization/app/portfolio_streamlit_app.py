"""
Portfolio Optimization - Streamlit Web Application
Run with: streamlit run streamlit_app.py
"""

import sys
from pathlib import Path
import os
import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# FIX: Proper path handling for Streamlit
try:
    # Try to get the file path normally
    SCRIPT_DIR = Path(__file__).resolve().parent
except NameError:
    # Fallback for Streamlit: use current working directory
    SCRIPT_DIR = Path.cwd()

# Add parent directory to Python path
PROJECT_ROOT = SCRIPT_DIR.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

# Import custom modules
try:
    from portfolio_optimization.app.portfolio_risk_backtest import PortfolioRiskAnalyzer, PortfolioBacktester
except ImportError as e:
    st.error(f"⚠️ Could not import portfolio_risk_backtest.py: {e}")
    st.stop()

# Page configuration
st.set_page_config(
    page_title="Portfolio Optimizer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'returns' not in st.session_state:
    st.session_state.returns = None
if 'tickers' not in st.session_state:
    st.session_state.tickers = []

# Header
st.markdown('<p class="main-header">📈 Portfolio Optimization Platform</p>', unsafe_allow_html=True)
st.markdown("**Optimize your portfolio using Modern Portfolio Theory with advanced risk analysis and backtesting**")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Stock selection
    st.subheader("1. Select Assets")
    
    # Preset portfolios
    preset = st.selectbox(
        "Choose a preset portfolio",
        ["Custom", "Tech Giants", "Dow 30", "Dividend Aristocrats", "FAANG"]
    )
    
    if preset == "Tech Giants":
        default_tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META', 'NVDA', 'TSLA', 'NFLX']
    elif preset == "Dow 30":
        default_tickers = ['AAPL', 'MSFT', 'JPM', 'JNJ', 'V', 'PG', 'UNH', 'HD', 'DIS', 'MA']
    elif preset == "FAANG":
        default_tickers = ['META', 'AAPL', 'AMZN', 'NFLX', 'GOOGL']
    elif preset == "Dividend Aristocrats":
        default_tickers = ['JNJ', 'PG', 'KO', 'PEP', 'WMT', 'MCD', 'MMM', 'CAT']
    else:
        default_tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'JPM']
    
    tickers_input = st.text_area(
        "Enter stock tickers (comma-separated)",
        value=', '.join(default_tickers),
        height=100
    )
    
    # Date range
    st.subheader("2. Date Range")
    col1, col2 = st.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date",
            value=datetime.now() - timedelta(days=5*365)
        )
    with col2:
        end_date = st.date_input(
            "End Date",
            value=datetime.now()
        )
    
    # Optimization settings
    st.subheader("3. Optimization Settings")
    
    optimization_method = st.selectbox(
        "Strategy",
        ["Max Sharpe Ratio", "Min Variance", "Max Return"]
    )
    
    risk_free_rate = st.slider(
        "Risk-Free Rate (%)",
        min_value=0.0,
        max_value=10.0,
        value=3.0,
        step=0.1
    ) / 100
    
    # Backtesting settings
    st.subheader("4. Backtesting Settings")
    
    lookback_years = st.slider(
        "Lookback Period (years)",
        min_value=1,
        max_value=5,
        value=3
    )
    
    rebalance_freq = st.selectbox(
        "Rebalance Frequency",
        ["Monthly", "Quarterly", "Yearly"]
    )
    
    include_costs = st.checkbox("Include Transaction Costs", value=True)
    
    # Load data button
    st.divider()
    load_data = st.button("🚀 Load Data & Optimize", type="primary", use_container_width=True)

# Main content
# Main content
if load_data:
    with st.spinner("Downloading data..."):
        try:
            # Parse tickers
            tickers = [t.strip().upper() for t in tickers_input.split(',') if t.strip()]
            
            # Download data
            data = yf.download(
                tickers,
                start=start_date,
                end=end_date,
                progress=False
            )
            
            # Handle different data structures from yfinance
            if len(tickers) == 1:
                # Single ticker: data is already a DataFrame
                if 'Adj Close' in data.columns:
                    data = data[['Adj Close']]
                    data.columns = tickers
                else:
                    # Fallback to Close if Adj Close not available
                    data = data[['Close']]
                    data.columns = tickers
            else:
                # Multiple tickers: extract Adj Close
                if isinstance(data.columns, pd.MultiIndex):
                    # MultiIndex structure
                    if 'Adj Close' in data.columns.levels[0]:
                        data = data['Adj Close']
                    else:
                        data = data['Close']
                else:
                    # Already simplified
                    data = data
            
            # Ensure data is DataFrame
            if isinstance(data, pd.Series):
                data = data.to_frame(name=tickers[0])
            
            # Remove any columns with all NaN
            data = data.dropna(axis=1, how='all')
            
            # Calculate returns
            returns = data.pct_change().dropna()
            
            # Verify we have valid data
            if returns.empty:
                st.error("❌ No valid data retrieved. Please check ticker symbols and date range.")
                st.stop()
            
            # Store in session state
            st.session_state.returns = returns
            st.session_state.tickers = list(returns.columns)  # Use actual column names
            st.session_state.data_loaded = True
            st.session_state.risk_free_rate = risk_free_rate
            
            st.success(f"✅ Successfully loaded {len(returns)} days of data for {len(returns.columns)} assets")
            
        except Exception as e:
            st.error(f"❌ Error loading data: {str(e)}")
            st.exception(e)  # Show full traceback for debugging
            st.stop()
            
            # Store in session state
            st.session_state.returns = returns
            st.session_state.tickers = tickers
            st.session_state.data_loaded = True
            st.session_state.risk_free_rate = risk_free_rate
            
            st.success(f"✅ Successfully loaded {len(returns)} days of data for {len(tickers)} assets")
            
        except Exception as e:
            st.error(f"❌ Error loading data: {str(e)}")
            st.stop()

if st.session_state.data_loaded:
    returns = st.session_state.returns
    tickers = st.session_state.tickers
    
    # Tabs for different analyses
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Overview", "🎯 Optimization", "📈 Risk Analysis", "🔄 Backtesting"])
    
    # TAB 1: Overview
    with tab1:
        st.header("Portfolio Overview")
        
        # Summary statistics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Assets", len(tickers))
        with col2:
            st.metric("Days", len(returns))
        with col3:
            st.metric("Date Range", f"{returns.index[0].strftime('%Y-%m-%d')}")
        with col4:
            st.metric("to", f"{returns.index[-1].strftime('%Y-%m-%d')}")
        
        # Price evolution
        st.subheader("Price Evolution (Normalized)")
        
        normalized_prices = (1 + returns).cumprod()
        
        fig = go.Figure()
        for ticker in tickers:
            fig.add_trace(go.Scatter(
                x=normalized_prices.index,
                y=normalized_prices[ticker],
                name=ticker,
                mode='lines'
            ))
        
        fig.update_layout(
            title="Cumulative Returns",
            xaxis_title="Date",
            yaxis_title="Cumulative Return",
            hovermode='x unified',
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Correlation matrix
        st.subheader("Correlation Matrix")
        
        corr_matrix = returns.corr()
        
        fig = go.Figure(data=go.Heatmap(
            z=corr_matrix.values,
            x=corr_matrix.columns,
            y=corr_matrix.columns,
            colorscale='RdBu',
            zmid=0,
            text=corr_matrix.values.round(2),
            texttemplate='%{text}',
            textfont={"size": 10},
            colorbar=dict(title="Correlation")
        ))
        
        fig.update_layout(
            title="Asset Correlation Matrix",
            height=500
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Statistics table
        st.subheader("Asset Statistics")
        
        stats_df = pd.DataFrame({
            'Annual Return': returns.mean() * 252,
            'Annual Volatility': returns.std() * np.sqrt(252),
            'Sharpe Ratio': (returns.mean() * 252 - risk_free_rate) / (returns.std() * np.sqrt(252))
        })
        
        st.dataframe(stats_df.style.format("{:.4f}"), use_container_width=True)
    
    # TAB 2: Optimization
    with tab2:
        st.header("Portfolio Optimization")
        
        st.info("⚠️ Optimization features require portfolio_risk_backtest.py module (currently commented out)")
        
        # You can add basic optimization here without the custom module
        # Or uncomment the import once you have the file
    
    # TAB 3: Risk Analysis
    with tab3:
        st.header("Risk Analysis")
        
        st.info("⚠️ Risk analysis features require portfolio_risk_backtest.py module (currently commented out)")
    
    # TAB 4: Backtesting
    with tab4:
        st.header("Walk-Forward Backtesting")
        
        st.info("⚠️ Backtesting features require portfolio_risk_backtest.py module (currently commented out)")

else:
    # Welcome screen
    st.info("👈 Configure your portfolio in the sidebar and click 'Load Data & Optimize' to get started")
    
    st.markdown("""
    ## 🎯 Features
    
    - **Portfolio Optimization**: Max Sharpe, Min Variance, or Max Return strategies
    - **Risk Analysis**: 13+ risk metrics including VaR, CVaR, and Max Drawdown
    - **Backtesting**: Walk-forward validation with realistic transaction costs
    - **Visualization**: Interactive charts for analysis and decision-making
    
    ## 📊 How to Use
    
    1. Select assets or choose a preset portfolio
    2. Choose date range and optimization strategy
    3. Configure backtesting parameters
    4. Click "Load Data & Optimize"
    5. Explore results across different tabs
    
    ## 💡 Tips
    
    - Use at least 3 years of data for reliable results
    - Quarterly rebalancing balances performance and costs
    - Enable transaction costs for realistic backtests
    - Compare multiple strategies using different configurations
    """)

# Footer
st.divider()
st.markdown("""
    <div style='text-align: center; color: #666; padding: 1rem;'>
        <p>📊 Portfolio Optimization Platform | Built with Streamlit & Python</p>
        <p>⚠️ For educational purposes only. Not financial advice.</p>
    </div>
""", unsafe_allow_html=True)