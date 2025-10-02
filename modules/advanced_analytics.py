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

from modules.translations import get_text, translate_segment_name, translate_day_name
from modules.business_analytics import BusinessAnalyzer
from modules.logger import get_logger

# Initialize logger for this module
logger = get_logger(__name__)


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
        logger.info(f"AdvancedAnalytics initialized for project: {self.analyzer.config['project_name']}")

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
        logger.debug("Starting RFM customer segmentation analysis")

        if self.analyzer.data is None or self.analyzer.config['customer_col'] not in self.analyzer.data.columns:
            logger.warning("No customer column available, using transaction pattern segmentation")
            return self._segment_by_transaction_patterns()

        # Standard RFM if customer data exists
        analysis_date = pd.Timestamp(self.analyzer.config['analysis_date'])
        logger.debug(f"Analysis date: {analysis_date}")

        rfm = self.analyzer.data.groupby(self.analyzer.config['customer_col']).agg({
            self.analyzer.config['date_col']: lambda x: (analysis_date - x.max()).days, # Recency
            self.analyzer.config['transaction_col']: 'nunique', # Frequency
            self.analyzer.config['revenue_col']: 'sum' # Monetary
        })

        rfm.columns = ['Recency', 'Frequency', 'Monetary']
        logger.debug(f"RFM data shape: {rfm.shape}")
        logger.debug(f"Recency range: {rfm['Recency'].min():.0f} to {rfm['Recency'].max():.0f} days")
        logger.debug(f"Frequency range: {rfm['Frequency'].min():.0f} to {rfm['Frequency'].max():.0f} transactions")
        logger.debug(f"Monetary range: {rfm['Monetary'].min():.0f} to {rfm['Monetary'].max():.0f}")

        # Create segments using quartiles (or fewer if data has duplicates)
        # Note: For Recency, lower days = better, so we invert the labels
        for col in ['Recency', 'Frequency', 'Monetary']:
            try:
                # Try to create quartiles with S1-S4 labels (Segment notation)
                if col == 'Recency':
                    # Invert labels for Recency: lower days = higher segment (S4 is best)
                    rfm[f'{col}_Quartile'] = pd.qcut(rfm[col], 4, labels=['S4', 'S3', 'S2', 'S1'])
                else:
                    rfm[f'{col}_Quartile'] = pd.qcut(rfm[col], 4, labels=['S1', 'S2', 'S3', 'S4'])
                logger.debug(f"{col} quartiles created with labels successfully")
            except ValueError as e:
                # If quartiles fail due to duplicates, use duplicates='drop' without labels
                logger.warning(f"{col} quartile creation failed (duplicates), using duplicates='drop': {e}")
                rfm[f'{col}_Quartile'] = pd.qcut(rfm[col], 4, duplicates='drop')
                # For intervals, we'll handle the inversion in the display logic

        # Define customer segments using all 3 RFM dimensions
        # Priority hierarchy: Monetary > Frequency > Recency
        # Calculate quartile boundaries once (not per row for performance)
        r_max = rfm['Recency_Quartile'].max()  # Best recency (lowest days)
        f_max = rfm['Frequency_Quartile'].max()  # Best frequency (highest transactions)
        m_max = rfm['Monetary_Quartile'].max()  # Best monetary (highest spending)
        r_min = rfm['Recency_Quartile'].min()  # Worst recency (highest days)
        logger.debug(f"Best recency (lowest days):{r_max}")
        logger.debug(f"Best frequency (highest transactions):{f_max}")
        logger.debug(f"Best monetary (highest spending):{m_max}")
        logger.debug(f"Worst recency (highest days):{r_min}")


        # Calculate median for monetary VALUE (not quartile) to identify decent spenders
        m_median_value = rfm['Monetary'].median()

        logger.debug(f"Segmentation boundaries: R_max={r_max}, F_max={f_max}, M_max={m_max}, R_min={r_min}, M_median_value={m_median_value}")

        def segment_customers(row):
            r = row['Recency_Quartile']
            f = row['Frequency_Quartile']
            m = row['Monetary_Quartile']
            m_value = row['Monetary']  # Actual monetary value for median comparison

            # 1. Champions: Best in all 3 dimensions
            if m == m_max and f == f_max and r == r_max:
                return 'Champions'

            # 2. High Value Customers: High spenders who are either frequent OR recent (but not both)
            elif m == m_max and (f == f_max or r == r_max):
                return 'High Value Customers'

            # 3. Loyal Customers: Frequent buyers (but not high spenders)
            elif f == f_max:
                return 'Loyal Customers'

            # 4. Recent High Spenders: Recent + decent spending (but not champions/high value/loyal)
            elif r == r_max and m_value >= m_median_value:
                return 'Recent High Spenders'

            # 5. At Risk - High Value: High spenders who haven't purchased recently
            elif m == m_max and r == r_min:
                return 'At Risk - High Value'

            # 6. At Risk: Haven't purchased recently (not high spenders)
            elif r == r_min:
                return 'At Risk'

            # 7. Need Attention: Everyone else (moderate on all dimensions)
            else:
                return 'Need Attention'

        logger.debug("Applying segmentation logic to all customers...")
        rfm['Segment'] = rfm.apply(segment_customers, axis=1)  # Apply segmentation

        # Log segment distribution with details
        segment_counts = rfm['Segment'].value_counts().to_dict()
        logger.debug(f"Segment distribution: {segment_counts}")

        # Log summary statistics per segment
        for segment in ['Champions', 'High Value Customers', 'Loyal Customers', 'Recent High Spenders', 'At Risk - High Value', 'At Risk', 'Need Attention']:
            if segment in segment_counts:
                seg_data = rfm[rfm['Segment'] == segment]
                logger.debug(f"{segment}: {segment_counts[segment]} customers, "
                           f"Avg Monetary: {seg_data['Monetary'].mean():.0f}, "
                           f"Avg Frequency: {seg_data['Frequency'].mean():.1f}, "
                           f"Avg Recency: {seg_data['Recency'].mean():.1f} days")

        logger.info(f"RFM segmentation completed: {len(rfm)} customers across {len(segment_counts)} segments")

        # Store RFM data for detailed reports
        self.rfm_data = rfm.copy()

        return {
            'segments': segment_counts,
            'segment_revenue': rfm.groupby('Segment')['Monetary'].sum().to_dict(),
            'total_customers': len(rfm),
            'avg_recency': rfm['Recency'].mean(),
            'avg_frequency': rfm['Frequency'].mean(),
            'avg_monetary': rfm['Monetary'].mean()
        }

    def _segment_by_transaction_patterns(self) -> Dict:
        """Segment based on transaction patterns when no customer data"""
        trans_analysis = self.analyzer.data.groupby(self.analyzer.config['transaction_col']).agg({
            self.analyzer.config['revenue_col']: 'sum', # Total revenue per transaction
            self.analyzer.config['product_col']: 'count', # Number of items per transaction
            self.analyzer.config['date_col']: 'first' # First transaction date
        })

        # Categorize transactions
        trans_analysis['size_category'] = pd.cut(
            trans_analysis[self.analyzer.config['revenue_col']], # Transaction size
            bins=[0, trans_analysis[self.analyzer.config['revenue_col']].quantile(0.33), # 33% of transactions
                  trans_analysis[self.analyzer.config['revenue_col']].quantile(0.67), # 67% of transactions
                  trans_analysis[self.analyzer.config['revenue_col']].max()], # Max value
            labels=['Small', 'Medium', 'Large']
        )

        return {
            'transaction_segments': trans_analysis['size_category'].value_counts().to_dict(), # Count per size category
            'avg_transaction_size': trans_analysis[self.analyzer.config['revenue_col']].mean(), # Average transaction size
            'avg_items_per_transaction': trans_analysis[self.analyzer.config['product_col']].mean() # Average items per transaction
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

        lang = self.analyzer.config.get('language', 'ENG')
        recommendations = []

        # Get insights
        pareto = self.analyzer.get_pareto_insights()
        inventory = self.analyzer.get_inventory_health()
        forecast = self.calculate_revenue_forecast()
        cross_sell = self.calculate_cross_sell_opportunities()

        # Revenue concentration recommendation
        if pareto['revenue_from_top_pct'] > 80:
            recommendations.append({
                'priority': get_text('priority_high', lang),
                'category': 'Risk Management',
                'title': get_text('rec_promote_top_title', lang),
                'description': get_text('rec_promote_top_desc', lang),
                'action': get_text('rec_promote_top_action', lang),
                'expected_impact': get_text('rec_promote_top_impact', lang),
                'timeframe': '3 months'
            })

        # Inventory optimization
        if inventory['dead_stock_count'] > 5:
            recommendations.append({
                'priority': get_text('priority_high', lang),
                'category': 'Cash Flow',
                'title': get_text('rec_clear_dead_stock_title', lang),
                'description': get_text('rec_clear_dead_stock_desc', lang, count=inventory['dead_stock_count']),
                'action': get_text('rec_clear_dead_stock_action', lang),
                'expected_impact': get_text('rec_clear_dead_stock_impact', lang),
                'timeframe': get_text('timeline_1_2_weeks', lang)
            })

        # Cross-selling opportunities
        if cross_sell:
            top_bundle = cross_sell[0]
            bundle_title = 'Implement Product Bundling' if lang == 'ENG' else 'Implementar Paquetes de Productos'
            bundle_desc = f"Products frequently bought together: {top_bundle['product_1'][:30]} & {top_bundle['product_2'][:30]}" if lang == 'ENG' else f"Productos comprados juntos frecuentemente: {top_bundle['product_1'][:30]} & {top_bundle['product_2'][:30]}"
            bundle_action = 'Create bundle offers with 5-10% discount' if lang == 'ENG' else 'Crear ofertas de paquetes con 5-10% descuento'
            bundle_impact = 'Increase average transaction value by 15%' if lang == 'ENG' else 'Aumentar valor promedio de transacción en 15%'
            bundle_timeframe = '1 month' if lang == 'ENG' else '1 mes'

            recommendations.append({
                'priority': get_text('priority_medium', lang),
                'category': 'Revenue Growth',
                'title': bundle_title,
                'description': bundle_desc,
                'action': bundle_action,
                'expected_impact': bundle_impact,
                'timeframe': bundle_timeframe
            })

        # Trend-based recommendation
        if forecast.get('trend') == 'decreasing':
            recommendations.append({
                'priority': get_text('priority_high', lang),
                'category': 'Revenue Protection',
                'title': get_text('rec_address_decline_title', lang),
                'description': get_text('rec_address_decline_desc', lang),
                'action': get_text('rec_address_decline_action', lang),
                'expected_impact': get_text('rec_address_decline_impact', lang),
                'timeframe': get_text('timeline_immediate', lang)
            })

        return sorted(recommendations, key=lambda x: 0 if x['priority'] in ['HIGH', 'ALTA'] else 1 if x['priority'] in ['MEDIUM', 'MEDIA'] else 2)

    # PRINT/FORMAT METHODS

    def print_revenue_forecast(self, days_ahead: int = 30) -> str:
        """Format revenue forecast as string"""

        lang = self.analyzer.config.get('language', 'ENG')
        forecast = self.calculate_revenue_forecast(days_ahead)

        if not forecast:
            return "No forecast data available"

        # Translate trend
        trend_key = forecast['trend'].lower()
        trend_translated = get_text(trend_key, lang)

        forecast_str = []
        forecast_str.append(f"📈 {get_text('revenue_forecast', lang, days=days_ahead)}")
        forecast_str.append(f" {get_text('daily', lang)}")
        forecast_str.append(f" - {get_text('average', lang)}: {self.analyzer.format_currency(forecast['forecast_daily_avg'])}")
        forecast_str.append(f" - {get_text('std_dev', lang)}: {self.analyzer.format_currency(forecast['daily_std_dev'])}")
        forecast_str.append(f" - 95% {get_text('confidence_interval', lang)}: ({self.analyzer.format_currency(forecast['confidence_interval_daily'][0])}, {self.analyzer.format_currency(forecast['confidence_interval_daily'][1])})")
        forecast_str.append(f" {get_text('total', lang)}")
        forecast_str.append(f" - {get_text('forecast', lang)}: {self.analyzer.format_currency(forecast['forecast_total'])}")
        forecast_str.append(f" - 95% {get_text('confidence_interval', lang)}: ({self.analyzer.format_currency(forecast['confidence_interval_total'][0])}, {self.analyzer.format_currency(forecast['confidence_interval_total'][1])})")
        forecast_str.append(f" - {get_text('trend', lang)}: {trend_translated.capitalize()}")

        return "\n".join(forecast_str)

    def print_cross_sell_opportunities(self, min_support: float = 0.01, limit: int = 3) -> str:
        """Format cross-sell opportunities as string"""

        lang = self.analyzer.config.get('language', 'ENG')
        opportunities = self.calculate_cross_sell_opportunities(min_support, limit)

        if not opportunities:
            return f"ℹ️ {get_text('no_cross_sell', lang)}"

        xsell_str = []
        xsell_str.append(f"🛍️ {get_text('cross_sell_opportunities', lang)}")
        for opp in opportunities:
            xsell_str.append(f"  • {opp['product_1'][:30]} & {opp['product_2'][:30]}")
            freq_label = "Frequency" if lang == 'ENG' else "Frecuencia"
            support_label = "Support" if lang == 'ENG' else "Soporte"
            xsell_str.append(f"    {freq_label}: {opp['frequency']} | {support_label}: {opp['support']:.2f}%")
            xsell_str.append(f"    → {opp['recommendation']}")

        return "\n".join(xsell_str)

    def print_anomalies(self, limit: int = 3) -> str:
        """Format anomalies as string"""

        lang = self.analyzer.config.get('language', 'ENG')
        anomalies = self.calculate_anomalies(limit)

        if not anomalies:
            return f"ℹ️ {get_text('no_anomalies', lang)}"

        anomalies_str = []
        anomalies_str.append(f"⚠️ {get_text('anomalies_detected', lang)}")
        for anomaly in anomalies:
            anomalies_str.append(f"  • {anomaly['description']}")

        return "\n".join(anomalies_str)

    def print_recommendations(self) -> str:
        """Format recommendations as string"""

        lang = self.analyzer.config.get('language', 'ENG')
        recommendations = self.calculate_recommendations()

        if not recommendations:
            return f"ℹ️ {get_text('no_recommendations', lang)}"

        recmm_str = []
        recmm_str.append(f"\n💡 {get_text('top_recommendations', lang)}")
        for i, rec in enumerate(recommendations[:3], 1):
            recmm_str.append(f"\n{i}. [{rec['priority']}] {rec['title']}")
            recmm_str.append(f"   {rec['description']}")
            recmm_str.append(f"   {get_text('action', lang)}: {rec['action']}")
            recmm_str.append(f"   {get_text('expected_impact', lang)}: {rec['expected_impact']} | {get_text('timeline', lang)}: {rec['timeframe']}")

        return "\n".join(recmm_str)

    def print_customer_segmentation(self) -> str:
        """Format customer segmentation as string"""

        lang = self.analyzer.config.get('language', 'ENG')
        rfm_segmentation = self.calculate_customer_segmentation_rfm()
        
        logger.info(f"rfm_segmentation: {rfm_segmentation}")

        # Format output
        rfm_str = []
        rfm_str.append(f"👥 {get_text('customer_segmentation', lang)}\n")
        if 'segments' in rfm_segmentation:
            rfm_str.append(get_text('customer_segments', lang))
            for segment, count in rfm_segmentation['segments'].items():
                segment_translated = translate_segment_name(segment, lang)
                customers_label = get_text('customers', lang)
                rfm_str.append(f"  • {segment_translated}: {count} {customers_label}")

            days_label = get_text('days', lang)
            transactions_label = get_text('transactions', lang)

            rfm_str.append(f"\n{get_text('total_customers', lang)}: {rfm_segmentation['total_customers']}")
            rfm_str.append(f"{get_text('avg_recency', lang)}: {rfm_segmentation['avg_recency']:.1f} {days_label}")
            rfm_str.append(f"{get_text('avg_frequency', lang)}: {rfm_segmentation['avg_frequency']:.1f} {transactions_label}")
            rfm_str.append(f"{get_text('avg_monetary', lang)}: {self.analyzer.format_currency(rfm_segmentation['avg_monetary'])}")
        else:
            rfm_str.append(f"{get_text('transaction_segments', lang)}")
            for segment, count in rfm_segmentation['transaction_segments'].items():
                transactions_label = get_text('transactions', lang)
                rfm_str.append(f"  • {segment}: {count} {transactions_label}")
            rfm_str.append(f"\n{get_text('avg_transaction_size', lang)}: {self.analyzer.format_currency(rfm_segmentation['avg_transaction_size'])}")
            rfm_str.append(f"{get_text('avg_items_per_transaction', lang)}: {rfm_segmentation['avg_items_per_transaction']:.1f}")

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
            segment_customers = self.rfm_data[self.rfm_data['Segment'] == segment].copy() # Copy to avoid modifying original data

            # Sort by composite RFM score (Recency ascending=best is lowest days, Frequency & Monetary descending)
            # Priority: Recency first (most recent), then Frequency, then Monetary
            segment_customers = segment_customers.sort_values(
                by=['Recency', 'Frequency', 'Monetary'],
                ascending=[True, False, False]
            )

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

        lang = self.analyzer.config.get('language', 'ENG')
        detailed_segments = self.calculate_detailed_customer_segments(top_n=top_n)

        if 'error' in detailed_segments:
            return f"ℹ️ {detailed_segments['error']}"

        # Segment emoji mapping
        segment_emojis = {
            'Champions': '🏆',
            'High Value Customers': '💎',
            'Loyal Customers': '🔵',
            'Recent High Spenders': '🟢',
            'At Risk - High Value': '🟠',
            'At Risk': '🔴',
            'Need Attention': '🟡'
        }

        # Segment order for display (priority: best to worst)
        segment_order = ['Champions', 'High Value Customers', 'Loyal Customers', 'Recent High Spenders', 'Need Attention', 'At Risk - High Value', 'At Risk']

        output = []
        output.append("=" * 60)
        output.append(get_text('detailed_segmentation_report', lang))
        output.append("=" * 60)
        output.append("")

        # Add RFM explanation section
        output.append("┌" + "─" * 58 + "┐")
        output.append("│ " + get_text('rfm_explanation_title', lang).ljust(57) + "│")
        output.append("├" + "─" * 58 + "┤")
        output.append(f"│ • {get_text('rfm_r_label', lang)}: {get_text('rfm_r_desc', lang)}".ljust(59) + "│")
        output.append(f"│ • {get_text('rfm_f_label', lang)}: {get_text('rfm_f_desc', lang)}".ljust(59) + "│")
        output.append(f"│ • {get_text('rfm_m_label', lang)}: {get_text('rfm_m_desc', lang)}".ljust(59) + "│")
        output.append("│" + " " * 58 + "│")
        output.append(f"│ ℹ️  {get_text('rfm_quartile_note', lang)}".ljust(59) + "│")
        output.append("└" + "─" * 58 + "┘")
        output.append("")

        # Process segments in order
        for segment in segment_order:
            if segment not in detailed_segments:
                continue

            segment_data = detailed_segments[segment]
            emoji = segment_emojis.get(segment, '📊')
            segment_translated = translate_segment_name(segment, lang)
            customers_label = get_text('customers', lang)

            output.append(f"\n{emoji} {segment_translated.upper()} ({segment_data['total_count']} {customers_label})")
            output.append("━" * 60)

            for i, customer in enumerate(segment_data['top_customers'], 1):
                # Build customer header line
                customer_line = f"\n#{i}: {customer['customer_id']}"
                if 'name' in customer:
                    customer_line += f" - {customer['name']}"
                if 'location' in customer:
                    customer_line += f" ({customer['location']})"
                output.append(customer_line)

                # Get labels
                recency_days = int(customer['recency'])
                day_label = get_text('day' if recency_days == 1 else 'days', lang)
                freq_count = int(customer['frequency'])
                purchase_label = get_text('purchase' if freq_count == 1 else 'purchases', lang)

                output.append(f"    💰 {get_text('total_revenue', lang)}: {self.analyzer.format_currency(customer['monetary'])}")
                output.append(f"    📅 {get_text('last_purchase', lang)}: {recency_days} {day_label} {get_text('ago', lang)}")
                output.append(f"    🔄 {get_text('transactions', lang).capitalize()}: {freq_count} {purchase_label}")
                output.append("")

                # Format RFM score - use actual days for R if it's an interval, otherwise use segment notation
                r_display = customer['recency_quartile']
                if isinstance(r_display, (float, int)) or (isinstance(r_display, str) and ',' in str(r_display)):
                    # It's an interval or numeric, show actual days value
                    r_display = f"{recency_days}d"

                output.append(f"    📊 {get_text('rfm_score', lang)}: R[{r_display}] F[{customer['frequency_quartile']}] M[{customer['monetary_quartile']}]")
                output.append("")

                # Generate explanation
                explanation = self._generate_segment_explanation(segment, customer, lang)
                output.append(f"    ✨ {get_text('why_segment', lang, segment=segment_translated)}?")
                for line in explanation:
                    output.append(f"    {line}")

                if i < len(segment_data['top_customers']):
                    output.append("")

            output.append("\n" + "━" * 60)

        return '\n'.join(output)

    def _generate_segment_explanation(self, segment: str, customer: Dict, lang: str = 'ENG') -> list:
        """Generate business-friendly explanation for why customer is in segment"""

        explanations = []

        r_q = customer['recency_quartile']
        f_q = customer['frequency_quartile']
        m_q = customer['monetary_quartile']

        if segment == 'Champions':
            explanations.append(f"• {get_text('exp_high_spending', lang)}")
            explanations.append(f"• {get_text('exp_high_frequency', lang)}")
            explanations.append(f"• {get_text('exp_purchased_recently', lang)}")
            explanations.append(f"• {get_text('exp_strong_revenue', lang)}")
        elif segment == 'High Value Customers':
            explanations.append(f"• {get_text('exp_high_spending', lang)}")
            if f_q in ['S4', 'Q4', '4']:
                explanations.append(f"• {get_text('exp_high_frequency', lang)}")
            if r_q in ['S4', 'Q4', '4']:
                explanations.append(f"• {get_text('exp_purchased_recently', lang)}")
            explanations.append(f"• {get_text('exp_strong_revenue', lang)}")
        elif segment == 'Loyal Customers':
            explanations.append(f"• {get_text('exp_high_frequency', lang)}")
            explanations.append(f"• {get_text('exp_regular_customer', lang)}")
            if m_q in ['S3', 'S4', 'Q3', 'Q4', '3', '2']:  # High monetary
                explanations.append(f"• {get_text('exp_strong_revenue', lang)}")
        elif segment == 'Recent High Spenders':
            explanations.append(f"• {get_text('exp_purchased_recently', lang)}")
            explanations.append(f"• {get_text('exp_strong_revenue', lang)}")
            explanations.append(f"• {get_text('exp_potential_engagement', lang)}")
        elif segment == 'At Risk - High Value':
            explanations.append(f"• {get_text('exp_high_spending', lang)} (historically)")
            explanations.append(f"• {get_text('exp_not_purchased', lang)}")
            explanations.append(f"• {get_text('exp_churn_risk', lang)} - HIGH PRIORITY")
            explanations.append(f"• {get_text('exp_reengagement', lang)}")
        elif segment == 'At Risk':
            explanations.append(f"• {get_text('exp_not_purchased', lang)}")
            explanations.append(f"• {get_text('exp_churn_risk', lang)}")
            explanations.append(f"• {get_text('exp_reengagement', lang)}")
        elif segment == 'Need Attention':
            explanations.append(f"• {get_text('exp_moderate_engagement', lang)}")
            explanations.append(f"• {get_text('exp_opportunity', lang)}")
            explanations.append(f"• {get_text('exp_targeted_promo', lang)}")

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

        lang = self.analyzer.config.get('language', 'ENG')

        fig, axes = plt.subplots(2, 2, figsize=figsize)
        fig.suptitle(get_text('trend_analysis_title', lang), fontsize=16, fontweight='bold')

        # 1. Revenue Trend
        ax1 = axes[0, 0]
        daily_revenue = self.analyzer.data.groupby(
            pd.Grouper(key=self.analyzer.config['date_col'], freq='D')
        )[self.analyzer.config['revenue_col']].sum()

        ax1.plot(daily_revenue.index, daily_revenue.values, color='#2E86AB', linewidth=1, alpha=0.5)
        ax1.plot(daily_revenue.index, daily_revenue.rolling(7).mean(), color='#D62828', linewidth=2, label=get_text('moving_average_7d', lang))
        ax1.fill_between(daily_revenue.index, 0, daily_revenue.values, alpha=0.3, color='#2E86AB')
        ax1.set_title(get_text('revenue_trend', lang), fontweight='bold')
        ax1.set_xlabel(get_text('date_label', lang))
        ax1.set_ylabel(get_text('revenue_label', lang))
        ax1.legend()
        ax1.grid(True, alpha=0.3)

        # 2. Transaction Volume
        ax2 = axes[0, 1]
        daily_trans = self.analyzer.data.groupby(
            pd.Grouper(key=self.analyzer.config['date_col'], freq='D')
        )[self.analyzer.config['transaction_col']].nunique()

        ax2.bar(daily_trans.index, daily_trans.values, color='#52B788', alpha=0.7)
        ax2.set_title(get_text('daily_transactions_title', lang), fontweight='bold')
        ax2.set_xlabel(get_text('date_label', lang))
        ax2.set_ylabel(get_text('num_transactions', lang))
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

        ax3.set_title(get_text('top_products_weekly', lang), fontweight='bold')
        ax3.set_xlabel(get_text('week_label', lang))
        ax3.set_ylabel(get_text('revenue_label', lang))
        ax3.legend(fontsize=8)
        ax3.grid(True, alpha=0.3)

        # 4. Day of Week Pattern
        ax4 = axes[1, 1]
        if 'weekday' in self.analyzer.data.columns:
            dow_revenue = self.analyzer.data.groupby('weekday')[self.analyzer.config['revenue_col']].mean()
            day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
            dow_revenue = dow_revenue.reindex(day_order, fill_value=0)

            # Translate day names for display
            day_labels = [translate_day_name(day, lang) for day in day_order]

            colors = ['#D62828' if day in ['Saturday', 'Sunday'] else '#2E86AB' for day in day_order]
            bars = ax4.bar(range(7), dow_revenue.values, color=colors, alpha=0.8)
            ax4.set_xticks(range(7))
            ax4.set_xticklabels([d[:3] for d in day_labels])
            ax4.set_title(get_text('avg_revenue_by_dow', lang), fontweight='bold')
            ax4.set_ylabel(get_text('revenue_label', lang))
            ax4.grid(True, alpha=0.3, axis='y')

        plt.tight_layout()

        self.trend_analysis = fig
        return fig
