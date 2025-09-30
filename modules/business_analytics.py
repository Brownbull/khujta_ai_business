"""
Business Analytics Core Module
Main analytics engine for executive dashboards
"""

from matplotlib.pylab import pareto
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import warnings
import os
warnings.filterwarnings('ignore')

class BusinessAnalyzer:
    """Main orchestrator for business analytics"""
    
    def __init__(self, data_source: str = None, config: Dict = None, out_dir: str = None):
        """Initialize the analyzer with data and configuration"""
        self.config = config or self._default_config()
        self.data = None
        self.product_analysis = None
        self.inventory_status = None
        self.revenue_metrics = None
        self.pareto = None
        self.out_dir = out_dir or self._set_out_dir()
        
        # Initialize run timestamp strings for unique file names
        now = datetime.now()
        self.run_dt = now.strftime('%Y%m%d') # YYYYMMDD, e.g. '20250927'
        self.run_time = now.strftime('%H%M') # HHMM, e.g. '1435'

        if data_source:
            self.load_data(data_source)
    
    def _default_config(self) -> Dict:
        """Default configuration settings"""
        return {
            'project_name': 'Buenacarne',
            'analysis_date': datetime.now(),
            'top_products_threshold': 0.2,
            'dead_stock_days': 30,
            'currency_format': 'CLP',
            'language': 'EN',
            'date_col': 'fecha',
            'product_col': 'producto',
            'description_col': 'glosa',
            'revenue_col': 'total',
            'quantity_col': 'cantidad',
            'transaction_col': 'trans_id',
            'cost_col': 'costo',
            'out_dir' : 'outputs' 
        }
        
    def _set_out_dir(self) -> str:
        # Get save path if not defined
        output_dir = os.path.join(self.config['out_dir'], self.config['project_name'], f"{self.run_dt}_{self.run_time}")
        if not os.path.exists(output_dir):
            print(f"📂 Creating output directory: {output_dir}")
            os.makedirs(output_dir, exist_ok=True)
        self.config['out_dir'] = output_dir
    
    def load_data(self, data_source: str):
        """Load and prepare data"""
        if data_source.endswith('.csv'):
            self.data = pd.read_csv(data_source)
        elif data_source.endswith(('.xlsx', '.xls')):
            self.data = pd.read_excel(data_source)
        else:
            self.data = data_source  # Assume it's already a DataFrame
        
        self._prepare_data()
        self._calculate_metrics()
    
    def _prepare_data(self):
        """Prepare data for analysis"""
        # Convert date column
        if self.config['date_col'] in self.data.columns:
            self.data[self.config['date_col']] = pd.to_datetime(
                self.data[self.config['date_col']], 
                errors='coerce'
            )
        
        # Add time-based columns if they don't exist
        if 'hour' not in self.data.columns and 'inith' in self.data.columns:
            self.data['hour'] = self.data['inith']
        
        if 'weekday' not in self.data.columns and self.config['date_col'] in self.data.columns:
            self.data['weekday'] = self.data[self.config['date_col']].dt.day_name()
            self.data['weekday_num'] = self.data[self.config['date_col']].dt.dayofweek
    
    def _calculate_metrics(self):
        """Calculate all base metrics"""
        self._calculate_product_metrics()
        self._calculate_inventory_metrics()
        self._calculate_revenue_metrics()
    
    def _calculate_product_metrics(self):
        """Calculate product-level metrics"""
        self.product_analysis = self.data.groupby(self.config['product_col']).agg({
            self.config['description_col']: 'first',
            self.config['revenue_col']: 'sum',
            self.config['quantity_col']: 'sum',
            self.config['transaction_col']: 'count'
        }).sort_values(self.config['revenue_col'], ascending=False)
        
        # Add cumulative metrics
        self.product_analysis['revenue_cum'] = self.product_analysis[self.config['revenue_col']].cumsum()
        total_revenue = self.product_analysis[self.config['revenue_col']].sum()
        self.product_analysis['revenue_pct_cum'] = 100 * self.product_analysis['revenue_cum'] / total_revenue
        
        # Identify top products
        threshold_idx = int(len(self.product_analysis) * self.config['top_products_threshold'])
        self.product_analysis['is_top_product'] = False
        self.product_analysis.iloc[:threshold_idx, self.product_analysis.columns.get_loc('is_top_product')] = True
    
    def _calculate_inventory_metrics(self):
        """Calculate inventory health metrics"""
        last_sale = self.data.groupby(self.config['product_col']).agg({
            self.config['date_col']: 'max',
            self.config['description_col']: 'first'
        }).reset_index()
        
        analysis_date = pd.Timestamp(self.config['analysis_date'])
        last_sale['days_since_sale'] = (analysis_date - last_sale[self.config['date_col']]).dt.days
        
        # Categorize inventory status
        last_sale['status'] = pd.cut(
            last_sale['days_since_sale'],
            bins=[0, 7, 30, 60, 90, 365, 9999],
            labels=['Hot', 'Active', 'Slowing', 'Cold', 'Dead', 'Zombie']
        )
        
        self.inventory_status = last_sale
    
    def _calculate_revenue_metrics(self):
        """Calculate revenue-based metrics"""
        self.revenue_metrics = {
            'total_revenue': self.data[self.config['revenue_col']].sum(),
            'total_transactions': self.data[self.config['transaction_col']].nunique(),
            'avg_transaction_value': self.data.groupby(self.config['transaction_col'])[self.config['revenue_col']].sum().mean(),
            'total_products': self.data[self.config['product_col']].nunique(),
            'date_range': {
                'start': self.data[self.config['date_col']].min(),
                'end': self.data[self.config['date_col']].max()
            }
        }
    
    def get_kpis(self, show: bool = False) -> Dict:
        """Get key performance indicators"""
        if self.revenue_metrics is None:
            return {}
        
        # Calculate period comparisons if we have enough data
        mid_date = self.revenue_metrics['date_range']['start'] + \
                  (self.revenue_metrics['date_range']['end'] - self.revenue_metrics['date_range']['start']) / 2
        
        current_period = self.data[self.data[self.config['date_col']] >= mid_date]
        previous_period = self.data[self.data[self.config['date_col']] < mid_date]
        
        current_revenue = current_period[self.config['revenue_col']].sum()
        previous_revenue = previous_period[self.config['revenue_col']].sum()
        
        growth_rate = ((current_revenue - previous_revenue) / previous_revenue * 100) if previous_revenue > 0 else 0
        
        return_kpis = {
            'total_revenue': self.revenue_metrics['total_revenue'],
            'total_transactions': self.revenue_metrics['total_transactions'],
            'avg_transaction_value': self.revenue_metrics['avg_transaction_value'],
            'total_products': self.revenue_metrics['total_products'],
            'revenue_growth': growth_rate,
            'current_period_revenue': current_revenue,
            'previous_period_revenue': previous_revenue
        }
        
        if show:
            print(f"\n💰 Revenue: {self.format_currency(return_kpis['total_revenue'])}")
            print(f"📈 Growth: {return_kpis['revenue_growth']:.1f}%")
            print(f"🛒 Transactions: {return_kpis['total_transactions']:,}")

        return return_kpis
    
    def get_alerts(self, show: bool = False) -> Dict:
        """Get critical business alerts"""
        alerts = {
            'critical': [],
            'warning': [],
            'success': []
        }
        
        # Check for dead inventory
        if self.inventory_status is not None:
            dead_stock = self.inventory_status[
                self.inventory_status['days_since_sale'] > self.config['dead_stock_days']
            ]
            if len(dead_stock) > 0:
                alerts['critical'].append({
                    'type': 'dead_inventory',
                    'message': f'{len(dead_stock)} products haven\'t sold in {self.config["dead_stock_days"]}+ days',
                    'impact': 'Cash tied up in non-moving inventory',
                    'action': 'Consider liquidation or promotional campaigns'
                })
        
        # Check revenue concentration
        if self.product_analysis is not None:
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
            
        # Display alerts
        if show:
            if alerts['critical']:
                print("🔴 CRITICAL ACTIONS REQUIRED:")
                for alert in alerts['critical']:
                    print(f"\n  {alert['message']}")
                    print(f"  Impact: {alert['impact']}")
                    print(f"  ➔ Action: {alert['action']}")

            if alerts['warning']:
                print("\n🟡 WARNINGS:")
                for alert in alerts['warning']:
                    print(f"\n  {alert['message']}")
                    print(f"  ➔ Action: {alert['action']}")

            if alerts['success']:
                print("\n🟢 SUCCESS INDICATORS:")
                for alert in alerts['success']:
                    print(f"\n  {alert['message']}")
                    print(f"  ➔ Next Step: {alert['action']}")
        
        return alerts

    def get_pareto_insights(self, show: bool = False) -> Dict:
        """Get 80/20 analysis insights"""
        if self.product_analysis is None:
            return {}
        
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
        
        # Display insights
        if show:
            print(f"🎯 TOP INSIGHT: Your top {self.pareto['top_products_count']} products "
                f"({self.pareto['top_products_pct']:.0f}% of catalog) generate "
                f"{self.pareto['revenue_from_top_pct']:.1f}% of revenue!")

            print(f"\nConcentration Risk Level: {self.pareto['concentration_level']}")

            print("\n📋 Top 5 Revenue Generators:")
            for i, product in enumerate(self.pareto['top_products_list'][:5], 1):
                print(f"  {i}. {product['glosa']}: {self.format_currency(product['total'])}")
            print(f"\n📊 80/20 Rule: Top {self.pareto['top_products_pct']:.0f}% = {self.pareto['revenue_from_top_pct']:.1f}% of revenue")
        
        return self.pareto
    
    def save_top_products(self, out_dir: Optional[str] = None):
        """Save top products insights to CSV"""
        if self.pareto is None:
            self.pareto = self.get_pareto_insights()
        top_products_df = pd.DataFrame(self.pareto['top_products_list'])
        
        # Get save path
        save_path = out_dir or self.out_dir + f'/top_products.csv'
        
        # Save to CSV
        top_products_df.to_csv(save_path, index=False)
        print(f"✅ Top Products exported to {save_path}")

    def get_inventory_health(self, show: bool = False) -> Dict:
        """Get inventory health summary"""
        if self.inventory_status is None:
            return {}
        
        status_summary = self.inventory_status['status'].value_counts().to_dict()
        
        # Calculate tied up cash if cost data available
        dead_stock = self.inventory_status[self.inventory_status['status'].isin(['Dead', 'Zombie'])]
        
        inventory_return = {
            'status_distribution': status_summary,
            'dead_stock_count': len(dead_stock),
            'healthy_stock_pct': (status_summary.get('Hot', 0) + status_summary.get('Active', 0)) / len(self.inventory_status) * 100,
            'at_risk_products': self.inventory_status[self.inventory_status['status'] == 'Slowing'].to_dict('records')[:5]
        }
        
        if show:
            print(f"📊 Inventory Health Score: {inventory_return['healthy_stock_pct']:.0f}%")
            print(f"\n⚠️ Dead Stock Alert: {inventory_return['dead_stock_count']} products")

            if inventory_return['at_risk_products']:
                print("\n🟡 Products At Risk (Slowing):")
                for product in inventory_return['at_risk_products'][:3]:
                    print(f"  • {product['glosa']}: {product['days_since_sale']} days since last sale")
        
        return inventory_return
    
    def get_peak_times(self, show: bool = False) -> Dict:
        """Get peak business times"""
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
        
        peak_times_return = {
            'peak_hour': peak_hour,
            'peak_day': peak_day,
            'valley_day': valley_day,
            'hourly_distribution': hourly_revenue.to_dict(),
            'recommendation': f'Optimize staffing for {peak_day}s around {peak_hour}:00'
        }

        # Display insights
        if show:
            print(f"⏰ Peak Performance Windows:")
            print(f"  • Best Day: {peak_times_return['peak_day']}s")
            print(f"  • Peak Hour: {peak_times_return['peak_hour']}:00")
            print(f"  • Slowest Day: {peak_times_return['valley_day']}s")
            print(f"\n💡 {peak_times_return['recommendation']}")

        return peak_times_return
    
    def format_currency(self, value: float) -> str:
        """Format value as currency based on config"""
        if self.config['currency_format'] == 'CLP':
            return f"$ {value:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
        else:
            return f"${value:,.2f}"
        
    def save_executive_summary(self, out_dir: Optional[str] = None):
        """Save executive summary to CSV"""
        summary = {
            'Date': self.config['analysis_date'],
            'Total Revenue': self.get_kpis().get('total_revenue', 0),
            'Revenue Growth %': self.get_kpis().get('revenue_growth', 0),
            'Total Transactions': self.get_kpis().get('total_transactions', 0),
            'Top 20% Revenue Share': self.get_pareto_insights().get('revenue_from_top_pct', 0),
            'Dead Stock Count': self.get_inventory_health().get('dead_stock_count', 0),
            'Inventory Health %': self.get_inventory_health().get('healthy_stock_pct', 0)
        }
        
        # Convert to DataFrame for easy CSV export
        summary_df = pd.DataFrame([summary])
        
        # Get save path
        save_path = out_dir or self.config['out_dir'] + f'/executive_summary.csv'

        # Save to CSV
        summary_df.to_csv(save_path, index=False)
        print(f"✅ Executive summary exported to {save_path}")
