
import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from fredapi import Fred

# Page configuration
st.set_page_config(
    page_title="Economic Indicators Dashboard",
    page_icon="📊",
    layout="wide"
)

# Title
st.title("📊 Economic Indicators Analysis Dashboard")
st.markdown("Analyze and visualize key economic indicators")

# Sidebar
st.sidebar.header("⚙️ Configuration")

# Option to use sample data or upload
data_source = st.sidebar.radio(
    "Data Source:",
    ["Upload CSV", "Use FRED API", "Sample Data"]
)

df = None

# Sample data generator
def generate_sample_data():
    """Generate sample economic data"""
    dates = pd.date_range(start='2020-01-01', end='2024-12-31', freq='M')
    data = {
        'Date': dates,
        'GDP_Growth': [2.1, 2.3, -5.0, -31.4, 33.4, 4.3, 4.5, 6.3, 6.7, 2.3, 
                       6.9, 5.5, 1.7, 2.9, 3.2, 4.9, 2.0, 2.7, 3.4, 2.6,
                       3.2, 2.1, 2.8, 3.0, 2.4, 2.9, 1.6, 1.3, 2.5, 2.8,
                       3.1, 2.4, 2.7, 3.0, 2.2, 2.5, 2.9, 3.1, 2.6, 2.4,
                       2.7, 2.3, 2.8, 2.5, 3.0, 2.6, 2.4, 2.8, 2.5, 2.7,
                       2.9, 2.6, 2.4, 2.8, 2.5, 2.7, 2.3, 2.6, 2.4, 2.5],
        'Unemployment_Rate': [3.6, 3.5, 4.4, 14.7, 13.3, 11.1, 10.2, 8.4, 7.9, 6.9,
                              6.7, 6.3, 6.2, 6.0, 6.1, 5.9, 5.4, 5.2, 4.0, 3.6,
                              3.6, 3.8, 3.6, 3.5, 3.4, 3.7, 3.8, 3.9, 3.5, 3.4,
                              3.6, 3.7, 3.5, 3.4, 3.9, 3.8, 3.7, 3.5, 3.9, 4.0,
                              3.8, 3.9, 3.7, 4.0, 3.8, 3.9, 4.1, 3.8, 4.0, 3.9,
                              4.1, 4.0, 4.2, 3.9, 4.1, 4.0, 4.2, 4.1, 4.3, 4.2],
        'Inflation_Rate': [2.5, 2.3, 1.5, 0.3, 0.6, 1.0, 1.3, 1.2, 1.4, 1.2,
                          1.4, 1.5, 1.7, 2.6, 4.2, 5.4, 7.0, 8.5, 8.3, 8.0,
                          7.1, 6.5, 6.0, 5.0, 4.0, 3.7, 3.2, 3.0, 3.4, 3.2,
                          3.5, 3.7, 3.1, 3.0, 3.2, 3.4, 3.1, 2.9, 3.3, 3.5,
                          3.2, 3.4, 3.0, 3.1, 2.9, 3.2, 3.4, 2.8, 3.0, 2.9,
                          3.1, 3.0, 2.8, 2.9, 2.7, 2.8, 2.6, 2.7, 2.5, 2.6],
        'Interest_Rate': [1.75, 1.75, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25, 0.25,
                         0.25, 0.25, 0.25, 0.25, 0.50, 1.00, 1.75, 2.50, 3.00, 3.25,
                         3.75, 4.50, 4.75, 5.25, 5.50, 5.50, 5.50, 5.50, 5.25, 5.00,
                         4.75, 4.50, 4.75, 5.00, 4.75, 4.50, 4.75, 5.00, 4.75, 4.50,
                         4.75, 4.50, 4.75, 4.50, 4.25, 4.50, 4.25, 4.50, 4.25, 4.00,
                         4.25, 4.00, 4.25, 4.00, 3.75, 4.00, 3.75, 3.50, 3.75, 3.50]
    }
    return pd.DataFrame(data)

# Load data based on selection
if data_source == "Upload CSV":
    uploaded_file = st.sidebar.file_uploader("Upload CSV file", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        if df.columns[0] != 'Date':
            df.columns = ['Date'] + list(df.columns[1:])
        df['Date'] = pd.to_datetime(df['Date'])
        st.write(df)
    else:
        st.info("👈 Please upload a CSV file to begin")

elif data_source == "Use FRED API":
    st.sidebar.markdown("### FRED API Setup")
    api_key = st.sidebar.text_input("Enter FRED API Key:", type="password")
    
    if api_key:
        from fredapi import Fred
        fred = Fred(api_key=api_key)
        st.sidebar.success("✓ API Key provided")
        st.sidebar.markdown("Get your free API key at [FRED](https://fred.stlouisfed.org/docs/api/api_key.html)")

        # --- Choose source type for series list ---
        source_type = st.sidebar.radio("Select series source:", ["JSON", "CSV"])

        if source_type == "JSON":
            import json
            with open("fred_series.json", "r") as f:
                available_series = json.load(f)
        else:  # CSV
            df_series = pd.read_csv("fred_series.csv")
            available_series = dict(zip(df_series["Label"], df_series["SeriesID"]))

        # --- Multiselect dropdown for series ---
        selected_labels = st.sidebar.multiselect(
            "Select FRED data fields:",
            options=list(available_series.keys()),
            default=[]
        )

        if selected_labels:
            data_dict = {}
            for label in selected_labels:
                series_id = available_series[label]
                st.write(f"Fetching {label} ({series_id})...")
                data_dict[label] = fred.get_series(series_id)

            # Combine into DataFrame
            df = pd.DataFrame(data_dict)
            df.index = pd.to_datetime(df.index)
            df.reset_index(inplace=True)
            df.rename(columns={"index": "Date"}, inplace=True)

            st.success("✅ FRED data successfully loaded")
            st.dataframe(df.tail(10))
    else:
        st.sidebar.info("Need a FRED API key? [Get one here](https://fred.stlouisfed.org/docs/api/api_key.html)")
        
elif data_source == "Sample Data":
    df = generate_sample_data()
    st.sidebar.success("✓ Sample data loaded")

# Main dashboard
if df is not None:
    # Date range selector
    st.sidebar.markdown("### Date Range")
    min_date = df['Date'].min()
    max_date = df['Date'].max()
    
    date_range = st.sidebar.date_input(
        "Select date range:",
        value=(min_date, max_date),
        min_value=min_date,
        max_value=max_date
    )
    
    if len(date_range) == 2:
        mask = (df['Date'] >= pd.to_datetime(date_range[0])) & (df['Date'] <= pd.to_datetime(date_range[1]))
        df_filtered = df[mask].copy()
    else:
        df_filtered = df.copy()
    
    # Key metrics
    st.subheader("📈 Key Metrics Overview")
    
    numeric_cols = df_filtered.select_dtypes(include=['float64', 'int64']).columns.tolist()
    
    if len(numeric_cols) > 0:
        cols = st.columns(min(4, len(numeric_cols)))
        
        for idx, col_name in enumerate(numeric_cols[:4]):
            with cols[idx]:
                current_value = df_filtered[col_name].iloc[-1]
                previous_value = df_filtered[col_name].iloc[-2] if len(df_filtered) > 1 else current_value
                change = current_value - previous_value
                
                st.metric(
                    label=col_name.replace('_', ' '),
                    value=f"{current_value:.2f}",
                    delta=f"{change:.2f}"
                )
    
    # Indicator selection
    st.subheader("📊 Indicator Visualization")
    
    indicators = st.multiselect(
        "Select indicators to visualize:",
        numeric_cols,
        default=numeric_cols[:min(3, len(numeric_cols))]
    )
    
    if indicators:
        # Time series chart
        fig = go.Figure()
        
        for indicator in indicators:
            fig.add_trace(go.Scatter(
                x=df_filtered['Date'],
                y=df_filtered[indicator],
                mode='lines+markers',
                name=indicator.replace('_', ' '),
                line=dict(width=2),
                marker=dict(size=4)
            ))
        
        fig.update_layout(
            title="Economic Indicators Over Time",
            xaxis_title="Date",
            yaxis_title="Value",
            hovermode='x unified',
            height=500,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Statistical summary
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Statistical Summary")
            summary_df = df_filtered[indicators].describe()
            st.dataframe(summary_df, use_container_width=True)
        
        with col2:
            st.subheader("📈 Recent Values")
            recent_df = df_filtered[['Date'] + indicators].tail(10).sort_values('Date', ascending=False)
            st.dataframe(recent_df, use_container_width=True, hide_index=True)
        
        # Correlation analysis
        if len(indicators) > 1:
            st.subheader("🔗 Correlation Analysis")
            
            corr_matrix = df_filtered[indicators].corr()
            
            fig_corr = px.imshow(
                corr_matrix,
                text_auto='.2f',
                aspect="auto",
                color_continuous_scale='RdBu_r',
                zmin=-1,
                zmax=1,
                title="Correlation Matrix"
            )
            
            fig_corr.update_layout(height=400)
            st.plotly_chart(fig_corr, use_container_width=True)
        
        # Distribution analysis
        st.subheader("📉 Distribution Analysis")
        
        selected_indicator = st.selectbox(
            "Select an indicator for distribution:",
            indicators
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_hist = px.histogram(
                df_filtered,
                x=selected_indicator,
                nbins=30,
                title=f"Distribution of {selected_indicator.replace('_', ' ')}"
            )
            st.plotly_chart(fig_hist, use_container_width=True)
        
        with col2:
            fig_box = px.box(
                df_filtered,
                y=selected_indicator,
                title=f"Box Plot of {selected_indicator.replace('_', ' ')}"
            )
            st.plotly_chart(fig_box, use_container_width=True)
    
    # Raw data view
    with st.expander("🔍 View Raw Data"):
        st.dataframe(df_filtered, use_container_width=True, hide_index=True)
        
        # Download button
        csv = df_filtered.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download filtered data as CSV",
            data=csv,
            file_name='economic_indicators_filtered.csv',
            mime='text/csv'
        )

else:
    # Instructions when no data is loaded
    st.info("👈 Please select a data source from the sidebar to get started")
    
    st.markdown("""
    ### Getting Started
    
    **Option 1: Upload CSV**
    - Upload your own economic indicators CSV file
    - First column should be dates, other columns should be numeric indicators
    
    **Option 2: Use FRED API**
    - Get a free API key from [FRED](https://fred.stlouisfed.org/docs/api/api_key.html)
    - Access 800,000+ economic time series
    
    **Option 3: Sample Data**
    - Explore the dashboard with pre-loaded sample data
    - Includes GDP Growth, Unemployment, Inflation, and Interest Rates
    
    ### Expected CSV Format
    ```
    Date,GDP_Growth,Unemployment_Rate,Inflation_Rate
    2020-01-01,2.1,3.6,2.5
    2020-02-01,2.3,3.5,2.3
    ...
    ```
    """)

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info("""
This dashboard allows you to:
- Visualize economic indicators over time
- Analyze correlations between indicators
- View statistical summaries
- Export filtered data
""")
