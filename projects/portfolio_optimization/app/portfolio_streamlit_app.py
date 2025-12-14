"""
Portfolio Optimization - Streamlit Web Application
Run with: streamlit run streamlit_app.py
"""

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

# Import custom modules
try:
    from portfolio_risk_backtest import PortfolioRiskAnalyzer, PortfolioBacktester
except ImportError:
    st.error("⚠️ Could not import portfolio_risk_backtest.py. Make sure it's in the same directory.")
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
            )['Adj Close']
            
            if isinstance(data, pd.Series):
                data = data.to_frame()
            
            # Calculate returns
            returns = data.pct_change().dropna()
            
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
        
        with st.spinner("Optimizing portfolio..."):
            try:
                # Map strategy names
                strategy_map = {
                    "Max Sharpe Ratio": "max_sharpe",
                    "Min Variance": "min_variance",
                    "Max Return": "max_return"
                }
                
                # Create backtester to use optimization
                backtester = PortfolioBacktester(returns, lookback_years=lookback_years)
                
                # Optimize
                optimal_weights = backtester.optimize_portfolio(
                    returns,
                    method=strategy_map[optimization_method],
                    risk_free_rate=risk_free_rate
                )
                
                # Calculate portfolio metrics
                portfolio_return = np.dot(optimal_weights, returns.mean() * 252)
                portfolio_vol = np.sqrt(np.dot(optimal_weights.T, np.dot(returns.cov() * 252, optimal_weights)))
                sharpe = (portfolio_return - risk_free_rate) / portfolio_vol
                
                # Display results
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("Expected Annual Return", f"{portfolio_return:.2%}")
                with col2:
                    st.metric("Annual Volatility", f"{portfolio_vol:.2%}")
                with col3:
                    st.metric("Sharpe Ratio", f"{sharpe:.4f}")
                
                st.divider()
                
                # Portfolio weights
                st.subheader("Optimal Portfolio Weights")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Bar chart
                    weights_df = pd.DataFrame({
                        'Asset': tickers,
                        'Weight': optimal_weights
                    }).sort_values('Weight', ascending=True)
                    
                    fig = px.bar(
                        weights_df,
                        x='Weight',
                        y='Asset',
                        orientation='h',
                        title="Asset Allocation",
                        color='Weight',
                        color_continuous_scale='Blues'
                    )
                    
                    fig.update_layout(height=400)
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    # Pie chart
                    fig = go.Figure(data=[go.Pie(
                        labels=tickers,
                        values=optimal_weights,
                        hole=0.3
                    )])
                    
                    fig.update_layout(
                        title="Weight Distribution",
                        height=400
                    )
                    st.plotly_chart(fig, use_container_width=True)
                
                # Weights table
                st.dataframe(
                    weights_df.style.format({'Weight': '{:.2%}'}),
                    use_container_width=True,
                    hide_index=True
                )
                
                # Efficient Frontier
                st.subheader("Efficient Frontier")
                
                with st.spinner("Calculating efficient frontier..."):
                    n_portfolios = 5000
                    results = np.zeros((3, n_portfolios))
                    
                    for i in range(n_portfolios):
                        weights = np.random.random(len(tickers))
                        weights /= np.sum(weights)
                        
                        portfolio_return = np.dot(weights, returns.mean() * 252)
                        portfolio_vol = np.sqrt(np.dot(weights.T, np.dot(returns.cov() * 252, weights)))
                        sharpe = (portfolio_return - risk_free_rate) / portfolio_vol
                        
                        results[0, i] = portfolio_return
                        results[1, i] = portfolio_vol
                        results[2, i] = sharpe
                    
                    fig = go.Figure()
                    
                    # Random portfolios
                    fig.add_trace(go.Scatter(
                        x=results[1, :],
                        y=results[0, :],
                        mode='markers',
                        marker=dict(
                            size=5,
                            color=results[2, :],
                            colorscale='Viridis',
                            showscale=True,
                            colorbar=dict(title="Sharpe Ratio")
                        ),
                        name='Random Portfolios'
                    ))
                    
                    # Optimal portfolio
                    fig.add_trace(go.Scatter(
                        x=[portfolio_vol],
                        y=[portfolio_return],
                        mode='markers',
                        marker=dict(size=20, color='red', symbol='star'),
                        name='Optimal Portfolio'
                    ))
                    
                    fig.update_layout(
                        title="Efficient Frontier",
                        xaxis_title="Volatility (Risk)",
                        yaxis_title="Expected Return",
                        height=600
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"❌ Error during optimization: {str(e)}")
    
    # TAB 3: Risk Analysis
    with tab3:
        st.header("Risk Analysis")
        
        with st.spinner("Calculating risk metrics..."):
            try:
                # Use equal weights for initial analysis
                analyzer = PortfolioRiskAnalyzer(returns)
                metrics = analyzer.get_risk_metrics()
                
                # Display metrics
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("Return Metrics")
                    st.metric("Annual Return", f"{metrics['Annual Return']:.2%}")
                    st.metric("Annual Volatility", f"{metrics['Annual Volatility']:.2%}")
                    st.metric("Sharpe Ratio", f"{metrics['Sharpe Ratio']:.4f}")
                    st.metric("Sortino Ratio", f"{metrics['Sortino Ratio']:.4f}")
                    st.metric("Calmar Ratio", f"{metrics['Calmar Ratio']:.4f}")
                
                with col2:
                    st.subheader("Risk Metrics")
                    st.metric("Max Drawdown", f"{metrics['Max Drawdown']:.2%}")
                    st.metric("VaR (95%)", f"{metrics['VaR (95%)']:.2%}")
                    st.metric("CVaR (95%)", f"{metrics['CVaR (95%)']:.2%}")
                    st.metric("Downside Deviation", f"{metrics['Downside Deviation']:.2%}")
                    st.metric("Skewness", f"{metrics['Skewness']:.4f}")
                    st.metric("Kurtosis", f"{metrics['Kurtosis']:.4f}")
                
                st.divider()
                
                # Cumulative returns
                st.subheader("Cumulative Returns")
                cumulative = (1 + analyzer.portfolio_returns).cumprod()
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=cumulative.index,
                    y=cumulative.values,
                    fill='tozeroy',
                    name='Cumulative Return'
                ))
                
                fig.update_layout(
                    xaxis_title="Date",
                    yaxis_title="Cumulative Return",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Drawdown
                st.subheader("Drawdown Analysis")
                dd_info = analyzer.calculate_maximum_drawdown()
                
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=dd_info['drawdown_series'].index,
                    y=dd_info['drawdown_series'].values,
                    fill='tozeroy',
                    fillcolor='rgba(255, 0, 0, 0.3)',
                    line=dict(color='red'),
                    name='Drawdown'
                ))
                
                fig.update_layout(
                    xaxis_title="Date",
                    yaxis_title="Drawdown",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Returns distribution
                st.subheader("Returns Distribution")
                
                fig = go.Figure()
                fig.add_trace(go.Histogram(
                    x=analyzer.portfolio_returns,
                    nbinsx=50,
                    name='Returns'
                ))
                
                fig.add_vline(
                    x=analyzer.portfolio_returns.mean(),
                    line_dash="dash",
                    line_color="green",
                    annotation_text="Mean"
                )
                
                fig.add_vline(
                    x=metrics['VaR (95%)'],
                    line_dash="dash",
                    line_color="red",
                    annotation_text="VaR (95%)"
                )
                
                fig.update_layout(
                    xaxis_title="Daily Returns",
                    yaxis_title="Frequency",
                    height=400
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
            except Exception as e:
                st.error(f"❌ Error in risk analysis: {str(e)}")
    
    # TAB 4: Backtesting
    with tab4:
        st.header("Walk-Forward Backtesting")
        
        rebal_map = {"Monthly": "M", "Quarterly": "Q", "Yearly": "Y"}
        
        if st.button("🔄 Run Backtest", type="primary"):
            with st.spinner("Running backtest... This may take a minute..."):
                try:
                    backtester = PortfolioBacktester(
                        returns,
                        lookback_years=lookback_years,
                        rebalance_frequency=rebal_map[rebalance_freq]
                    )
                    
                    # Run backtest
                    results = backtester.backtest(
                        strategy=strategy_map[optimization_method],
                        include_costs=include_costs
                    )
                    
                    # Display results
                    st.success("✅ Backtest complete!")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Total Return", f"{results['metrics']['Total Return']:.2%}")
                    with col2:
                        st.metric("CAGR", f"{results['metrics']['CAGR']:.2%}")
                    with col3:
                        st.metric("Sharpe Ratio", f"{results['metrics']['Sharpe Ratio']:.4f}")
                    with col4:
                        st.metric("Max Drawdown", f"{results['metrics']['Max Drawdown']:.2%}")
                    
                    st.divider()
                    
                    # Portfolio value over time
                    st.subheader("Portfolio Value Over Time")
                    
                    fig = go.Figure()
                    fig.add_trace(go.Scatter(
                        x=results['portfolio_values'].index,
                        y=results['portfolio_values']['value'],
                        fill='tozeroy',
                        name='Portfolio Value'
                    ))
                    
                    # Add rebalance points
                    rebal_dates = [r['date'] for r in results['rebalance_info']]
                    rebal_values = [r['portfolio_value'] for r in results['rebalance_info']]
                    
                    fig.add_trace(go.Scatter(
                        x=rebal_dates,
                        y=rebal_values,
                        mode='markers',
                        marker=dict(size=10, color='red'),
                        name='Rebalance Points'
                    ))
                    
                    fig.update_layout(
                        xaxis_title="Date",
                        yaxis_title="Portfolio Value ($)",
                        height=500
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # All metrics
                    st.subheader("Complete Backtest Metrics")
                    
                    metrics_df = pd.DataFrame([results['metrics']]).T
                    metrics_df.columns = ['Value']
                    
                    st.dataframe(
                        metrics_df.style.format("{:.4f}"),
                        use_container_width=True
                    )
                    
                    # Download results
                    csv = results['portfolio_values'].to_csv()
                    st.download_button(
                        label="📥 Download Portfolio Values (CSV)",
                        data=csv,
                        file_name="portfolio_backtest_results.csv",
                        mime="text/csv"
                    )
                    
                except Exception as e:
                    st.error(f"❌ Error during backtesting: {str(e)}")
                    st.exception(e)

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