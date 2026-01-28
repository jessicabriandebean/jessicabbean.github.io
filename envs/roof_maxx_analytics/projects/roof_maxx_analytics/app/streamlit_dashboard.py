 ============================================================================

# SECTION 5: STREAMLIT SALES DASHBOARD APPLICATION

# ============================================================================

# Save this as a separate file: streamlit_dashboard.py

STREAMLIT_APP = ‘’’
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import folium
from streamlit_folium import folium_static

st.set_page_config(
page_title=“Roof Maxx Sales Analytics”,
page_icon=“🏠”,
layout=“wide”
)

# Custom CSS

st.markdown(”””
<style>
.metric-card {
background-color: #f0f2f6;
padding: 20px;
border-radius: 10px;
margin: 10px 0;
}
.big-font {
font-size: 24px !important;
font-weight: bold;
}
</style>
“””, unsafe_allow_html=True)

st.title(“🏠 Roof Maxx Market Analytics Dashboard”)
st.markdown(”### Real-time Sales Intelligence & Predictive Analytics”)

# Sidebar filters

st.sidebar.header(“🎯 Territory Settings”)
territory = st.sidebar.selectbox(
“Select Territory”,
[“Washington - King County”, “Washington - Pierce County”,
“Washington - Snohomish County”, “Canada - British Columbia”,
“Canada - Ontario”, “Canada - Alberta”]
)

date_range = st.sidebar.date_input(
“Analysis Period”,
value=(datetime.now() - timedelta(days=90), datetime.now())
)

# Marketing Budget Input

st.sidebar.header(“💰 Marketing Investment”)
monthly_marketing = st.sidebar.number_input(
“Monthly Marketing Budget ($)”,
min_value=1000,
max_value=50000,
value=5000,
step=500
)

# Main Dashboard Tabs

tab1, tab2, tab3, tab4, tab5 = st.tabs([
“📊 Executive Dashboard”,
“🎯 Lead Generation”,
“🗺️ Territory Analysis”,
“📈 Predictive Forecasts”,
“👥 Customer Insights”
])

# TAB 1: Executive Dashboard

with tab1:
col1, col2, col3, col4 = st.columns(4)

```
# KPI Metrics
with col1:
    st.metric(
        label="Monthly Leads",
        value="187",
        delta="+23 vs last month"
    )

with col2:
    st.metric(
        label="Conversion Rate",
        value="28.5%",
        delta="+3.2%"
    )

with col3:
    st.metric(
        label="Revenue (MTD)",
        value="$241,500",
        delta="+$45,300"
    )

with col4:
    st.metric(
        label="Pipeline Value",
        value="$1.2M",
        delta="+18%"
    )

st.markdown("---")

# Sales Funnel
col1, col2 = st.columns(2)

with col1:
    st.subheader("Sales Funnel Performance")
    funnel_data = pd.DataFrame({
        'Stage': ['Leads', 'Qualified', 'Inspection', 'Proposal', 'Closed'],
        'Count': [187, 142, 98, 67, 53],
        'Value': [841500, 639000, 441000, 301500, 238500]
    })
    
    fig = go.Figure(go.Funnel(
        y=funnel_data['Stage'],
        x=funnel_data['Count'],
        textinfo="value+percent initial"
    ))
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Revenue by Service Type")
    revenue_data = pd.DataFrame({
        'Service': ['First Treatment', 'Second Treatment', 'Third Treatment', 'Commercial'],
        'Revenue': [165000, 52500, 12000, 12000]
    })
    
    fig = px.pie(revenue_data, values='Revenue', names='Service', 
                 color_discrete_sequence=px.colors.sequential.Blues)
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)

# Monthly Trend
st.subheader("Revenue & Lead Trend (Last 6 Months)")
months = pd.date_range(end=datetime.now(), periods=6, freq='M')
trend_data = pd.DataFrame({
    'Month': months.strftime('%b %Y'),
    'Revenue': [198000, 215000, 187000, 223000, 241000, 267000],
    'Leads': [142, 156, 134, 168, 187, 198],
    'Conversions': [38, 44, 36, 47, 53, 58]
})

fig = go.Figure()
fig.add_trace(go.Bar(x=trend_data['Month'], y=trend_data['Revenue'], 
                     name='Revenue', yaxis='y', marker_color='lightblue'))
fig.add_trace(go.Scatter(x=trend_data['Month'], y=trend_data['Leads'], 
                        name='Leads', yaxis='y2', marker_color='blue'))
fig.add_trace(go.Scatter(x=trend_data['Month'], y=trend_data['Conversions'], 
                        name='Conversions', yaxis='y2', marker_color='darkblue'))

fig.update_layout(
    yaxis=dict(title='Revenue ($)'),
    yaxis2=dict(title='Count', overlaying='y', side='right'),
    hovermode='x unified',
    height=400
)
st.plotly_chart(fig, use_container_width=True)
```

# TAB 2: Lead Generation

with tab2:
st.subheader(“🎯 Lead Generation Analytics”)

```
# Lead Source Performance
col1, col2 = st.columns([2, 1])

with col1:
    lead_sources = pd.DataFrame({
        'Source': ['Google Ads', 'SEO/Organic', 'Facebook Ads', 
                  'Referrals', 'Direct Mail', 'Home Shows'],
        'Leads': [67, 52, 34, 23, 8, 3],
        'Cost': [3200, 800, 1800, 200, 900, 400],
        'Conversions': [19, 18, 8, 12, 2,
```
