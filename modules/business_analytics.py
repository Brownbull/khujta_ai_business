"""
Business Analytics Core Module
Core metrics calculations for Business class
"""

import pandas as pd
from typing import Dict
import warnings
warnings.filterwarnings('ignore')

from modules.business import Business


class BusinessAnalyzer(Business):
    """
    Analytics engine that extends Business class.
    Inherits all data, config, and metrics from Business and adds calculation methods.
    """

    def __init__(self, data_source: str = None, config: Dict = None):
        """
        Initialize analyzer by calling parent Business constructor

        Args:
            data_source: Path to data file or DataFrame
            config: Configuration dictionary
        """
        # Initialize parent Business class
        super().__init__(data_source=data_source, config=config)

        # Calculate all base metrics if data is loaded
        if self.data is not None:
            self.calculate_all_metrics()

        print(f"BusinessAnalyzer initialized for project: {self.config['project_name']}")

    # METRIC CALCULATION METHODS
    def calculate_all_metrics(self):
        """Calculate all base metrics"""
        self.calculate_product_metrics()
        self.calculate_inventory_metrics()
        self.calculate_revenue_metrics()
        print("✓ All base metrics calculated")

    def calculate_product_metrics(self):
        """Calculate product-level metrics"""
        if self.data is None:
            return

        self.product_analysis = self.data.groupby(self.config['product_col']).agg({
            self.config['description_col']: 'first', # Use first description
            self.config['revenue_col']: 'sum', # Total revenue
            self.config['quantity_col']: 'sum', # Total quantity sold
            self.config['transaction_col']: 'count' # Number of transactions
        }).sort_values(self.config['revenue_col'], ascending=False)

        # Add cumulative metrics
        self.product_analysis['revenue_cum'] = self.product_analysis[self.config['revenue_col']].cumsum() # Cumulative revenue
        total_revenue = self.product_analysis[self.config['revenue_col']].sum() # Total revenue
        self.product_analysis['revenue_pct_cum'] = 100 * self.product_analysis['revenue_cum'] / total_revenue # Cumulative revenue %

        # Identify top products
        threshold_idx = int(len(self.product_analysis) * self.config['top_products_threshold']) # Index for top products
        self.product_analysis['is_top_product'] = False # Initialize column
        self.product_analysis.iloc[:threshold_idx, self.product_analysis.columns.get_loc('is_top_product')] = True # Set top products to True

    def calculate_inventory_metrics(self):
        """Calculate inventory health metrics"""
        if self.data is None:
            return

        last_sale = self.data.groupby(self.config['product_col']).agg({
            self.config['date_col']: 'max', # Last sale date
            self.config['description_col']: 'first' # Product description
        }).reset_index()

        analysis_date = pd.Timestamp(self.config['analysis_date'])
        last_sale['days_since_sale'] = (analysis_date - last_sale[self.config['date_col']]).dt.days

        # Categorize inventory status
        last_sale['status'] = pd.cut(
            last_sale['days_since_sale'],
            bins=[0, 7, 30, 60, 90, 365, 9999],
            labels=['Hot', 'Active', 'Slowing', 'Cold', 'Dead', 'Zombie']
        )

        self.inventory = last_sale

    def calculate_revenue_metrics(self):
        """Calculate revenue-based metrics"""
        if self.data is None:
            return

        date_range = self.get_date_range()

        self.revenue_metrics = {
            'total_revenue': self.data[self.config['revenue_col']].sum(), # Total revenue
            'total_transactions': self.data[self.config['transaction_col']].nunique(), # Unique transactions
            'avg_transaction_value': self.data.groupby(self.config['transaction_col'])[self.config['revenue_col']].sum().mean(), # Average transaction value
            'total_products': self.data[self.config['product_col']].nunique(), # Unique products sold
            'date_range': date_range # Date range {start, end}
        }

    def calculate_kpis(self) -> Dict:
        """Calculate key performance indicators"""
        if self.revenue_metrics is None:
            print("@calculate_kpis: Revenue metrics not calculated yet.")
            return {}

        date_range = self.revenue_metrics['date_range']

        # Calculate period comparisons
        mid_date = date_range['start'] + (date_range['end'] - date_range['start']) / 2

        current_period = self.data[self.data[self.config['date_col']] >= mid_date]
        previous_period = self.data[self.data[self.config['date_col']] < mid_date]

        current_revenue = current_period[self.config['revenue_col']].sum()
        previous_revenue = previous_period[self.config['revenue_col']].sum()

        growth_rate = ((current_revenue - previous_revenue) / previous_revenue * 100) if previous_revenue > 0 else 0

        self.kpis = {
            'total_revenue': self.revenue_metrics['total_revenue'],
            'total_transactions': self.revenue_metrics['total_transactions'],
            'avg_transaction_value': self.revenue_metrics['avg_transaction_value'],
            'total_products': self.revenue_metrics['total_products'],
            'revenue_growth': growth_rate,
            'current_period_revenue': current_revenue,
            'previous_period_revenue': previous_revenue,
            'mid_date': mid_date
        }

        return self.kpis

    def calculate_alerts(self) -> Dict:
        """Calculate critical business alerts"""
        alerts = {
            'critical': [],
            'warning': [],
            'success': []
        }

        # Check for dead inventory
        if self.inventory is not None:
            dead_stock = self.inventory[
                self.inventory['days_since_sale'] > self.config['dead_stock_days']
            ]
            if len(dead_stock) > 0:
                alerts['critical'].append({
                    'type': 'dead_inventory',
                    'message': f'{len(dead_stock)} products haven\'t sold in {self.config["dead_stock_days"]}+ days',
                    'impact': 'Cash tied up in non-moving inventory',
                    'action': 'Consider liquidation or promotional campaigns'
                })

        # Check revenue concentration
        if self.product_analysis is not None and self.revenue_metrics is not None:
            top_20_pct = int(len(self.product_analysis) * 0.2)
            revenue_concentration = self.product_analysis.iloc[:top_20_pct][self.config['revenue_col']].sum()
            concentration_pct = (revenue_concentration / self.revenue_metrics['total_revenue']) * 100

            if concentration_pct > 80:
                alerts['warning'].append({
                    'type': 'high_concentration',
                    'message': f'Top 20% of products generate {concentration_pct:.1f}% of revenue',
                    'impact': 'High dependency on few products',
                    'action': 'Diversify product portfolio'
                })
            else:
                alerts['success'].append({
                    'type': 'balanced_portfolio',
                    'message': f'Revenue well distributed across products',
                    'impact': 'Lower concentration risk',
                    'action': 'Maintain current portfolio balance'
                })

        # Check for growth
        kpis = self.get_kpis()
        if kpis.get('revenue_growth', 0) > 10:
            alerts['success'].append({
                'type': 'strong_growth',
                'message': f'Revenue growing at {kpis["revenue_growth"]:.1f}%',
                'impact': 'Positive business momentum',
                'action': 'Scale successful initiatives'
            })
        elif kpis.get('revenue_growth', 0) < -10:
            alerts['critical'].append({
                'type': 'revenue_decline',
                'message': f'Revenue declining by {abs(kpis["revenue_growth"]):.1f}%',
                'impact': 'Negative business trend',
                'action': 'Urgent review of sales strategy needed'
            })

        self.alerts = alerts
        return alerts

    def calculate_pareto_insights(self) -> Dict:
        """Calculate 80/20 analysis insights"""
        if self.product_analysis is None:
            return {}

        # Calculate Pareto insights
        twenty_percent = int(len(self.product_analysis) * self.config['top_products_threshold'])
        top_products = self.product_analysis.iloc[:twenty_percent]

        revenue_from_top = top_products[self.config['revenue_col']].sum()
        total_revenue = self.product_analysis[self.config['revenue_col']].sum()
        revenue_pct = (revenue_from_top / total_revenue) * 100

        self.pareto = {
            'top_products_count': twenty_percent,
            'top_products_pct': self.config['top_products_threshold'] * 100,
            'revenue_from_top': revenue_from_top,
            'revenue_from_top_pct': revenue_pct,
            'top_products_list': top_products.head(10).to_dict('records'),
            'concentration_level': 'High' if revenue_pct > 80 else 'Medium' if revenue_pct > 60 else 'Low'
        }

        return self.pareto

    def calculate_inventory_health(self) -> Dict:
        """Calculate inventory health summary"""
        if self.inventory is None:
            return {}

        status_summary = self.inventory['status'].value_counts().to_dict() # Status distribution
        dead_stock = self.inventory[self.inventory['status'].isin(['Dead', 'Zombie'])] # Dead stock count

        inventory_health = {
            'status_distribution': status_summary,
            'dead_stock_count': len(dead_stock),
            'dead_stock_products': dead_stock.to_dict('records'),
            'healthy_stock_pct': (status_summary.get('Hot', 0) + status_summary.get('Active', 0)) / len(self.inventory) * 100,
            'at_risk_products': self.inventory[self.inventory['status'] == 'Slowing'].to_dict('records')[:5]
        }

        return inventory_health

    def calculate_peak_times(self) -> Dict:
        """Calculate peak business times"""
        if self.data is None or 'hour' not in self.data.columns:
            return {}

        # Revenue by hour
        hourly_revenue = self.data.groupby('hour')[self.config['revenue_col']].sum()
        peak_hour = hourly_revenue.idxmax()

        # Revenue by weekday
        if 'weekday' in self.data.columns:
            daily_revenue = self.data.groupby('weekday')[self.config['revenue_col']].sum()
            peak_day = daily_revenue.idxmax()
            valley_day = daily_revenue.idxmin()
        else:
            peak_day = valley_day = 'N/A'

        peak_times = {
            'peak_hour': peak_hour,
            'peak_day': peak_day,
            'valley_day': valley_day,
            'hourly_distribution': hourly_revenue.to_dict(),
            'recommendation': f'Optimize staffing for {peak_day}s around {peak_hour}:00'
        }

        return peak_times

    # PUBLIC GET METHODS (with lazy calculation)
    def get_kpis(self, show: bool = False) -> Dict:
        """Get KPIs (calculate if not yet calculated)"""
        if self.kpis is None:
            self.calculate_kpis()

        if show:
            print(self.print_kpis())

        return self.kpis

    def get_alerts(self, show: bool = False) -> Dict:
        """Get alerts (calculate if not yet calculated)"""
        if self.alerts is None:
            self.calculate_alerts()

        if show:
            print(self.print_alerts())

        return self.alerts

    def get_pareto_insights(self) -> Dict:
        """Get pareto insights (calculate if not yet calculated)"""
        if self.pareto is None:
            self.calculate_pareto_insights()
        return self.pareto

    def get_inventory_health(self) -> Dict:
        """Get inventory health summary (calculate if not yet calculated)"""
        inventory_health = self.calculate_inventory_health()
        return inventory_health

    def get_peak_times(self) -> Dict:
        """Get peak business times (calculate if not yet calculated)"""
        peak_times = self.calculate_peak_times()
        return peak_times

    # PRINT/FORMAT METHODS
    def print_kpis(self) -> str:
        """Format KPIs as string"""
        if self.kpis is None:
            self.calculate_kpis()

        kpis = self.kpis
        mid_date = kpis['mid_date']
        date_range = self.revenue_metrics['date_range']

        prev_start_str = pd.to_datetime(date_range['start']).strftime('%Y-%m-%d')
        prev_end_str = pd.to_datetime(mid_date).strftime('%Y-%m-%d')
        curr_start_str = pd.to_datetime(mid_date).strftime('%Y-%m-%d')
        curr_end_str = pd.to_datetime(date_range['end']).strftime('%Y-%m-%d')

        kpi_str = []
        kpi_str.append(f"\n📅 Periods considered for growth:")
        kpi_str.append(f"  • Previous: {prev_start_str} -> {prev_end_str}")
        kpi_str.append(f"  • Current:  {curr_start_str} -> {curr_end_str}")
        kpi_str.append(f"📈 Growth: {kpis['revenue_growth']:.1f}%")
        kpi_str.append(f"\n💰 Revenue: {self.format_currency(kpis['total_revenue'])}")
        kpi_str.append(f"🛒 Transactions: {kpis['total_transactions']:,}")

        return "\n".join(kpi_str)

    def print_alerts(self) -> str:
        """Format alerts as string"""
        if self.alerts is None:
            self.calculate_alerts()

        alerts = self.alerts
        alerts_str = []

        if alerts['critical']:
            alerts_str.append("🔴 CRITICAL ACTIONS REQUIRED:")
            for alert in alerts['critical']:
                alerts_str.append(f"\n  {alert['message']}")
                alerts_str.append(f"  Impact: {alert['impact']}")
                alerts_str.append(f"  ➔ Action: {alert['action']}")

        if alerts['warning']:
            alerts_str.append("\n🟡 WARNINGS:")
            for alert in alerts['warning']:
                alerts_str.append(f"\n  {alert['message']}")
                alerts_str.append(f"  ➔ Action: {alert['action']}")

        if alerts['success']:
            alerts_str.append("\n🟢 SUCCESS INDICATORS:")
            for alert in alerts['success']:
                alerts_str.append(f"\n  {alert['message']}")
                alerts_str.append(f"  ➔ Next Step: {alert['action']}")

        return "\n".join(alerts_str)

    def print_pareto(self, top_products_count: int = 5) -> str:
        """Format pareto insights as string"""
        if self.pareto is None:
            self.calculate_pareto_insights()

        pareto = self.pareto
        pareto_str = []
        pareto_str.append(f"🎯 TOP INSIGHT: Your top {pareto['top_products_count']} products "
            f"({pareto['top_products_pct']:.0f}% of catalog) generate "
            f"{pareto['revenue_from_top_pct']:.1f}% of revenue!")

        pareto_str.append(f"\nConcentration Risk Level: {pareto['concentration_level']}")

        pareto_str.append(f"\n📋 Top {top_products_count} Revenue Generators:")
        for i, product in enumerate(pareto['top_products_list'][:top_products_count], 1):
            pareto_str.append(f"  {i}. {product[self.config['description_col']]}: {self.format_currency(product[self.config['revenue_col']])}")

        pareto_str.append(f"\n📊 80/20 Rule: Top {pareto['top_products_pct']:.0f}% = {pareto['revenue_from_top_pct']:.1f}% of revenue")

        return "\n".join(pareto_str)

    def print_inventory_health(self) -> str:
        """Format inventory health as string"""
        inventory_health = self.calculate_inventory_health()

        if not inventory_health:
            return "No inventory data available"

        inv_health_str = []
        inv_health_str.append(f"📊 Inventory Health Score: {inventory_health['healthy_stock_pct']:.0f}%")
        inv_health_str.append(f"\n⚠️ Dead Stock Alert: {inventory_health['dead_stock_count']} products")

        if inventory_health['at_risk_products']:
            inv_health_str.append("\n🟡 Products At Risk (Slowing):")
            for product in inventory_health['at_risk_products'][:3]:
                inv_health_str.append(f"  • {product[self.config['description_col']]}: {product['days_since_sale']} days since last sale")
        
        if inventory_health['dead_stock_count'] > 0:
            inv_health_str.append("\n🔴 Dead Stock Examples:")
            for product in inventory_health['dead_stock_products'][:3]:
                inv_health_str.append(f"  • {product[self.config['description_col']]}: {product['days_since_sale']} days since last sale")
        
        return "\n".join(inv_health_str)

    def print_peak_times(self) -> str:
        """Format peak times as string"""
        peak_times = self.calculate_peak_times()

        if not peak_times:
            return "No timing data available"

        peaks_str = []
        peaks_str.append(f"⏰ Peak Performance Windows:")
        peaks_str.append(f"  • Best Day: {peak_times['peak_day']}s")
        peaks_str.append(f"  • Peak Hour: {peak_times['peak_hour']}:00")
        peaks_str.append(f"  • Slowest Day: {peak_times['valley_day']}s")
        peaks_str.append(f"\n💡 {peak_times['recommendation']}")

        return "\n".join(peaks_str)

    # SUMMARY METHODS
    def get_executive_summary_dict(self) -> Dict:
        """Get executive summary as dictionary (for CSV export)"""
        return {
            'Date': self.config['analysis_date'],
            'Total Revenue': self.get_kpis().get('total_revenue', 0),
            'Revenue Growth %': self.get_kpis().get('revenue_growth', 0),
            'Total Transactions': self.get_kpis().get('total_transactions', 0),
            'Top 20% Revenue Share': self.get_pareto_insights().get('revenue_from_top_pct', 0),
            'Dead Stock Count': self.get_inventory_health().get('dead_stock_count', 0),
            'Inventory Health %': self.get_inventory_health().get('healthy_stock_pct', 0)
        }
