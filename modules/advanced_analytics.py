"""
Advanced Analytics Module
Extended analytics functions for deeper insights
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional


class AdvancedAnalytics:
    """Advanced analytics functions for business intelligence"""
    
    def __init__(self, analyzer):
        """Initialize with BusinessAnalyzer instance"""
        self.analyzer = analyzer
        self.data = analyzer.data
        self.config = analyzer.config
    
    def forecast_revenue(self, days_ahead: int = 30) -> Dict:
        """Simple revenue forecasting using moving averages"""
        if self.data is None:
            return {}
        
        # Group by date
        daily_revenue = self.data.groupby(
            pd.Grouper(key=self.config['date_col'], freq='D')
        )[self.config['revenue_col']].sum()
        
        # Calculate moving averages
        ma_7 = daily_revenue.rolling(window=7, min_periods=1).mean()
        ma_30 = daily_revenue.rolling(window=30, min_periods=1).mean()
        
        # Simple forecast (using last 7-day average)
        last_avg = ma_7.iloc[-1] if len(ma_7) > 0 else 0
        forecast_total = last_avg * days_ahead
        
        # Calculate confidence interval (simplified)
        std_dev = daily_revenue.std()
        confidence_low = (last_avg - 1.96 * std_dev) * days_ahead
        confidence_high = (last_avg + 1.96 * std_dev) * days_ahead
        
        return {
            'forecast_daily_avg': last_avg,
            'forecast_total': forecast_total,
            'confidence_interval': (max(0, confidence_low), confidence_high),
            'days_ahead': days_ahead,
            'trend': 'increasing' if ma_7.iloc[-1] > ma_30.iloc[-1] else 'decreasing'
        }
    
    def find_cross_sell_opportunities(self, min_support: float = 0.01) -> List[Dict]:
        """Find products frequently bought together"""
        if self.data is None:
            return []
        
        # Group products by transaction
        transaction_products = self.data.groupby(self.config['transaction_col'])[
            self.config['product_col']
        ].apply(list).reset_index()
        
        # Find product pairs
        from itertools import combinations
        product_pairs = {}
        
        for products in transaction_products[self.config['product_col']]:
            if len(products) > 1:
                for pair in combinations(set(products), 2):
                    sorted_pair = tuple(sorted(pair))
                    product_pairs[sorted_pair] = product_pairs.get(sorted_pair, 0) + 1
        
        # Calculate support
        total_transactions = len(transaction_products)
        opportunities = []
        
        for pair, count in sorted(product_pairs.items(), key=lambda x: x[1], reverse=True)[:10]:
            support = count / total_transactions
            if support >= min_support:
                # Get product names
                prod1_name = self.data[self.data[self.config['product_col']] == pair[0]][
                    self.config['description_col']
                ].iloc[0] if len(self.data[self.data[self.config['product_col']] == pair[0]]) > 0 else pair[0]
                
                prod2_name = self.data[self.data[self.config['product_col']] == pair[1]][
                    self.config['description_col']
                ].iloc[0] if len(self.data[self.data[self.config['product_col']] == pair[1]]) > 0 else pair[1]
                
                opportunities.append({
                    'product_1': prod1_name,
                    'product_2': prod2_name,
                    'frequency': count,
                    'support': support * 100,
                    'recommendation': f"Bundle {prod1_name[:20]}... with {prod2_name[:20]}..."
                })
        
        return opportunities
    
    def customer_segmentation_rfm(self) -> Dict:
        """Perform RFM (Recency, Frequency, Monetary) analysis"""
        if self.data is None or 'customer_id' not in self.data.columns:
            # If no customer data, segment by transaction patterns
            return self._segment_by_transaction_patterns()
        
        # Standard RFM if customer data exists
        analysis_date = pd.Timestamp(self.config['analysis_date'])
        
        rfm = self.data.groupby('customer_id').agg({
            self.config['date_col']: lambda x: (analysis_date - x.max()).days,  # Recency
            self.config['transaction_col']: 'nunique',  # Frequency
            self.config['revenue_col']: 'sum'  # Monetary
        })
        
        rfm.columns = ['Recency', 'Frequency', 'Monetary']
        
        # Create segments using quartiles
        for col in ['Recency', 'Frequency', 'Monetary']:
            rfm[f'{col}_Quartile'] = pd.qcut(rfm[col], 4, labels=['Q1', 'Q2', 'Q3', 'Q4'])
        
        # Define customer segments
        def segment_customers(row):
            if row['Recency_Quartile'] == 'Q4' and row['Frequency_Quartile'] == 'Q4':
                return 'Champions'
            elif row['Frequency_Quartile'] == 'Q4':
                return 'Loyal Customers'
            elif row['Recency_Quartile'] == 'Q4':
                return 'Recent Customers'
            elif row['Recency_Quartile'] == 'Q1':
                return 'At Risk'
            else:
                return 'Need Attention'
        
        rfm['Segment'] = rfm.apply(segment_customers, axis=1)
        
        return {
            'segments': rfm['Segment'].value_counts().to_dict(),
            'segment_revenue': rfm.groupby('Segment')['Monetary'].sum().to_dict(),
            'total_customers': len(rfm),
            'avg_recency': rfm['Recency'].mean(),
            'avg_frequency': rfm['Frequency'].mean(),
            'avg_monetary': rfm['Monetary'].mean()
        }
    
    def _segment_by_transaction_patterns(self) -> Dict:
        """Segment based on transaction patterns when no customer data"""
        # Group by transaction to understand buying patterns
        trans_analysis = self.data.groupby(self.config['transaction_col']).agg({
            self.config['revenue_col']: 'sum',
            self.config['product_col']: 'count',
            self.config['date_col']: 'first'
        })
        
        # Categorize transactions
        trans_analysis['size_category'] = pd.cut(
            trans_analysis[self.config['revenue_col']],
            bins=[0, trans_analysis[self.config['revenue_col']].quantile(0.33),
                  trans_analysis[self.config['revenue_col']].quantile(0.67),
                  trans_analysis[self.config['revenue_col']].max()],
            labels=['Small', 'Medium', 'Large']
        )
        
        return {
            'transaction_segments': trans_analysis['size_category'].value_counts().to_dict(),
            'avg_transaction_size': trans_analysis[self.config['revenue_col']].mean(),
            'avg_items_per_transaction': trans_analysis[self.config['product_col']].mean()
        }
    
    def anomaly_detection(self) -> List[Dict]:
        """Detect anomalies in sales patterns"""
        anomalies = []
        
        # Daily revenue anomalies
        daily_revenue = self.data.groupby(
            pd.Grouper(key=self.config['date_col'], freq='D')
        )[self.config['revenue_col']].sum()
        
        if len(daily_revenue) > 3:
            # Calculate z-scores
            z_scores = np.abs(stats.zscore(daily_revenue.dropna()))
            threshold = 2.5  # Anomalies beyond 2.5 standard deviations
            
            anomaly_days = daily_revenue.index[z_scores > threshold]
            for day in anomaly_days:
                anomalies.append({
                    'type': 'revenue_spike',
                    'date': day.strftime('%Y-%m-%d'),
                    'value': daily_revenue[day],
                    'severity': 'high' if z_scores[daily_revenue.index.get_loc(day)] > 3 else 'medium',
                    'description': f'Unusual revenue on {day.strftime("%Y-%m-%d")}: {self.analyzer.format_currency(daily_revenue[day])}'
                })
        
        # Product price anomalies
        product_prices = self.data.groupby(self.config['product_col'])[self.config['revenue_col']].agg(['mean', 'std'])
        for product in product_prices.index[:50]:  # Check top 50 products
            product_data = self.data[self.data[self.config['product_col']] == product]
            if len(product_data) > 5:
                prices = product_data[self.config['revenue_col']] / product_data[self.config['quantity_col']]
                z_scores = np.abs(stats.zscore(prices.dropna()))
                if (z_scores > 3).any():
                    anomalies.append({
                        'type': 'price_anomaly',
                        'product': product,
                        'severity': 'medium',
                        'description': f'Unusual pricing detected for product {product}'
                    })
        
        return anomalies[:10]  # Return top 10 anomalies
    
    def create_trend_analysis(self, figsize=(15, 10)):
        """Create comprehensive trend analysis visualization"""
        fig, axes = plt.subplots(2, 2, figsize=figsize)
        fig.suptitle('Business Trend Analysis', fontsize=16, fontweight='bold')
        
        # 1. Revenue Trend
        ax1 = axes[0, 0]
        daily_revenue = self.data.groupby(
            pd.Grouper(key=self.config['date_col'], freq='D')
        )[self.config['revenue_col']].sum()
        
        ax1.plot(daily_revenue.index, daily_revenue.values, color='#2E86AB', linewidth=1, alpha=0.5)
        ax1.plot(daily_revenue.index, daily_revenue.rolling(7).mean(), color='#D62828', linewidth=2, label='7-day MA')
        ax1.fill_between(daily_revenue.index, 0, daily_revenue.values, alpha=0.3, color='#2E86AB')
        ax1.set_title('Revenue Trend', fontweight='bold')
        ax1.set_xlabel('Date')
        ax1.set_ylabel('Revenue')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # 2. Transaction Volume
        ax2 = axes[0, 1]
        daily_trans = self.data.groupby(
            pd.Grouper(key=self.config['date_col'], freq='D')
        )[self.config['transaction_col']].nunique()
        
        ax2.bar(daily_trans.index, daily_trans.values, color='#52B788', alpha=0.7)
        ax2.set_title('Daily Transactions', fontweight='bold')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Number of Transactions')
        ax2.grid(True, alpha=0.3, axis='y')
        
        # 3. Product Mix Evolution
        ax3 = axes[1, 0]
        weekly_products = self.data.groupby(
            [pd.Grouper(key=self.config['date_col'], freq='W'), self.config['product_col']]
        )[self.config['revenue_col']].sum().reset_index()
        
        top_products = self.analyzer.product_analysis.head(5).index
        for product in top_products:
            product_data = weekly_products[weekly_products[self.config['product_col']] == product]
            if len(product_data) > 0:
                label = self.data[self.data[self.config['product_col']] == product][
                    self.config['description_col']
                ].iloc[0][:20] + '...'
                ax3.plot(product_data[self.config['date_col']], 
                        product_data[self.config['revenue_col']], 
                        marker='o', label=label, linewidth=2)
        
        ax3.set_title('Top 5 Products Weekly Performance', fontweight='bold')
        ax3.set_xlabel('Week')
        ax3.set_ylabel('Revenue')
        ax3.legend(fontsize=8)
        ax3.grid(True, alpha=0.3)
        
        # 4. Day of Week Pattern
        ax4 = axes[1, 1]
        if 'weekday' in self.data.columns:
            dow_revenue = self.data.groupby('weekday')[self.config['revenue_col']].mean()
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            dow_revenue = dow_revenue.reindex(day_order, fill_value=0)
            
            colors = ['#D62828' if day in ['Saturday', 'Sunday'] else '#2E86AB' for day in day_order]
            bars = ax4.bar(range(7), dow_revenue.values, color=colors, alpha=0.8)
            ax4.set_xticks(range(7))
            ax4.set_xticklabels([d[:3] for d in day_order])
            ax4.set_title('Average Revenue by Day of Week', fontweight='bold')
            ax4.set_ylabel('Average Revenue')
            ax4.grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        return fig
    
    def generate_recommendations(self) -> List[Dict]:
        """Generate AI-powered recommendations based on analysis"""
        recommendations = []
        
        # Get insights
        pareto = self.analyzer.get_pareto_insights()
        inventory = self.analyzer.get_inventory_health()
        forecast = self.forecast_revenue()
        cross_sell = self.find_cross_sell_opportunities()
        
        # Revenue concentration recommendation
        if pareto['revenue_from_top_pct'] > 80:
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Risk Management',
                'title': 'Diversify Revenue Sources',
                'description': f"Your top {pareto['top_products_pct']:.0f}% of products generate {pareto['revenue_from_top_pct']:.1f}% of revenue",
                'action': 'Develop marketing campaigns for mid-tier products to reduce concentration risk',
                'expected_impact': 'Reduce business risk by 30%',
                'timeframe': '3 months'
            })
        
        # Inventory optimization
        if inventory['dead_stock_count'] > 5:
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Cash Flow',
                'title': 'Liquidate Dead Inventory',
                'description': f"{inventory['dead_stock_count']} products haven't sold recently",
                'action': 'Run clearance sale with 30-50% discounts on dead stock',
                'expected_impact': f"Free up cash and storage space",
                'timeframe': '2 weeks'
            })
        
        # Cross-selling opportunities
        if cross_sell:
            top_bundle = cross_sell[0]
            recommendations.append({
                'priority': 'MEDIUM',
                'category': 'Revenue Growth',
                'title': 'Implement Product Bundling',
                'description': f"Products frequently bought together: {top_bundle['product_1'][:30]} & {top_bundle['product_2'][:30]}",
                'action': 'Create bundle offers with 5-10% discount',
                'expected_impact': 'Increase average transaction value by 15%',
                'timeframe': '1 month'
            })
        
        # Trend-based recommendation
        if forecast.get('trend') == 'decreasing':
            recommendations.append({
                'priority': 'HIGH',
                'category': 'Revenue Protection',
                'title': 'Address Declining Revenue Trend',
                'description': 'Revenue showing downward trend in recent period',
                'action': 'Review pricing strategy and launch customer retention campaign',
                'expected_impact': 'Stabilize revenue decline',
                'timeframe': 'Immediate'
            })
        
        return sorted(recommendations, key=lambda x: 0 if x['priority'] == 'HIGH' else 1 if x['priority'] == 'MEDIUM' else 2)