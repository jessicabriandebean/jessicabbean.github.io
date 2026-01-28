# Roof Maxx Market Research & Predictive Analytics Suite

# Comprehensive Python toolkit for Washington State & Canada market analysis

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, r2_score
import folium
from folium.plugins import HeatMap
import geopandas as gpd
from datetime import datetime, timedelta
import requests
import json

# ============================================================================

# SECTION 1: DATA COLLECTION & MARKET RESEARCH FUNCTIONS

# ============================================================================

class MarketResearchCollector:
“””
Collects market data from various sources for Washington State and Canada
“””

```
def __init__(self, api_keys=None):
    """
    Initialize with API keys for data sources
    api_keys: dict with keys like 'census', 'google_maps', 'weather', etc.
    """
    self.api_keys = api_keys or {}
    
def collect_demographic_data(self, region='washington'):
    """
    Collect demographic data for target regions
    
    Data Sources to use:
    - US Census Bureau API: https://www.census.gov/data/developers/data-sets.html
    - Statistics Canada: https://www.statcan.gc.ca/en/developers
    - Local housing authority data
    
    Returns: DataFrame with demographic information
    """
    # Example structure - replace with actual API calls
    if region == 'washington':
        # Washington State counties and demographics
        data = {
            'county': ['King', 'Pierce', 'Snohomish', 'Spokane', 'Clark', 
                      'Thurston', 'Kitsap', 'Yakima', 'Whatcom', 'Benton'],
            'population': [2269675, 921130, 827957, 522798, 503311, 
                          291681, 271473, 256728, 229247, 206873],
            'median_income': [106326, 78936, 95184, 62371, 82614,
                             79683, 81934, 61709, 72977, 84867],
            'median_home_value': [686400, 451200, 589700, 298100, 445900,
                                 398600, 459800, 264100, 475300, 338700],
            'homeownership_rate': [0.61, 0.65, 0.68, 0.62, 0.66,
                                  0.64, 0.66, 0.58, 0.63, 0.68],
            'housing_units': [953923, 363418, 327152, 218234, 199876,
                             123456, 112345, 95432, 98765, 87654],
        }
        df = pd.DataFrame(data)
        
        # Calculate addressable market
        df['est_asphalt_roofs'] = (df['housing_units'] * 
                                  df['homeownership_rate'] * 0.70)  # 70% asphalt
        df['est_qualified_roofs'] = df['est_asphalt_roofs'] * 0.90  # 90% qualify
        df['market_potential_annual'] = df['est_qualified_roofs'] * 0.07  # 7% annual replacement rate
        
    elif region == 'canada':
        # Canadian provinces
        data = {
            'province': ['Ontario', 'British Columbia', 'Alberta', 'Quebec', 
                       'Manitoba', 'Saskatchewan'],
            'population': [14826276, 5214805, 4543111, 8604495, 
                          1383765, 1194803],
            'median_income_cad': [87353, 82851, 97940, 79105, 
                                 77750, 80679],
            'median_home_value_cad': [769800, 876600, 476300, 453200,
                                     347800, 312500],
            'homeownership_rate': [0.69, 0.68, 0.72, 0.61,
                                  0.70, 0.71],
            'housing_units': [5929000, 2100000, 1760000, 3700000,
                             580000, 485000],
        }
        df = pd.DataFrame(data)
        df['est_asphalt_roofs'] = (df['housing_units'] * 
                                  df['homeownership_rate'] * 0.72)
        df['est_qualified_roofs'] = df['est_asphalt_roofs'] * 0.85
        df['market_potential_annual'] = df['est_qualified_roofs'] * 0.065
        
    return df

def collect_weather_data(self, locations):
    """
    Collect weather patterns affecting roof maintenance
    
    Sources:
    - NOAA Climate Data: https://www.ncdc.noaa.gov/cdo-web/webservices/v2
    - Environment Canada: https://weather.gc.ca/
    
    Args:
        locations: list of (lat, lon, name) tuples
    
    Returns: DataFrame with weather statistics
    """
    weather_data = []
    
    for lat, lon, name in locations:
        # Example data structure - replace with API calls
        data = {
            'location': name,
            'latitude': lat,
            'longitude': lon,
            'avg_annual_precip_inches': np.random.uniform(30, 50),
            'freeze_thaw_cycles': np.random.randint(20, 80),
            'avg_high_temp_summer': np.random.uniform(75, 85),
            'avg_low_temp_winter': np.random.uniform(25, 40),
            'snow_days_annual': np.random.randint(5, 30),
            'severe_weather_events': np.random.randint(2, 15),
        }
        weather_data.append(data)
    
    return pd.DataFrame(weather_data)

def collect_housing_age_data(self, region='washington'):
    """
    Collect housing age distribution data
    
    Sources:
    - US Census American Community Survey
    - Canada Mortgage and Housing Corporation (CMHC)
    
    Returns: DataFrame with housing age statistics
    """
    # Example data - replace with actual data collection
    if region == 'washington':
        data = {
            'age_range': ['0-5 years', '6-10 years', '11-15 years', '16-20 years',
                        '21-30 years', '31-50 years', '51+ years'],
            'percentage': [8, 12, 15, 18, 25, 18, 4],
            'avg_roof_age': [3, 8, 13, 18, 25, 20, 25],  # Roofs often replaced
        }
    else:  # canada
        data = {
            'age_range': ['0-5 years', '6-10 years', '11-15 years', '16-20 years',
                        '21-30 years', '31-50 years', '51+ years'],
            'percentage': [7, 11, 14, 17, 27, 19, 5],
            'avg_roof_age': [3, 8, 13, 18, 26, 22, 27],
        }
    
    df = pd.DataFrame(data)
    
    # Calculate ideal treatment window (6-15 year old roofs)
    df['in_treatment_window'] = df['age_range'].isin(['6-10 years', '11-15 years'])
    
    return df

def collect_competitor_data(self, region='washington'):
    """
    Collect competitor information
    
    Sources:
    - Google Maps API for business locations
    - Yelp API for reviews
    - Industry reports
    - State licensing boards
    
    Returns: DataFrame with competitor information
    """
    competitors = {
        'business_name': [
            'ABC Roofing', 'Elite Roof Repair', 'Northwest Roofing Co',
            'Precision Roofing', 'Summit Roof Solutions', 'Pacific Roof Care'
        ],
        'service_type': [
            'Replacement', 'Repair & Replacement', 'Replacement',
            'Replacement & Coating', 'Replacement', 'Coating & Repair'
        ],
        'avg_replacement_cost': [22000, 24500, 19800, 21500, 26000, 23000],
        'avg_coating_cost': [0, 0, 0, 4500, 0, 5200],
        'review_rating': [4.2, 4.7, 3.9, 4.5, 4.8, 4.1],
        'years_in_business': [15, 8, 22, 12, 6, 18],
        'service_area_radius_miles': [30, 25, 50, 20, 15, 35],
    }
    
    return pd.DataFrame(competitors)
```

# ============================================================================

# SECTION 2: PREDICTIVE ANALYTICS MODELS

# ============================================================================

class RoofMaxxPredictiveModel:
“””
Predictive models for market opportunity and sales forecasting
“””

```
def __init__(self):
    self.models = {}
    
def prepare_features(self, df):
    """
    Engineer features for predictive modeling
    """
    features = df.copy()
    
    # Create interaction features
    if 'median_income' in features.columns and 'median_home_value' in features.columns:
        features['income_home_ratio'] = features['median_income'] / features['median_home_value']
    
    if 'population' in features.columns and 'housing_units' in features.columns:
        features['population_density'] = features['population'] / features['housing_units']
    
    return features

def predict_market_penetration(self, demographic_data, marketing_spend, 
                               months_in_market=12):
    """
    Predict market penetration based on demographics and marketing investment
    
    Args:
        demographic_data: DataFrame with market demographics
        marketing_spend: Monthly marketing budget
        months_in_market: Number of months operating in territory
    
    Returns: Predictions DataFrame
    """
    # Feature engineering
    X = self.prepare_features(demographic_data)
    
    # Select relevant features
    feature_cols = ['population', 'median_income', 'median_home_value', 
                   'homeownership_rate', 'market_potential_annual']
    X_model = X[feature_cols].fillna(X[feature_cols].mean())
    
    # Add marketing and time factors
    X_model['marketing_spend'] = marketing_spend
    X_model['months_in_market'] = months_in_market
    X_model['marketing_per_capita'] = marketing_spend / X['population']
    
    # Simulate historical data for training (replace with actual data)
    np.random.seed(42)
    n_samples = len(X_model)
    
    # Create synthetic target variable (sales volume)
    # Formula: base_rate * market_size * marketing_effect * time_effect
    base_conversion = 0.02  # 2% base market capture
    marketing_multiplier = 1 + (X_model['marketing_per_capita'] * 10000)
    time_multiplier = np.minimum(months_in_market / 24, 1.0)  # Ramps up over 24 months
    
    y_potential = (X_model['market_potential_annual'] * 
                  base_conversion * 
                  marketing_multiplier * 
                  time_multiplier)
    
    # Add some realistic variance
    y_actual = y_potential * np.random.uniform(0.7, 1.3, n_samples)
    
    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_model, y_actual)
    
    # Make predictions
    predictions = model.predict(X_model)
    
    # Calculate metrics
    results = X.copy()
    results['predicted_annual_sales'] = predictions
    results['predicted_revenue'] = predictions * 4500  # Avg treatment cost
    results['market_share_percentage'] = (predictions / 
                                         X['market_potential_annual'] * 100)
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': X_model.columns,
        'importance': model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    self.models['penetration'] = model
    
    return results, feature_importance

def forecast_lead_generation(self, base_data, digital_spend, seo_score,
                            content_pieces, review_count):
    """
    Forecast lead generation based on digital marketing inputs
    
    Based on Big Leap case study: 6,268% keyword increase, 30+ leads/month from FAQs
    
    Args:
        base_data: Market baseline data
        digital_spend: Monthly digital marketing spend
        seo_score: SEO optimization score (0-100)
        content_pieces: Number of optimized content pieces
        review_count: Number of customer reviews
    
    Returns: Lead forecast
    """
    # Lead generation model based on proven metrics
    base_leads_per_1k_spend = 15  # Industry baseline
    
    # Multipliers based on optimization
    seo_multiplier = 1 + (seo_score / 100) * 2  # Up to 3x with perfect SEO
    content_multiplier = 1 + (content_pieces / 50) * 1.5  # Diminishing returns
    review_multiplier = 1 + (review_count / 100) * 0.5
    
    # Calculate leads
    monthly_leads = (digital_spend / 1000 * base_leads_per_1k_spend * 
                    seo_multiplier * content_multiplier * review_multiplier)
    
    # Lead quality distribution
    lead_breakdown = {
        'total_leads': monthly_leads,
        'hot_leads': monthly_leads * 0.25,  # Ready to buy
        'warm_leads': monthly_leads * 0.45,  # Interested, needs nurturing
        'cold_leads': monthly_leads * 0.30,  # Early research stage
    }
    
    # Conversion projections (industry averages for home services)
    conversion_rates = {
        'hot_conversion': 0.60,   # 60% of hot leads convert
        'warm_conversion': 0.25,  # 25% of warm leads convert
        'cold_conversion': 0.05,  # 5% of cold leads convert
    }
    
    projected_sales = (
        lead_breakdown['hot_leads'] * conversion_rates['hot_conversion'] +
        lead_breakdown['warm_leads'] * conversion_rates['warm_conversion'] +
        lead_breakdown['cold_leads'] * conversion_rates['cold_conversion']
    )
    
    return {
        'leads': lead_breakdown,
        'conversion_rates': conversion_rates,
        'projected_monthly_sales': projected_sales,
        'projected_monthly_revenue': projected_sales * 4500,
        'cost_per_lead': digital_spend / monthly_leads,
        'cost_per_acquisition': digital_spend / projected_sales,
        'roi': (projected_sales * 4500 - digital_spend) / digital_spend
    }

def seasonal_demand_forecast(self, historical_data=None):
    """
    Forecast seasonal demand patterns
    
    Roof maintenance is highly seasonal - peaks in spring/summer
    """
    if historical_data is None:
        # Create example seasonal pattern
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
                 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        
        # Seasonal multipliers (1.0 = average)
        seasonal_index = [0.4, 0.5, 0.9, 1.3, 1.6, 1.8,
                        1.7, 1.5, 1.2, 0.9, 0.5, 0.4]
        
        forecast = pd.DataFrame({
            'month': months,
            'seasonal_index': seasonal_index,
            'demand_category': ['Low', 'Low', 'Medium', 'High', 'Peak', 'Peak',
                              'Peak', 'High', 'High', 'Medium', 'Low', 'Low']
        })
    else:
        # Use actual historical data for forecasting
        forecast = historical_data
    
    return forecast
```

# ============================================================================

# SECTION 3: GEOSPATIAL ANALYTICS

# ============================================================================

class GeospatialAnalyzer:
“””
Geographic analysis and territory optimization
“””

```
def __init__(self):
    self.maps = {}

def create_market_heatmap(self, demographic_data, metric='market_potential_annual'):
    """
    Create interactive heatmap of market opportunity
    
    Args:
        demographic_data: DataFrame with lat/lon and metrics
        metric: Column to visualize
    
    Returns: Folium map object
    """
    # Example coordinates for Washington State counties
    wa_coordinates = {
        'King': [47.5480, -121.9836],
        'Pierce': [47.0676, -122.1295],
        'Snohomish': [48.0420, -121.7170],
        'Spokane': [47.6588, -117.4260],
        'Clark': [45.7466, -122.5194],
        'Thurston': [46.9965, -122.8890],
        'Kitsap': [47.6477, -122.6413],
        'Yakima': [46.5890, -120.5435],
        'Whatcom': [48.8426, -122.1361],
        'Benton': [46.2632, -119.5419],
    }
    
    # Create base map centered on Washington
    m = folium.Map(
        location=[47.5, -120.5],
        zoom_start=7,
        tiles='OpenStreetMap'
    )
    
    # Add markers for each county/region
    for idx, row in demographic_data.iterrows():
        if 'county' in row:
            location_name = row['county']
        elif 'province' in row:
            location_name = row['province']
        else:
            continue
            
        if location_name in wa_coordinates:
            coords = wa_coordinates[location_name]
            
            # Create popup with market data
            popup_html = f"""
            <div style='width: 200px'>
                <h4>{location_name}</h4>
                <b>Market Potential:</b> {row.get(metric, 0):,.0f}<br>
                <b>Population:</b> {row.get('population', 0):,.0f}<br>
                <b>Median Income:</b> ${row.get('median_income', 0):,.0f}<br>
                <b>Qualified Roofs:</b> {row.get('est_qualified_roofs', 0):,.0f}
            </div>
            """
            
            # Circle size based on metric value
            radius = row.get(metric, 0) / 100
            
            folium.CircleMarker(
                location=coords,
                radius=radius,
                popup=folium.Popup(popup_html, max_width=250),
                color='blue',
                fill=True,
                fillColor='blue',
                fillOpacity=0.6
            ).add_to(m)
    
    self.maps['opportunity_heatmap'] = m
    return m

def optimize_territory_coverage(self, dealer_location, service_radius_miles=30):
    """
    Optimize dealer territory coverage
    
    Args:
        dealer_location: (lat, lon) tuple
        service_radius_miles: Maximum service radius
    
    Returns: Coverage analysis
    """
    # Create map centered on dealer
    m = folium.Map(
        location=dealer_location,
        zoom_start=10,
        tiles='OpenStreetMap'
    )
    
    # Add dealer marker
    folium.Marker(
        dealer_location,
        popup='Dealer Location',
        icon=folium.Icon(color='red', icon='home')
    ).add_to(m)
    
    # Add service radius circle
    folium.Circle(
        dealer_location,
        radius=service_radius_miles * 1609.34,  # Convert miles to meters
        color='blue',
        fill=True,
        fillOpacity=0.2,
        popup=f'{service_radius_miles} mile service radius'
    ).add_to(m)
    
    # Calculate coverage metrics
    coverage = {
        'service_area_sq_miles': np.pi * (service_radius_miles ** 2),
        'estimated_homes_in_radius': None,  # Would calculate from census data
        'drive_time_minutes': service_radius_miles / 0.75,  # Assume 45mph avg
    }
    
    return m, coverage

def competitor_proximity_analysis(self, dealer_locations, competitor_locations):
    """
    Analyze competitive landscape and market gaps
    
    Args:
        dealer_locations: List of (lat, lon, name) for Roof Maxx dealers
        competitor_locations: List of (lat, lon, name, type) for competitors
    
    Returns: Competition analysis map
    """
    # Calculate center point
    all_lats = [loc[0] for loc in dealer_locations + competitor_locations]
    all_lons = [loc[1] for loc in dealer_locations + competitor_locations]
    center = [np.mean(all_lats), np.mean(all_lons)]
    
    m = folium.Map(location=center, zoom_start=8)
    
    # Add Roof Maxx dealers in blue
    for lat, lon, name in dealer_locations:
        folium.Marker(
            [lat, lon],
            popup=f'Roof Maxx: {name}',
            icon=folium.Icon(color='blue', icon='star')
        ).add_to(m)
    
    # Add competitors in red
    for lat, lon, name, comp_type in competitor_locations:
        folium.Marker(
            [lat, lon],
            popup=f'{comp_type}: {name}',
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)
    
    return m
```

# ============================================================================

# SECTION 4: MARKET SEGMENTATION & CUSTOMER ANALYTICS

# ============================================================================

def segment_customer_base(customer_data):
“””
Segment customers using RFM (Recency, Frequency, Monetary) analysis
adapted for roof treatment business

```
Args:
    customer_data: DataFrame with customer transaction history

Returns: Segmented customer data
"""
# Example segmentation logic
segments = {
    'Champions': 'High value, recent customers - upsell to 2nd/3rd treatment',
    'Loyal': 'Regular customers, promote referral program',
    'Potential Loyalists': 'Recent customers, encourage reviews',
    'New Customers': 'First treatment, nurture for retention',
    'At Risk': 'Haven\'t responded to follow-ups, re-engagement campaign',
    'Cant Lose': 'High value but losing, special retention offer',
}

return segments
```

def calculate_customer_lifetime_value(avg_treatment_cost=4500, treatments=3,
referral_rate=0.3):
“””
Calculate CLV for Roof Maxx customer

```
Args:
    avg_treatment_cost: Average treatment price
    treatments: Expected number of treatments (up to 3 possible)
    referral_rate: Percentage of customers who refer others

Returns: CLV breakdown
"""
direct_revenue = avg_treatment_cost * treatments
referral_value = avg_treatment_cost * referral_rate

clv = {
    'direct_revenue': direct_revenue,
    'referral_value': referral_value,
    'total_clv': direct_revenue + referral_value,
    'timespan_years': treatments * 5,  # 5 years between treatments
}

return clv
```

