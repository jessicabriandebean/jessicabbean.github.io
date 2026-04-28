"""
Product Analytics Engine
A comprehensive analytics system for tracking user behavior, feature adoption,
and product performance metrics.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import json

class ProductAnalytics:
    """
    Core analytics engine for product metrics and user behavior analysis
    """
    
    def __init__(self):
        self.events = None
        self.users = None
        self.sessions = None
        
    def generate_sample_data(self, days: int = 30, num_users: int = 5000) -> None:
        """
        Generate realistic product analytics sample data
        
        Parameters:
        -----------
        days : int
            Number of days of historical data
        num_users : int
            Number of unique users
        """
        np.random.seed(42)
        
        # Generate users
        users_data = []
        for i in range(num_users):
            signup_date = datetime.now() - timedelta(days=np.random.randint(0, days * 2))
            user_segment = np.random.choice(
                ['Power User', 'Regular User', 'Casual User', 'Trial User'],
                p=[0.15, 0.35, 0.35, 0.15]
            )
            
            users_data.append({
                'user_id': f'user_{i:05d}',
                'signup_date': signup_date,
                'user_segment': user_segment,
                'plan': np.random.choice(['free', 'basic', 'premium'], p=[0.6, 0.3, 0.1]),
                'country': np.random.choice(['US', 'UK', 'Canada', 'Germany', 'France'], p=[0.4, 0.2, 0.15, 0.15, 0.1]),
                'device': np.random.choice(['desktop', 'mobile', 'tablet'], p=[0.6, 0.3, 0.1])
            })
        
        self.users = pd.DataFrame(users_data)
        
        # Generate events
        events_data = []
        event_types = [
            'page_view', 'button_click', 'form_submit', 'video_play',
            'download', 'share', 'comment', 'like', 'search', 'purchase'
        ]
        
        features = [
            'dashboard', 'reports', 'analytics', 'settings', 
            'integrations', 'api', 'export', 'notifications'
        ]
        
        for day in range(days):
            event_date = datetime.now() - timedelta(days=day)
            
            # Active users for this day (varies)
            active_users = np.random.randint(int(num_users * 0.4), int(num_users * 0.8))
            selected_users = np.random.choice(self.users['user_id'].values, active_users, replace=False)
            
            for user_id in selected_users:
                # Each user generates multiple events
                num_events = np.random.poisson(15)
                
                for _ in range(num_events):
                    event_time = event_date + timedelta(
                        hours=np.random.randint(0, 24),
                        minutes=np.random.randint(0, 60)
                    )
                    
                    events_data.append({
                        'event_id': f'evt_{len(events_data)}',
                        'user_id': user_id,
                        'event_type': np.random.choice(event_types, p=[0.3, 0.2, 0.1, 0.08, 0.07, 0.06, 0.05, 0.05, 0.05, 0.04]),
                        'feature': np.random.choice(features, p=[0.25, 0.2, 0.15, 0.12, 0.1, 0.08, 0.06, 0.04]),
                        'timestamp': event_time,
                        'session_id': f'session_{user_id}_{day}_{np.random.randint(0, 5)}',
                        'duration_seconds': np.random.randint(10, 600)
                    })
        
        self.events = pd.DataFrame(events_data)
        self.events = self.events.merge(self.users[['user_id', 'user_segment', 'plan']], on='user_id')
        
    def calculate_dau_mau(self, date_col: str = 'timestamp') -> pd.DataFrame:
        """Calculate Daily Active Users and Monthly Active Users"""
        self.events[date_col] = pd.to_datetime(self.events[date_col])
        
        # DAU
        dau = self.events.groupby(self.events[date_col].dt.date)['user_id'].nunique().reset_index()
        dau.columns = ['date', 'dau']
        
        # Convert date back to datetime for proper comparison
        dau['date'] = pd.to_datetime(dau['date'])
        
        # MAU (rolling 30 days) - FIXED VERSION
        mau_list = []
        for i, row in dau.iterrows():
            current_date = row['date']
            # Get all events in the last 30 days including current date
            date_30_days_ago = current_date - pd.Timedelta(days=29)  # 29 + today = 30 days
            
            mask = (self.events[date_col] >= date_30_days_ago) & (self.events[date_col] <= current_date)
            mau = self.events[mask]['user_id'].nunique()
            mau_list.append(mau)
        
        dau['mau'] = mau_list
        
        # Stickiness (DAU/MAU) — replace 0 MAU with NaN to avoid inf
        dau['stickiness'] = (dau['dau'] / dau['mau'].replace(0, np.nan) * 100).round(2)
        
        # Convert date back to date type for display
        dau['date'] = dau['date'].dt.date
        
        return dau

    def calculate_retention(self, cohort_periods: int = 8) -> pd.DataFrame:
        """
        Calculate cohort retention analysis
        
        Parameters:
        -----------
        cohort_periods : int
            Number of periods to track retention
            
        Returns:
        --------
        DataFrame with cohort retention rates
        """
        # Get user cohorts based on signup week
        self.users['cohort'] = pd.to_datetime(self.users['signup_date']).dt.to_period('W')
        
        # Get user activity by week
        self.events['event_week'] = pd.to_datetime(self.events['timestamp']).dt.to_period('W')
        
        user_activity = self.events.groupby(['user_id', 'event_week']).size().reset_index(name='events')
        user_activity = user_activity.merge(self.users[['user_id', 'cohort']], on='user_id')
        
        # Calculate periods since cohort
        user_activity['period'] = (user_activity['event_week'] - user_activity['cohort']).apply(lambda x: x.n)
        
        # Count active users per cohort per period
        cohort_data = user_activity.groupby(['cohort', 'period'])['user_id'].nunique().reset_index()
        cohort_data.columns = ['cohort', 'period', 'active_users']
        
        # Get cohort sizes
        cohort_sizes = user_activity.groupby('cohort')['user_id'].nunique().reset_index()
        cohort_sizes.columns = ['cohort', 'cohort_size']
        
        # Calculate retention percentage
        retention = cohort_data.merge(cohort_sizes, on='cohort')
        retention['retention_rate'] = (retention['active_users'] / retention['cohort_size'] * 100).round(2)
        
        return retention[retention['period'] <= cohort_periods]
    
    def calculate_funnel(self, funnel_steps: List[str]) -> pd.DataFrame:
        """
        Calculate conversion funnel metrics
        
        Parameters:
        -----------
        funnel_steps : list
            List of event types representing funnel steps
            
        Returns:
        --------
        DataFrame with funnel conversion rates
        """
        funnel_data = []
        
        for i, step in enumerate(funnel_steps):
            users_in_step = self.events[self.events['event_type'] == step]['user_id'].nunique()
            
            funnel_data.append({
                'step': step,
                'step_number': i + 1,
                'users': users_in_step
            })
        
        funnel_df = pd.DataFrame(funnel_data)
        
        # Calculate conversion rates
        total_users = funnel_df.iloc[0]['users']
        funnel_df['conversion_rate'] = (funnel_df['users'] / total_users * 100).round(2)
        funnel_df['drop_off'] = funnel_df['users'].diff().fillna(0).abs()
        
        return funnel_df
    
    def calculate_feature_adoption(self) -> pd.DataFrame:
        """Calculate feature adoption metrics"""
        feature_stats = self.events.groupby('feature').agg({
            'user_id': 'nunique',
            'event_id': 'count'
        }).reset_index()
        
        feature_stats.columns = ['feature', 'unique_users', 'total_events']
        
        total_users = self.users.shape[0]
        feature_stats['adoption_rate'] = (feature_stats['unique_users'] / total_users * 100).round(2)
        feature_stats['avg_events_per_user'] = (feature_stats['total_events'] / feature_stats['unique_users']).round(2)
        
        return feature_stats.sort_values('unique_users', ascending=False)
    
    def calculate_user_segments(self) -> Dict:
        """Analyze user segments"""
        segments = {}
        
        for segment in self.users['user_segment'].unique():
            segment_users = self.users[self.users['user_segment'] == segment]['user_id'].values
            segment_events = self.events[self.events['user_id'].isin(segment_users)]
            
            segments[segment] = {
                'count': len(segment_users),
                'avg_events_per_user': len(segment_events) / len(segment_users),
                'most_used_feature': segment_events['feature'].mode()[0] if len(segment_events) > 0 else None,
                'avg_session_duration': segment_events['duration_seconds'].mean()
            }
        
        return segments
    
    def calculate_revenue_metrics(self) -> pd.DataFrame:
        """Calculate revenue and monetization metrics"""
        # Simulate purchase events with revenue
        purchases = self.events[self.events['event_type'] == 'purchase'].copy()
        
        # Assign revenue based on plan
        plan_prices = {'free': 0, 'basic': 29, 'premium': 99}
        purchases = purchases.merge(self.users[['user_id', 'plan']], on='user_id')
        purchases['revenue'] = purchases['plan'].map(plan_prices)
        
        # Daily revenue
        purchases['date'] = pd.to_datetime(purchases['timestamp']).dt.date
        daily_revenue = purchases.groupby('date').agg({
            'revenue': 'sum',
            'user_id': 'nunique'
        }).reset_index()
        
        daily_revenue.columns = ['date', 'revenue', 'paying_users']
        daily_revenue['arpu'] = (daily_revenue['revenue'] / daily_revenue['paying_users']).round(2)
        
        return daily_revenue
    
    def calculate_engagement_score(self) -> pd.DataFrame:
        """
        Calculate user engagement scores based on multiple factors
        """
        user_metrics = self.events.groupby('user_id').agg({
            'event_id': 'count',
            'session_id': 'nunique',
            'duration_seconds': 'mean',
            'feature': lambda x: x.nunique()
        }).reset_index()
        
        user_metrics.columns = ['user_id', 'total_events', 'num_sessions', 'avg_duration', 'features_used']
        
        # Normalize metrics
        from sklearn.preprocessing import MinMaxScaler
        scaler = MinMaxScaler()
        
        metrics_to_scale = ['total_events', 'num_sessions', 'avg_duration', 'features_used']
        user_metrics[metrics_to_scale] = scaler.fit_transform(user_metrics[metrics_to_scale])
        
        # Calculate engagement score (weighted average)
        user_metrics['engagement_score'] = (
            user_metrics['total_events'] * 0.3 +
            user_metrics['num_sessions'] * 0.25 +
            user_metrics['avg_duration'] * 0.25 +
            user_metrics['features_used'] * 0.2
        ) * 100
        
        user_metrics['engagement_score'] = user_metrics['engagement_score'].round(2)
        
        # Categorize engagement
        user_metrics['engagement_level'] = pd.cut(
            user_metrics['engagement_score'],
            bins=[0, 25, 50, 75, 100],
            labels=['Low', 'Medium', 'High', 'Very High']
        )
        
        return user_metrics.sort_values('engagement_score', ascending=False)
    
    def detect_churned_users(self, inactive_days: int = 30) -> pd.DataFrame:
        """
        Identify users at risk of churning
        
        Parameters:
        -----------
        inactive_days : int
            Number of days of inactivity to consider churned
        """
        last_activity = self.events.groupby('user_id')['timestamp'].max().reset_index()
        last_activity.columns = ['user_id', 'last_activity']
        last_activity['last_activity'] = pd.to_datetime(last_activity['last_activity'])
        
        today = datetime.now()
        last_activity['days_inactive'] = (today - last_activity['last_activity']).dt.days
        
        churned = last_activity[last_activity['days_inactive'] >= inactive_days].copy()
        churned = churned.merge(self.users[['user_id', 'user_segment', 'plan']], on='user_id')
        
        return churned.sort_values('days_inactive', ascending=False)
    
    def generate_insights(self) -> Dict[str, str]:
        """Generate automated insights from the data"""
        insights = {}
        
        # DAU/MAU
        dau_mau = self.calculate_dau_mau()
        avg_stickiness = dau_mau['stickiness'].mean()
        insights['stickiness'] = f"Average DAU/MAU ratio is {avg_stickiness:.1f}%, indicating {'strong' if avg_stickiness > 20 else 'moderate'} user engagement"
        
        # Feature adoption
        features = self.calculate_feature_adoption()
        top_feature = features.iloc[0]
        insights['feature_adoption'] = f"Top feature '{top_feature['feature']}' has {top_feature['adoption_rate']:.1f}% adoption rate"
        
        # User segments
        segments = self.calculate_user_segments()
        power_users = segments.get('Power User', {})
        insights['power_users'] = f"Power users generate {power_users.get('avg_events_per_user', 0):.1f} events per user on average"
        
        # Churn
        churned = self.detect_churned_users()
        churn_rate = (len(churned) / len(self.users) * 100)
        insights['churn'] = f"Churn rate is {churn_rate:.1f}% - {len(churned)} users inactive for 30+ days"
        
        return insights
    
    def export_report(self, filename: str = 'product_analytics_report.json') -> None:
        """Export comprehensive analytics report"""
        report = {
            'generated_at': datetime.now().isoformat(),
            'summary': {
                'total_users': len(self.users),
                'total_events': len(self.events),
                'date_range': {
                    'start': self.events['timestamp'].min().isoformat(),
                    'end': self.events['timestamp'].max().isoformat()
                }
            },
            'insights': self.generate_insights(),
            'metrics': {
                'dau_mau': self.calculate_dau_mau().to_dict('records'),
                'feature_adoption': self.calculate_feature_adoption().to_dict('records'),
                'user_segments': self.calculate_user_segments()
            }
        }
        
        with open(filename, 'w') as f:
            json.dump(report, f, indent=2, default=str)
        
        print(f"Report exported to {filename}")


# Example usage
if __name__ == "__main__":
    print("="*70)
    print("PRODUCT ANALYTICS ENGINE")
    print("="*70)
    
    # Initialize analytics
    analytics = ProductAnalytics()
    
    # Generate sample data
    print("\n📊 Generating sample data...")
    analytics.generate_sample_data(days=30, num_users=5000)
    print(f"Generated {len(analytics.events):,} events for {len(analytics.users):,} users")
    
    # Calculate DAU/MAU
    print("\n" + "="*70)
    print("DAU/MAU ANALYSIS")
    print("="*70)
    dau_mau = analytics.calculate_dau_mau()
    print(f"\nRecent metrics:")
    print(dau_mau.tail(7))
    print(f"\nAverage Stickiness: {dau_mau['stickiness'].mean():.2f}%")
    
    # Retention analysis
    print("\n" + "="*70)
    print("COHORT RETENTION")
    print("="*70)
    retention = analytics.calculate_retention()
    print(retention.head(10))
    
    # Feature adoption
    print("\n" + "="*70)
    print("FEATURE ADOPTION")
    print("="*70)
    features = analytics.calculate_feature_adoption()
    print(features)
    
    # Engagement scores
    print("\n" + "="*70)
    print("USER ENGAGEMENT")
    print("="*70)
    engagement = analytics.calculate_engagement_score()
    print(f"\nTop 10 Most Engaged Users:")
    print(engagement[['user_id', 'engagement_score', 'engagement_level']].head(10))
    
    # Insights
    print("\n" + "="*70)
    print("KEY INSIGHTS")
    print("="*70)
    insights = analytics.generate_insights()
    for key, value in insights.items():
        print(f"\n• {value}")
    
    # Export report
    print("\n" + "="*70)
    analytics.export_report()
    print("\n✅ Analysis complete!")