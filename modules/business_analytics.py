"""
Business Analytics Core Module
Main analytics engine for executive dashboards
"""

from matplotlib.pylab import pareto
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
from contextlib import redirect_stdout
import warnings
import os
warnings.filterwarnings('ignore')

class BusinessAnalyzer:
    """Main orchestrator for business analytics"""
    
    def __init__(self, data_source: str = None, config: Dict = None):
        """Initialize the analyzer with data and configuration"""
        self.config = config or self._default_config()
        self.data = None
        self.product_analysis = None
        self.inventory_status = None
        self.revenue_metrics = None
        self.pareto = None
        
        # Initialize run timestamp strings for unique file names
        now = datetime.now()
        self.run_dt = now.strftime('%Y%m%d') # YYYYMMDD, e.g. '20250927'
        self.run_time = now.strftime('%H%M') # HHMM, e.g. '1435'
        
        # Prepare data if provided
        if data_source:
            self.load_data(data_source)
        
        # Prepare output directory
        self.out_dir = self._set_out_dir()
        print(f"Output directory set to: {self.out_dir}")
    
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

    # INTERNAL METHODS
    def _set_out_dir(self) -> str:
        # Get save path if not defined
        output_dir = os.path.join(self.config['out_dir'], self.config['project_name'], f"{self.run_dt}_{self.run_time}")
        return output_dir
    
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

    # PUBLIC METHODS
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
        
    def get_kpis(self, save: bool = False) -> Dict:
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
        
        kpi_str = []
        kpi_str.append(f"\n💰 Revenue: {self.format_currency(return_kpis['total_revenue'])}")
        kpi_str.append(f"📈 Growth: {return_kpis['revenue_growth']:.1f}%")
        kpi_str.append(f"🛒 Transactions: {return_kpis['total_transactions']:,}")
        kpi_str = "\n".join(kpi_str)
        
        if save:
            # Resolve save path and ensure directory exists
            save_path = (self.out_dir) + f'/BA_kpi.txt'
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            # Write printed output into file using redirect_stdout
            with open(save_path, 'w', encoding='utf-8') as out:
                with redirect_stdout(out):
                    print(kpi_str)

            print(f"✅ KPIs exported to {save_path}")
        else:
            # Print to normal stdout
            print(kpi_str)
        
        return return_kpis
    
    def get_alerts(self, save: bool = False) -> Dict:
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
    
        alerts_str = "\n".join(alerts_str)
        
        if save:
            # Resolve save path and ensure directory exists
            save_path = (self.out_dir) + f'/BA_alerts.txt'
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            # Write printed output into file using redirect_stdout
            with open(save_path, 'w', encoding='utf-8') as out:
                with redirect_stdout(out):
                    print(alerts_str)

            print(f"✅ Alerts exported to {save_path}")
        else:
            # Print to normal stdout
            print(alerts_str)
        
        return alerts

    def get_pareto_insights(self, top_products_count: int = 5, save: bool = False) -> Dict:
        """Get 80/20 analysis insights"""
        if self.product_analysis is None:
            return {}
        
        # Calculate Pareto insights
        twenty_percent = int(len(self.product_analysis) * self.config['top_products_threshold']) # Top 20%
        top_products = self.product_analysis.iloc[:twenty_percent] # Top 20% products by revenue
        
        revenue_from_top = top_products[self.config['revenue_col']].sum() # Revenue from top 20%
        total_revenue = self.product_analysis[self.config['revenue_col']].sum() # Total revenue
        revenue_pct = (revenue_from_top / total_revenue) * 100 # Percentage of revenue from top 20%
        
        self.pareto = {
            'top_products_count': twenty_percent,
            'top_products_pct': self.config['top_products_threshold'] * 100,
            'revenue_from_top': revenue_from_top,
            'revenue_from_top_pct': revenue_pct,
            'top_products_list': top_products.head(10).to_dict('records'),
            'concentration_level': 'High' if revenue_pct > 80 else 'Medium' if revenue_pct > 60 else 'Low'
        }
        
        # Print insights
        pareto_str = []
        pareto_str.append(f"🎯 TOP INSIGHT: Your top {self.pareto['top_products_count']} products "
            f"({self.pareto['top_products_pct']:.0f}% of catalog) generate "
            f"{self.pareto['revenue_from_top_pct']:.1f}% of revenue!")

        pareto_str.append(f"\nConcentration Risk Level: {self.pareto['concentration_level']}")

        pareto_str.append(f"\n📋 Top {top_products_count} Revenue Generators:")
        for i, product in enumerate(self.pareto['top_products_list'][:top_products_count], 1):
            pareto_str.append(f"  {i}. {product['glosa']}: {self.format_currency(product['total'])}")
        
        pareto_str.append(f"\n📊 80/20 Rule: Top {self.pareto['top_products_pct']:.0f}% = {self.pareto['revenue_from_top_pct']:.1f}% of revenue")
        
        pareto_str = "\n".join(pareto_str)
        
        # Save to file if needed
        if save:
            # Resolve save path and ensure directory exists
            save_path = (self.out_dir) + f'/BA_pareto.txt'
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            # Write printed output into file using redirect_stdout
            with open(save_path, 'w', encoding='utf-8') as out:
                with redirect_stdout(out):
                    print(pareto_str)

            print(f"✅ Dashboard summary exported to {save_path}")
        else:
            # Print to normal stdout
            print(pareto_str)
            
        return self.pareto

    def get_inventory_health(self, save: bool = False) -> Dict:
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
        
        # Print summary
        inv_health_str = []
        inv_health_str.append(f"📊 Inventory Health Score: {inventory_return['healthy_stock_pct']:.0f}%")
        inv_health_str.append(f"\n⚠️ Dead Stock Alert: {inventory_return['dead_stock_count']} products")

        if inventory_return['at_risk_products']:
            inv_health_str.append("\n🟡 Products At Risk (Slowing):")
            for product in inventory_return['at_risk_products'][:3]:
                inv_health_str.append(f"  • {product['glosa']}: {product['days_since_sale']} days since last sale")
        inv_health_str = "\n".join(inv_health_str)
        
        if save:
            # Resolve save path and ensure directory exists
            save_path = (self.out_dir) + f'/BA_inventory_health.txt'
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            # Write printed output into file using redirect_stdout
            with open(save_path, 'w', encoding='utf-8') as out:
                with redirect_stdout(out):
                    print(inv_health_str)

            print(f"✅ Dashboard summary exported to {save_path}")
        else:
            # Print to normal stdout
            print(inv_health_str)
        
        return inventory_return
    
    def get_peak_times(self, save: bool = False) -> Dict:
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
        peaks_str = []
        peaks_str.append(f"⏰ Peak Performance Windows:")
        peaks_str.append(f"  • Best Day: {peak_times_return['peak_day']}s")
        peaks_str.append(f"  • Peak Hour: {peak_times_return['peak_hour']}:00")
        peaks_str.append(f"  • Slowest Day: {peak_times_return['valley_day']}s")
        peaks_str.append(f"\n💡 {peak_times_return['recommendation']}")
        peaks_str = "\n".join(peaks_str)
        
        if save:
            # Resolve save path and ensure directory exists
            save_path = (self.out_dir) + f'/BA_peak_times.txt'
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            # Write printed output into file using redirect_stdout
            with open(save_path, 'w', encoding='utf-8') as out:
                with redirect_stdout(out):
                    print(peaks_str)

            print(f"✅ Dashboard summary exported to {save_path}")
        else:
            # Print to normal stdout
            print(peaks_str)

        return peak_times_return
    
    def format_currency(self, value: float) -> str:
        """Format value as currency based on config"""
        if self.config['currency_format'] == 'CLP':
            return f"$ {value:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
        else:
            return f"${value:,.2f}"
        
    def save_executive_summary(self, save: bool = False):
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
        
        # Save or print
        if save:
            # Resolve save path and ensure directory exists
            save_path = (self.out_dir) + f'/BA_executive_summary.csv'
            os.makedirs(os.path.dirname(save_path), exist_ok=True)

            # Write printed output into file using redirect_stdout
            summary_df.to_csv(save_path, index=False)
            print(f"✅ Executive summary exported to {save_path}")

