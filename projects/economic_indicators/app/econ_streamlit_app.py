import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import json

# Page configuration
st.set_page_config(
    page_title="Economic Indicators Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Economic Indicators Dashboard")
st.markdown("Analyze and visualize key economic indicators from FRED")

# Default FRED series if file doesn't exist
DEFAULT_FRED_SERIES = {
    "GDP": "GDP",
    "Unemployment Rate": "UNRATE",
    "Inflation (CPI)": "CPIAUCSL",
    "Federal Funds Rate": "FEDFUNDS",
    "S&P 500": "SP500",
    "10-Year Treasury": "GS10",
    "Consumer Sentiment": "UMCSENT",
    "Industrial Production": "INDPRO"
}

# Try to load fred_series.json, use defaults if not found
try:
    # Check if file exists
    json_path = "fred_series.json"
    if os.path.exists(json_path):
        with open(json_path, "r") as f:
            FRED_SERIES = json.load(f)
    else:
        st.info("Using default FRED series (fred_series.json not found)")
        FRED_SERIES = DEFAULT_FRED_SERIES
except Exception as e:
    st.warning(f"Could not load fred_series.json: {e}. Using defaults.")
    FRED_SERIES = DEFAULT_FRED_SERIES

# Sidebar
st.sidebar.header("⚙️ Configuration")

# API Key input
st.sidebar.markdown("### FRED API Setup")
st.sidebar.markdown("Get your free API key at [FRED](https://fred.stlouisfed.org/docs/api/api_key.html)")

# Check for API key in secrets first, then user input
api_key = None

# Try to get from Streamlit secrets (recommended for deployment)
try:
    api_key = st.secrets["FRED_API_KEY"]
    st.sidebar.success("✅ API Key loaded from secrets")
except:
    # Fall back to user input
    api_key = st.sidebar.text_input("Enter FRED API Key:", type="password")
    if api_key:
        st.sidebar.success("✅ API Key provided")
    else:
        st.sidebar.info("👆 Enter your FRED API key to fetch data")

# Data fetching function
@st.cache_data(ttl=3600)
def fetch_fred_data(series_id, api_key, start_date=None, end_date=None):
    """Fetch data from FRED API"""
    try:
        from fredapi import Fred
        fred = Fred(api_key=api_key)
        
        data = fred.get_series(
            series_id,
            observation_start=start_date,
            observation_end=end_date
        )
        
        df = pd.DataFrame({
            'Date': data.index,
            'Value': data.values
        })
        return df
    except ImportError:
        st.error("fredapi package not installed. Add 'fredapi' to requirements.txt")
        return None
    except Exception as e:
        st.error(f"Error fetching data for {series_id}: {e}")
        return None

# Sample data generator (fallback)
def generate_sample_data():
    """Generate sample economic data"""
    dates = pd.date_range(start='2020-01-01', end='2024-12-31', freq='ME')
    data = {
        'Date': dates,
        'GDP_Growth': [2.1 + i*0.1 for i in range(len(dates))],
        'Unemployment_Rate': [5.0 - i*0.02 for i in range(len(dates))],
        'Inflation_Rate': [2.5 + i*0.05 for i in range(len(dates))],
        'Interest_Rate': [1.75 + i*0.05 for i in range(len(dates))]
    }
    return pd.DataFrame(data)

# Main app logic
if api_key:
    st.sidebar.markdown("### Select Indicators")
    
    # Multi-select for FRED series
    selected_series = st.sidebar.multiselect(
        "Choose economic indicators:",
        options=list(FRED_SERIES.keys()),
        default=list(FRED_SERIES.keys())[:3]
    )
    
    # Date range
    st.sidebar.markdown("### Date Range")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        start_date = st.date_input(
            "Start Date",
            value=datetime(2020, 1, 1)
        )
    with col2:
        end_date = st.date_input(
            "End Date",
            value=datetime.now()
        )
    
    if selected_series:
        # Fetch data button
        if st.sidebar.button("📥 Fetch Data", type="primary"):
            with st.spinner("Fetching data from FRED..."):
                data_dict = {}
                
                for series_name in selected_series:
                    series_id = FRED_SERIES[series_name]
                    df = fetch_fred_data(
                        series_id,
                        api_key,
                        start_date=start_date.strftime('%Y-%m-%d'),
                        end_date=end_date.strftime('%Y-%m-%d')
                    )
                    
                    if df is not None:
                        data_dict[series_name] = df
                
                if data_dict:
                    # Store in session state
                    st.session_state['data'] = data_dict
                    st.success(f"✅ Successfully fetched {len(data_dict)} series!")
        
        # Display data if available
        if 'data' in st.session_state:
            data_dict = st.session_state['data']
            
            # Key metrics
            st.subheader("📈 Latest Values")
            cols = st.columns(len(data_dict))
            
            for idx, (name, df) in enumerate(data_dict.items()):
                with cols[idx]:
                    latest_value = df['Value'].iloc[-1]
                    previous_value = df['Value'].iloc[-2] if len(df) > 1 else latest_value
                    change = latest_value - previous_value
                    
                    st.metric(
                        label=name,
                        value=f"{latest_value:.2f}",
                        delta=f"{change:.2f}"
                    )
            
            # Time series visualization
            st.subheader("📊 Trends Over Time")
            
            # Create combined plot
            fig = go.Figure()
            
            for series_name, df in data_dict.items():
                fig.add_trace(go.Scatter(
                    x=df['Date'],
                    y=df['Value'],
                    mode='lines',
                    name=series_name,
                    line=dict(width=2)
                ))
            
            fig.update_layout(
                height=500,
                hovermode='x unified',
                xaxis_title="Date",
                yaxis_title="Value",
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Individual series plots
            st.subheader("📉 Individual Series")
            
            tabs = st.tabs(list(data_dict.keys()))
            
            for idx, (series_name, df) in enumerate(data_dict.items()):
                with tabs[idx]:
                    # Line chart
                    fig = px.line(
                        df,
                        x='Date',
                        y='Value',
                        title=f"{series_name} Over Time"
                    )
                    st.plotly_chart(fig, use_container_width=True)
                    
                    # Statistics
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        st.markdown("**Statistics**")
                        stats_df = df['Value'].describe().to_frame()
                        st.dataframe(stats_df, use_container_width=True)
                    
                    with col2:
                        st.markdown("**Recent Values**")
                        recent = df.tail(10).sort_values('Date', ascending=False)
                        st.dataframe(recent, use_container_width=True, hide_index=True)
            
            # Download data
            st.subheader("💾 Download Data")
            
            # Combine all series into one dataframe
            combined_df = None
            for series_name, df in data_dict.items():
                df_copy = df.copy()
                df_copy = df_copy.rename(columns={'Value': series_name})
                
                if combined_df is None:
                    combined_df = df_copy
                else:
                    combined_df = combined_df.merge(
                        df_copy,
                        on='Date',
                        how='outer'
                    )
            
            if combined_df is not None:
                csv = combined_df.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download All Data as CSV",
                    data=csv,
                    file_name=f"fred_data_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv"
                )
        else:
            st.info("👈 Click 'Fetch Data' in the sidebar to load economic indicators")
    else:
        st.info("👈 Select at least one indicator from the sidebar")

else:
    # No API key - show sample data option
    st.info("👈 Enter your FRED API key in the sidebar to fetch real data")
    
    if st.button("📊 Load Sample Data Instead"):
        df = generate_sample_data()
        
        # Display sample data
        st.subheader("📈 Sample Economic Indicators")
        
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
        
        # Metrics
        cols = st.columns(len(numeric_cols))
        for idx, col in enumerate(numeric_cols):
            with cols[idx]:
                st.metric(
                    label=col.replace('_', ' '),
                    value=f"{df[col].iloc[-1]:.2f}"
                )
        
        # Chart
        fig = px.line(
            df,
            x='Date',
            y=numeric_cols,
            title="Sample Economic Indicators"
        )
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(df, use_container_width=True)
    
    # Instructions
    st.markdown("""
    ### Getting Started
    
    **To use real FRED data:**
    1. Get a free API key from [FRED](https://fred.stlouisfed.org/docs/api/api_key.html)
    2. Enter it in the sidebar
    3. Select indicators and date range
    4. Click "Fetch Data"
    
    **Or use Streamlit Secrets (recommended for deployment):**
    1. Go to your app settings in Streamlit Cloud
    2. Add to secrets.toml:
    ```toml
    FRED_API_KEY = "your_api_key_here"
    ```
    """)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info("""
This dashboard fetches economic data from the Federal Reserve Economic Data (FRED) API.

Available indicators can be customized in fred_series.json or use the defaults.
""")
