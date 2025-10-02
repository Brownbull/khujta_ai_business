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
from typing import Dict, List
import warnings
warnings.filterwarnings('ignore')

from modules.business_analytics import BusinessAnalyzer


class AdvancedAnalytics:
    """
    Advanced analytics that works with a BusinessAnalyzer instance.
    Uses composition to access business data and basic analytics.
    """

    def __init__(self, analyzer: BusinessAnalyzer):
        """
        Initialize advanced analytics with a BusinessAnalyzer instance

        Args:
            analyzer: BusinessAnalyzer instance (which extends Business)
        """
        if not isinstance(analyzer, BusinessAnalyzer):
            raise TypeError("Expected BusinessAnalyzer instance")

        self.analyzer = analyzer
        self.trend_analysis = None
        print(f"AdvancedAnalytics initialized for project: {self.analyzer.config['project_name']}")

    # CALCULATION METHODS

    def calculate_revenue_forecast(self, days_ahead: int = 30) -> Dict:
        """Calculate revenue forecasting using moving averages"""
        if self.analyzer.data is None:
            return {}

        # Group by date
        daily_data = self.analyzer.data.groupby(pd.Grouper(key=self.analyzer.config['date_col'], freq='D')) # Group by date
        daily_revenue = daily_data[self.analyzer.config['revenue_col']].sum() # Sum revenue per day

        # Calculate moving averages
        ma_7 = daily_revenue.rolling(window=7, min_periods=1).mean() # 7-day MA
        ma_30 = daily_revenue.rolling(window=30, min_periods=1).mean() # 30-day MA

        # Simple forecast (using last 7-day average)
        last_avg_daily = ma_7.iloc[-1] if len(ma_7) > 0 else 0 # Last 7-day MA
        forecast_total = last_avg_daily * days_ahead # Forecast total for next period

        z_score = 1.96 # 95% confidence interval z-score
        # Calculate confidence interval (simplified)
        std_dev = daily_revenue.std() # Standard deviation of daily revenue
        confidence_low_daily = (last_avg_daily - z_score * std_dev) # 95% CI lower bound
        confidence_high_daily = (last_avg_daily + z_score * std_dev) # 95% CI upper bound
        confidence_low = confidence_low_daily * days_ahead # Total lower bound
        confidence_high = confidence_high_daily * days_ahead # Total upper bound

        return {
            'forecast_daily_avg': last_avg_daily,
            'daily_std_dev': std_dev,
            'confidence_interval_daily': (max(0, confidence_low_daily), confidence_high_daily),
            'forecast_total': forecast_total,
            'confidence_interval_total': (max(0, confidence_low), confidence_high),
            'days_ahead': days_ahead,
            'trend': 'increasing' if ma_7.iloc[-1] > ma_30.iloc[-1] else 'decreasing'
        }

    def calculate_cross_sell_opportunities(self, min_support: float = 0.01, limit: int = 3) -> List[Dict]:
        """Find products frequently bought together"""
        if self.analyzer.data is None:
            return []

        # Group products by transaction
        transaction_products = self.analyzer.data.groupby(self.analyzer.config['transaction_col'])[
            self.analyzer.config['product_col']
        ].apply(list).reset_index()

        # Find product pairs
        from itertools import combinations
        product_pairs = {}

        for products in transaction_products[self.analyzer.config['product_col']]:
            if len(products) > 1:
                for pair in combinations(set(products), 2):
                    sorted_pair = tuple(sorted(pair))
                    product_pairs[sorted_pair] = product_pairs.get(sorted_pair, 0) + 1

        # Calculate support
        total_transactions = len(transaction_products)
        opportunities = []

        for pair, count in sorted(product_pairs.items(), key=lambda x: x[1], reverse=True):
            support = count / total_transactions
            if support >= min_support:
                # Get product names
                prod1_name = self.analyzer.data[self.analyzer.data[self.analyzer.config['product_col']] == pair[0]][
                    self.analyzer.config['description_col']
                ].iloc[0] if len(self.analyzer.data[self.analyzer.data[self.analyzer.config['product_col']] == pair[0]]) > 0 else pair[0]

                prod2_name = self.analyzer.data[self.analyzer.data[self.analyzer.config['product_col']] == pair[1]][
                    self.analyzer.config['description_col']
                ].iloc[0] if len(self.analyzer.data[self.analyzer.data[self.analyzer.config['product_col']] == pair[1]]) > 0 else pair[1]

                opportunities.append({
                    'product_1': prod1_name,
                    'product_2': prod2_name,
                    'frequency': count,
                    'support': support * 100,
                    'recommendation': f"Bundle {prod1_name[:20]}... with {prod2_name[:20]}..."
                })
                if len(opportunities) >= limit:
                    break

        return opportunities

    def calculate_customer_segmentation_rfm(self) -> Dict:
        """Perform RFM (Recency, Frequency, Monetary) analysis"""
        if self.analyzer.data is None or self.analyzer.config['customer_col'] not in self.analyzer.data.columns:
            return self._segment_by_transaction_patterns()

        # Standard RFM if customer data exists
        analysis_date = pd.Timestamp(self.analyzer.config['analysis_date'])

        rfm = self.analyzer.data.groupby(self.analyzer.config['customer_col']).agg({
            self.analyzer.config['date_col']: lambda x: (analysis_date - x.max()).days,
            self.analyzer.config['transaction_col']: 'nunique',
            self.analyzer.config['revenue_col']: 'sum'
        })

        rfm.columns = ['Recency', 'Frequency', 'Monetary']

        # Create segments using quartiles (or fewer if data has duplicates)
        for col in ['Recency', 'Frequency', 'Monetary']:
            try:
                # Try to create quartiles with labels
                rfm[f'{col}_Quartile'] = pd.qcut(rfm[col], 4, labels=['Q1', 'Q2', 'Q3', 'Q4'])
            except ValueError:
                # If quartiles fail due to duplicates, use duplicates='drop' without labels
                rfm[f'{col}_Quartile'] = pd.qcut(rfm[col], 4, duplicates='drop')

        # Define customer segments (handle both string labels and numeric values)
        def segment_customers(row):
            # Get max values for each quartile column to handle both labeled and numeric quartiles
            r_max = rfm['Recency_Quartile'].max()
            f_max = rfm['Frequency_Quartile'].max()
            r_min = rfm['Recency_Quartile'].min()

            # Check if it's the highest quartile (best)
            if row['Recency_Quartile'] == r_max and row['Frequency_Quartile'] == f_max:
                return 'Champions'
            elif row['Frequency_Quartile'] == f_max:
                return 'Loyal Customers'
            elif row['Recency_Quartile'] == r_max:
                return 'Recent Customers'
            elif row['Recency_Quartile'] == r_min:
                return 'At Risk'
            else:
                return 'Need Attention'

        rfm['Segment'] = rfm.apply(segment_customers, axis=1)

        # Store RFM data for detailed reports
        self.rfm_data = rfm.copy()

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
        trans_analysis = self.analyzer.data.groupby(self.analyzer.config['transaction_col']).agg({
            self.analyzer.config['revenue_col']: 'sum',
            self.analyzer.config['product_col']: 'count',
            self.analyzer.config['date_col']: 'first'
        })

        # Categorize transactions
        trans_analysis['size_category'] = pd.cut(
            trans_analysis[self.analyzer.config['revenue_col']],
            bins=[0, trans_analysis[self.analyzer.config['revenue_col']].quantile(0.33),
                  trans_analysis[self.analyzer.config['revenue_col']].quantile(0.67),
                  trans_analysis[self.analyzer.config['revenue_col']].max()],
            labels=['Small', 'Medium', 'Large']
        )

        return {
            'transaction_segments': trans_analysis['size_category'].value_counts().to_dict(),
            'avg_transaction_size': trans_analysis[self.analyzer.config['revenue_col']].mean(),
            'avg_items_per_transaction': trans_analysis[self.analyzer.config['product_col']].mean()
        }

    def calculate_anomalies(self, limit: int = 3) -> List[Dict]:
        """Detect anomalies in sales patterns"""
        anomalies = []

        # Daily revenue anomalies
        daily_revenue = self.analyzer.data.groupby(
            pd.Grouper(key=self.analyzer.config['date_col'], freq='D')
        )[self.analyzer.config['revenue_col']].sum()

        if len(daily_revenue) > 3:
            # Calculate z-scores
            z_scores = np.abs(stats.zscore(daily_revenue.dropna()))
            threshold = 2.5

            anomaly_days = daily_revenue.index[z_scores > threshold]
            for day in anomaly_days:
                anomalies.append({
                    'type': 'revenue_spike',
                    'date': day.strftime('%Y-%m-%d'),
                    'value': daily_revenue[day],
                    'severity': 'high' if z_scores[daily_revenue.index.get_loc(day)] > 3 else 'medium',
                    'description': f'Unusual revenue on {day.strftime("%Y-%m-%d")}: {self.analyzer.format_currency(daily_revenue[day])}'
                })
                if len(anomalies) >= limit:
                    break

        if len(anomalies) < limit:
            # Product price anomalies
            product_prices = self.analyzer.data.groupby(self.analyzer.config['product_col'])[self.analyzer.config['revenue_col']].agg(['mean', 'std'])
            for product in product_prices.index[:50]:
                product_data = self.analyzer.data[self.analyzer.data[self.analyzer.config['product_col']] == product]
                if len(product_data) > 5:
                    prices = product_data[self.analyzer.config['revenue_col']] / product_data[self.analyzer.config['quantity_col']]
                    z_scores = np.abs(stats.zscore(prices.dropna()))
                    if (z_scores > 3).any():
                        anomalies.append({
                            'type': 'price_anomaly',
                            'product': product,
                            'severity': 'medium',
                            'description': f'Unusual pricing detected for product {product}'
                        })

        return anomalies

    def calculate_recommendations(self) -> List[Dict]:
        """Generate recommendations based on analysis"""
        recommendations = []

        # Get insights
        pareto = self.analyzer.get_pareto_insights()
        inventory = self.analyzer.get_inventory_health()
        forecast = self.calculate_revenue_forecast()
        cross_sell = self.calculate_cross_sell_opportunities()

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

    # PRINT/FORMAT METHODS

    def print_revenue_forecast(self, days_ahead: int = 30) -> str:
        """Format revenue forecast as string"""
        forecast = self.calculate_revenue_forecast(days_ahead)

        if not forecast:
            return "No forecast data available"

        forecast_str = []
        forecast_str.append(f"📈 Revenue Forecast for next {days_ahead} days:")
        forecast_str.append(f" Daily:")
        forecast_str.append(f" - Average: {self.analyzer.format_currency(forecast['forecast_daily_avg'])}")
        forecast_str.append(f" - Std Dev: {self.analyzer.format_currency(forecast['daily_std_dev'])}")
        forecast_str.append(f" - 95% Confidence Interval: ({self.analyzer.format_currency(forecast['confidence_interval_daily'][0])}, {self.analyzer.format_currency(forecast['confidence_interval_daily'][1])})")
        forecast_str.append(f" Total:")
        forecast_str.append(f" - Forecast: {self.analyzer.format_currency(forecast['forecast_total'])}")
        forecast_str.append(f" - 95% Confidence Interval: ({self.analyzer.format_currency(forecast['confidence_interval_total'][0])}, {self.analyzer.format_currency(forecast['confidence_interval_total'][1])})")
        forecast_str.append(f" - Trend: {forecast['trend'].capitalize()}")

        return "\n".join(forecast_str)

    def print_cross_sell_opportunities(self, min_support: float = 0.01, limit: int = 3) -> str:
        """Format cross-sell opportunities as string"""
        opportunities = self.calculate_cross_sell_opportunities(min_support, limit)

        if not opportunities:
            return "ℹ️ No significant cross-sell opportunities found."

        xsell_str = []
        xsell_str.append("🛍️ Cross-Sell Opportunities:")
        for opp in opportunities:
            xsell_str.append(f"  • {opp['product_1'][:30]} & {opp['product_2'][:30]}")
            xsell_str.append(f"    Frequency: {opp['frequency']} | Support: {opp['support']:.2f}%")
            xsell_str.append(f"    → {opp['recommendation']}")

        return "\n".join(xsell_str)

    def print_anomalies(self, limit: int = 3) -> str:
        """Format anomalies as string"""
        anomalies = self.calculate_anomalies(limit)

        if not anomalies:
            return "ℹ️ No anomalies detected."

        anomalies_str = []
        anomalies_str.append("⚠️ Anomalies Detected:")
        for anomaly in anomalies:
            anomalies_str.append(f"  • {anomaly['description']}")

        return "\n".join(anomalies_str)

    def print_recommendations(self) -> str:
        """Format recommendations as string"""
        recommendations = self.calculate_recommendations()

        if not recommendations:
            return "ℹ️ No actionable recommendations found."

        recmm_str = []
        recmm_str.append("\n💡 TOP RECOMMENDATIONS:")
        for i, rec in enumerate(recommendations[:3], 1):
            recmm_str.append(f"\n{i}. [{rec['priority']}] {rec['title']}")
            recmm_str.append(f"   {rec['description']}")
            recmm_str.append(f"   Action: {rec['action']}")
            recmm_str.append(f"   Impact: {rec['expected_impact']} | Timeline: {rec['timeframe']}")

        return "\n".join(recmm_str)
    
    def print_customer_segmentation(self) -> str:
        """Format customer segmentation as string"""
        rfm_segmentation = self.calculate_customer_segmentation_rfm()
        
        # Format output
        rfm_str = []
        rfm_str.append("👥 Customer/Transaction Segmentation Analysis\n")
        if 'segments' in rfm_segmentation:
            rfm_str.append("Customer Segments:")
            for segment, count in rfm_segmentation['segments'].items():
                rfm_str.append(f"  • {segment}: {count} customers")
            rfm_str.append(f"\nTotal Customers: {rfm_segmentation['total_customers']}")
            rfm_str.append(f"Avg Recency: {rfm_segmentation['avg_recency']:.1f} days")
            rfm_str.append(f"Avg Frequency: {rfm_segmentation['avg_frequency']:.1f} transactions")
            rfm_str.append(f"Avg Monetary: {self.analyzer.format_currency(rfm_segmentation['avg_monetary'])}")
        else:
            rfm_str.append("Transaction Size Segments:")
            for segment, count in rfm_segmentation['transaction_segments'].items():
                rfm_str.append(f"  • {segment}: {count} transactions")
            rfm_str.append(f"\nAvg Transaction Size: {self.analyzer.format_currency(rfm_segmentation['avg_transaction_size'])}")
            rfm_str.append(f"Avg Items per Transaction: {rfm_segmentation['avg_items_per_transaction']:.1f}")

        return '\n'.join(rfm_str)

    def calculate_detailed_customer_segments(self, top_n: int = 5) -> Dict:
        """Get detailed customer information for top N customers per segment"""
        # Ensure RFM calculation has been run
        if not hasattr(self, 'rfm_data') or self.rfm_data is None:
            self.calculate_customer_segmentation_rfm()

        if not hasattr(self, 'rfm_data') or self.rfm_data is None:
            return {'error': 'No customer data available for detailed segmentation'}

        # Get customer metadata (name, location) from original data if available
        customer_col = self.analyzer.config['customer_col']
        customer_meta = pd.DataFrame()

        # Build aggregation dictionary dynamically based on available columns
        agg_dict = {}
        if 'customer_name' in self.analyzer.data.columns:
            agg_dict['customer_name'] = 'first'
        if 'customer_location' in self.analyzer.data.columns:
            agg_dict['customer_location'] = 'first'

        # Only aggregate if we have metadata columns
        if agg_dict:
            customer_meta = self.analyzer.data.groupby(customer_col).agg(agg_dict)

        # Prepare detailed segments
        detailed_segments = {}

        for segment in self.rfm_data['Segment'].unique():
            segment_customers = self.rfm_data[self.rfm_data['Segment'] == segment].copy()

            # Sort by Monetary value (highest spenders first)
            segment_customers = segment_customers.sort_values('Monetary', ascending=False)

            # Get top N customers
            top_customers = segment_customers.head(top_n)

            customers_list = []
            for customer_id, row in top_customers.iterrows():
                customer_info = {
                    'customer_id': customer_id,
                    'recency': row['Recency'],
                    'frequency': row['Frequency'],
                    'monetary': row['Monetary'],
                    'recency_quartile': str(row['Recency_Quartile']),
                    'frequency_quartile': str(row['Frequency_Quartile']),
                    'monetary_quartile': str(row['Monetary_Quartile'])
                }

                # Add customer metadata if available
                if not customer_meta.empty and customer_id in customer_meta.index:
                    if 'customer_name' in customer_meta.columns:
                        customer_info['name'] = customer_meta.loc[customer_id, 'customer_name']
                    if 'customer_location' in customer_meta.columns:
                        customer_info['location'] = customer_meta.loc[customer_id, 'customer_location']

                customers_list.append(customer_info)

            detailed_segments[segment] = {
                'total_count': len(segment_customers),
                'top_customers': customers_list
            }

        return detailed_segments

    def print_detailed_customer_segments(self, top_n: int = 5) -> str:
        """Format detailed customer segmentation as string"""
        detailed_segments = self.calculate_detailed_customer_segments(top_n=top_n)

        if 'error' in detailed_segments:
            return f"ℹ️ {detailed_segments['error']}"

        # Segment emoji mapping
        segment_emojis = {
            'Champions': '🏆',
            'Loyal Customers': '🔵',
            'Recent Customers': '🟢',
            'At Risk': '🔴',
            'Need Attention': '🟡'
        }

        # Segment order for display
        segment_order = ['Champions', 'Loyal Customers', 'Recent Customers', 'Need Attention', 'At Risk']

        output = []
        output.append("=" * 60)
        output.append("DETAILED CUSTOMER SEGMENTATION REPORT")
        output.append("=" * 60)
        output.append("")

        # Process segments in order
        for segment in segment_order:
            if segment not in detailed_segments:
                continue

            segment_data = detailed_segments[segment]
            emoji = segment_emojis.get(segment, '📊')

            output.append(f"\n{emoji} {segment.upper()} ({segment_data['total_count']} customers)")
            output.append("━" * 60)

            for i, customer in enumerate(segment_data['top_customers'], 1):
                # Build customer header line
                customer_line = f"\n#{i}: {customer['customer_id']}"
                if 'name' in customer:
                    customer_line += f" - {customer['name']}"
                if 'location' in customer:
                    customer_line += f" ({customer['location']})"
                output.append(customer_line)

                output.append(f"    💰 Total Revenue: {self.analyzer.format_currency(customer['monetary'])}")
                output.append(f"    📅 Last Purchase: {int(customer['recency'])} day{'s' if customer['recency'] != 1 else ''} ago")
                output.append(f"    🔄 Transactions: {int(customer['frequency'])} purchase{'s' if customer['frequency'] != 1 else ''}")
                output.append("")
                output.append(f"    📊 RFM Score: R[{customer['recency_quartile']}] F[{customer['frequency_quartile']}] M[{customer['monetary_quartile']}]")
                output.append("")

                # Generate explanation
                explanation = self._generate_segment_explanation(segment, customer)
                output.append(f"    ✨ Why {segment}?")
                for line in explanation:
                    output.append(f"    {line}")

                if i < len(segment_data['top_customers']):
                    output.append("")

            output.append("\n" + "━" * 60)

        return '\n'.join(output)

    def _generate_segment_explanation(self, segment: str, customer: Dict) -> list:
        """Generate business-friendly explanation for why customer is in segment"""
        explanations = []

        r_q = customer['recency_quartile']
        f_q = customer['frequency_quartile']
        m_q = customer['monetary_quartile']

        if segment == 'Champions':
            explanations.append("• Purchased very recently (top tier recency)")
            explanations.append("• High purchase frequency (top tier loyalty)")
            explanations.append("• High total spending (top tier revenue)")
        elif segment == 'Loyal Customers':
            explanations.append("• High purchase frequency (top tier loyalty)")
            if m_q in ['Q3', 'Q4', '3', '2']:  # High monetary
                explanations.append("• Strong revenue contribution")
            explanations.append("• Regular customer with consistent orders")
        elif segment == 'Recent Customers':
            explanations.append("• Purchased very recently (top tier recency)")
            explanations.append("• Building purchase history")
            explanations.append("• Potential for increased engagement")
        elif segment == 'At Risk':
            explanations.append("• Haven't purchased recently (needs attention)")
            explanations.append("• Risk of customer churn")
            explanations.append("• Recommended: Re-engagement campaign")
        elif segment == 'Need Attention':
            explanations.append("• Moderate engagement levels")
            explanations.append("• Opportunity for improvement")
            explanations.append("• Recommended: Targeted promotions")

        return explanations

    # VISUALIZATION METHODS

    def create_trend_analysis(self, figsize=(15, 10)) -> plt.Figure:
        """
        Create comprehensive trend analysis visualization

        Returns:
            matplotlib.figure.Figure: The generated trend analysis figure

        Note:
            To save the figure, use fig.savefig() or a utility function
        """
        fig, axes = plt.subplots(2, 2, figsize=figsize)
        fig.suptitle('Business Trend Analysis', fontsize=16, fontweight='bold')

        # 1. Revenue Trend
        ax1 = axes[0, 0]
        daily_revenue = self.analyzer.data.groupby(
            pd.Grouper(key=self.analyzer.config['date_col'], freq='D')
        )[self.analyzer.config['revenue_col']].sum()

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
        daily_trans = self.analyzer.data.groupby(
            pd.Grouper(key=self.analyzer.config['date_col'], freq='D')
        )[self.analyzer.config['transaction_col']].nunique()

        ax2.bar(daily_trans.index, daily_trans.values, color='#52B788', alpha=0.7)
        ax2.set_title('Daily Transactions', fontweight='bold')
        ax2.set_xlabel('Date')
        ax2.set_ylabel('Number of Transactions')
        ax2.grid(True, alpha=0.3, axis='y')

        # 3. Product Mix Evolution
        ax3 = axes[1, 0]
        weekly_products = self.analyzer.data.groupby(
            [pd.Grouper(key=self.analyzer.config['date_col'], freq='W'), self.analyzer.config['product_col']]
        )[self.analyzer.config['revenue_col']].sum().reset_index()

        top_products = self.analyzer.product_analysis.head(5).index
        for product in top_products:
            product_data = weekly_products[weekly_products[self.analyzer.config['product_col']] == product]
            if len(product_data) > 0:
                label = self.analyzer.data[self.analyzer.data[self.analyzer.config['product_col']] == product][
                    self.analyzer.config['description_col']
                ].iloc[0][:20] + '...'
                ax3.plot(product_data[self.analyzer.config['date_col']],
                        product_data[self.analyzer.config['revenue_col']],
                        marker='o', label=label, linewidth=2)

        ax3.set_title('Top 5 Products Weekly Performance', fontweight='bold')
        ax3.set_xlabel('Week')
        ax3.set_ylabel('Revenue')
        ax3.legend(fontsize=8)
        ax3.grid(True, alpha=0.3)

        # 4. Day of Week Pattern
        ax4 = axes[1, 1]
        if 'weekday' in self.analyzer.data.columns:
            dow_revenue = self.analyzer.data.groupby('weekday')[self.analyzer.config['revenue_col']].mean()
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

        self.trend_analysis = fig
        return fig
