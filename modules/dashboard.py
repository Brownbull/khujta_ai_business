"""
Executive Dashboard Module
Creates comprehensive dashboard visualizations for executives
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.gridspec import GridSpec
from typing import Dict
import warnings
warnings.filterwarnings('ignore')

from modules.business_analytics import BusinessAnalyzer
from modules.logger import get_logger

# Initialize logger for this module
logger = get_logger(__name__)

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")


class ExecutiveDashboard:
    """
    Executive dashboard that works with a BusinessAnalyzer instance.
    Uses composition to access business data and analytics.
    """

    def __init__(self, analyzer: BusinessAnalyzer):
        """
        Initialize dashboard with a BusinessAnalyzer instance

        Args:
            analyzer: BusinessAnalyzer instance (which extends Business)
        """
        if not isinstance(analyzer, BusinessAnalyzer):
            raise TypeError("Expected BusinessAnalyzer instance")

        self.analyzer = analyzer
        logger.info(f"Dashboard initialized for project: {self.analyzer.config['project_name']}")
        self.colors = {
            'primary': '#2E86AB',
            'success': '#52B788',
            'warning': '#F77F00',
            'danger': '#D62828',
            'dark': '#264653',
            'light': '#F1FAEE'
        }
        self.dashboard = None

    # PRIVATE METHODS
    def _create_kpi_cards(self, fig, gridspec, kpis):
        """Create KPI metric cards"""
        from modules.translations import get_text

        lang = self.analyzer.config.get('language', 'ENG')

        # gridspec may be a SubplotSpec (e.g. gs[0, :]) spanning the full top row.
        # Create a nested sub-gridspec with 1 row x 4 cols to place four KPI cards.
        try:
            sub_gs = gridspec.subgridspec(1, 4)
        except AttributeError:
            # Older matplotlib versions may not have subgridspec method; fall back
            # to GridSpecFromSubplotSpec
            from matplotlib.gridspec import GridSpecFromSubplotSpec
            sub_gs = GridSpecFromSubplotSpec(1, 4, subplot_spec=gridspec)

        # Create 4 subplots for KPIs
        axes = [fig.add_subplot(sub_gs[0, i]) for i in range(4)]

        # KPI data
        kpi_configs = [
            {
                'title': get_text('kpi_total_revenue', lang),
                'value': self.analyzer.format_currency(kpis.get('total_revenue', 0)),
                'change': kpis.get('revenue_growth', 0),
                'color': self.colors['primary']
            },
            {
                'title': get_text('kpi_transactions', lang),
                'value': f"{kpis.get('total_transactions', 0):,}",
                'change': None,
                'color': self.colors['success']
            },
            {
                'title': get_text('kpi_avg_transaction', lang),
                'value': self.analyzer.format_currency(kpis.get('avg_transaction_value', 0)),
                'change': None,
                'color': self.colors['warning']
            },
            {
                'title': get_text('kpi_active_products', lang),
                'value': f"{kpis.get('total_products', 0):,}",
                'change': None,
                'color': self.colors['dark']
            }
        ]
        
        for ax, kpi in zip(axes, kpi_configs):
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            
            # Background
            rect = plt.Rectangle((0.05, 0.1), 0.9, 0.8, 
                                facecolor=kpi['color'], alpha=0.1, 
                                edgecolor=kpi['color'], linewidth=2)
            ax.add_patch(rect)
            
            # Title
            ax.text(0.5, 0.75, kpi['title'], 
                   ha='center', va='center', fontsize=11, 
                   color='gray', fontweight='bold')
            
            # Value
            ax.text(0.5, 0.45, kpi['value'], 
                   ha='center', va='center', fontsize=16, 
                   color=kpi['color'], fontweight='bold')
            
            # Change indicator
            if kpi['change'] is not None:
                arrow = '↑' if kpi['change'] > 0 else '↓' if kpi['change'] < 0 else '→'
                change_color = self.colors['success'] if kpi['change'] > 0 else self.colors['danger']
                ax.text(0.5, 0.2, f"{arrow} {abs(kpi['change']):.1f}%", 
                       ha='center', va='center', fontsize=10, 
                       color=change_color, fontweight='bold')
    
    def _create_pareto_chart(self, ax, pareto):
        """Create Pareto chart for revenue concentration"""
        from modules.translations import get_text

        lang = self.analyzer.config.get('language', 'ENG')

        if not pareto or not pareto.get('top_products_list'):
            ax.text(0.5, 0.5, 'No data available', ha='center', va='center')
            return

        # Get top 10 products
        products = pareto['top_products_list'][:10]
        names = [p[self.analyzer.config['description_col']][:20] + '...'
                if len(p[self.analyzer.config['description_col']]) > 20
                else p[self.analyzer.config['description_col']]
                for p in products]
        revenues = [p[self.analyzer.config['revenue_col']] for p in products]

        # Create horizontal bar chart
        y_pos = np.arange(len(names))
        bars = ax.barh(y_pos, revenues, color=self.colors['primary'], alpha=0.8)

        # Customize
        ax.set_yticks(y_pos)
        ax.set_yticklabels(names, fontsize=9)
        ax.set_xlabel(get_text('revenue_axis', lang), fontsize=10)

        title = get_text('top_revenue_generators_title', lang, n=10)
        subtitle = get_text('pareto_subtitle', lang,
                           pct=f"{pareto['top_products_pct']:.0f}",
                           revenue_pct=f"{pareto['revenue_from_top_pct']:.1f}")
        ax.set_title(f'{title}\n({subtitle})',
                    fontsize=11, fontweight='bold', pad=10)
        
        # Add value labels
        for i, (bar, revenue) in enumerate(zip(bars, revenues)):
            ax.text(bar.get_width() * 0.98, bar.get_y() + bar.get_height()/2,
                   self.analyzer.format_currency(revenue),
                   ha='right', va='center', fontsize=8, color='white', fontweight='bold')
        
        ax.grid(axis='x', alpha=0.3)
    
    def _create_inventory_gauge(self, ax, inventory):
        """Create inventory health gauge"""
        if not inventory:
            ax.text(0.5, 0.5, 'No data available', ha='center', va='center')
            return
        
        # Data for pie chart
        status_dist = inventory.get('status_distribution', {})
        if not status_dist:
            ax.text(0.5, 0.5, 'No inventory data', ha='center', va='center')
            return
        
        # Prepare data
        from modules.translations import translate_status_name
        lang = self.analyzer.config.get('language', 'ENG')

        status_order = ['Hot', 'Active', 'Slowing', 'Cold', 'Dead', 'Zombie']
        status_colors = {
            'Hot': self.colors['success'],
            'Active': '#90EE90',
            'Slowing': self.colors['warning'],
            'Cold': '#FFB84D',
            'Dead': self.colors['danger'],
            'Zombie': '#8B0000'
        }

        labels = []
        sizes = []
        colors = []

        for status in status_order:
            if status in status_dist and status_dist[status] > 0:
                translated_status = translate_status_name(status, lang)
                labels.append(f"{translated_status}\n({status_dist[status]})")
                sizes.append(status_dist[status])
                colors.append(status_colors[status])
        
        # Create donut chart
        wedges, texts, autotexts = ax.pie(sizes, labels=labels, colors=colors,
                                          autopct='%1.1f%%', startangle=90,
                                          pctdistance=0.85)
        
        # Create donut hole
        centre_circle = plt.Circle((0, 0), 0.70, fc='white')
        ax.add_artist(centre_circle)
        
        # Add center text
        healthy_pct = inventory.get('healthy_stock_pct', 0)
        from modules.translations import get_text
        lang = self.analyzer.config.get('language', 'ENG')

        ax.text(0, 0, f'{healthy_pct:.0f}%\n{get_text("healthy_label", lang)}',
               ha='center', va='center', fontsize=14, fontweight='bold',
               color=self.colors['success'] if healthy_pct > 70 else self.colors['warning'])

        ax.set_title(get_text('inventory_health_title', lang), fontsize=11, fontweight='bold', pad=20)
        
        # Style text
        for text in texts:
            text.set_fontsize(9)
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(8)
            autotext.set_fontweight('bold')
    
    def _create_alerts_panel(self, ax, alerts):
        """Create alerts and recommendations panel"""
        from modules.translations import get_text
        lang = self.analyzer.config.get('language', 'ENG')

        ax.axis('off')
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)

        # Title
        ax.text(0.5, 0.95, f'⚡ {get_text("alerts_actions_title", lang)}',
               ha='center', va='top', fontsize=12, fontweight='bold')
        
        y_position = 0.85
        
        # Critical alerts
        for alert in alerts.get('critical', []):
            ax.text(0.05, y_position, '🔴', fontsize=12, va='center')
            ax.text(0.1, y_position, alert['message'], 
                   fontsize=9, va='center', fontweight='bold')
            ax.text(0.1, y_position - 0.05, f"→ {alert['action']}", 
                   fontsize=8, va='center', style='italic', color='gray')
            y_position -= 0.15
        
        # Warning alerts
        for alert in alerts.get('warning', []):
            ax.text(0.05, y_position, '🟡', fontsize=12, va='center')
            ax.text(0.1, y_position, alert['message'], 
                   fontsize=9, va='center', fontweight='bold')
            ax.text(0.1, y_position - 0.05, f"→ {alert['action']}", 
                   fontsize=8, va='center', style='italic', color='gray')
            y_position -= 0.15
        
        # Success alerts
        for alert in alerts.get('success', [])[:2]:  # Limit to 2 success messages
            ax.text(0.05, y_position, '🟢', fontsize=12, va='center')
            ax.text(0.1, y_position, alert['message'], 
                   fontsize=9, va='center', fontweight='bold')
            ax.text(0.1, y_position - 0.05, f"→ {alert['action']}", 
                   fontsize=8, va='center', style='italic', color='gray')
            y_position -= 0.15
        
        # Add border
        rect = plt.Rectangle((0.02, 0.02), 0.96, 0.88, 
                            facecolor='none', edgecolor='gray', 
                            linewidth=1, linestyle='--', alpha=0.3)
        ax.add_patch(rect)
    
    def _create_peak_times_chart(self, ax, peak_times):
        """Create peak business times visualization"""
        from modules.translations import get_text
        lang = self.analyzer.config.get('language', 'ENG')

        if not peak_times or not peak_times.get('hourly_distribution'):
            ax.text(0.5, 0.5, 'No timing data available', ha='center', va='center')
            return

        # Prepare data
        hours = list(peak_times['hourly_distribution'].keys())
        revenues = list(peak_times['hourly_distribution'].values())

        # Create bar chart
        bars = ax.bar(hours, revenues, color=self.colors['primary'], alpha=0.7, edgecolor='black', linewidth=1)

        # Highlight peak hour
        peak_hour = peak_times['peak_hour']
        if peak_hour in hours:
            peak_idx = hours.index(peak_hour)
            bars[peak_idx].set_color(self.colors['success'])
            bars[peak_idx].set_alpha(1.0)

        # Customize
        ax.set_xlabel(get_text('hour_of_day', lang), fontsize=10)
        ax.set_ylabel(get_text('revenue_axis', lang), fontsize=10)
        ax.set_title(f'{get_text("revenue_by_hour", lang)}\n{get_text("peak_label", lang)}: {peak_times["peak_day"]}s @ {peak_hour}:00',
                    fontsize=11, fontweight='bold')
        
        # Add grid
        ax.grid(axis='y', alpha=0.3)
        ax.set_axisbelow(True)
        
        # Add recommendation
        ax.text(0.5, -0.15, peak_times.get('recommendation', ''), 
               transform=ax.transAxes, ha='center', va='top',
               fontsize=9, style='italic', color='gray')
        
    # PUBLIC METHODS
    def create_full_dashboard(self, figsize=(20, 12)):
        """
        Create comprehensive executive dashboard

        Returns:
            matplotlib.figure.Figure: The generated dashboard figure

        Note:
            To save the dashboard, use fig.savefig() or a utility function
        """
        from modules.translations import get_text
        lang = self.analyzer.config.get('language', 'ENG')

        fig = plt.figure(figsize=figsize, facecolor='white')
        gs = GridSpec(3, 4, figure=fig, hspace=0.3, wspace=0.3)

        # Title
        fig.suptitle(get_text('dashboard_title', lang),
                    fontsize=24, fontweight='bold', y=0.98)

        # Get data from analyzer
        kpis = self.analyzer.get_kpis()
        alerts = self.analyzer.get_alerts()
        pareto = self.analyzer.get_pareto_insights()
        inventory = self.analyzer.get_inventory_health()
        peak_times = self.analyzer.get_peak_times()

        # 1. KPI Cards (top row)
        self._create_kpi_cards(fig, gs[0, :], kpis)

        # 2. Revenue Concentration (left middle)
        ax_pareto = fig.add_subplot(gs[1, :2])
        self._create_pareto_chart(ax_pareto, pareto)

        # 3. Inventory Health (right middle)
        ax_inventory = fig.add_subplot(gs[1, 2:])
        self._create_inventory_gauge(ax_inventory, inventory)

        # 4. Alerts Panel (bottom left)
        ax_alerts = fig.add_subplot(gs[2, :2])
        self._create_alerts_panel(ax_alerts, alerts)

        # 5. Peak Times Heatmap (bottom right)
        ax_peak = fig.add_subplot(gs[2, 2:])
        self._create_peak_times_chart(ax_peak, peak_times)

        # Add timestamp
        fig.text(0.99, 0.01, f'{get_text("generated_label", lang)}: {pd.Timestamp.now().strftime("%Y-%m-%d %H:%M")}',
                ha='right', va='bottom', fontsize=8, style='italic', color='gray')

        plt.tight_layout()

        # Store the figure in the instance for later use
        self.dashboard = fig

        return fig
    
    def create_quick_summary(self) -> str:
        """
        Create a quick text summary for executives

        Returns:
            str: Formatted summary string

        Note:
            To print or save, use print() or utils.print_info()
        """
        from modules.translations import get_text

        lang = self.analyzer.config.get('language', 'ENG')
        kpis = self.analyzer.get_kpis()
        alerts = self.analyzer.get_alerts()
        pareto = self.analyzer.get_pareto_insights()
        inventory = self.analyzer.get_inventory_health()

        summary = []
        summary.append("=" * 60)
        summary.append(get_text('dashboard_summary', lang))
        summary.append("=" * 60)

        # KPIs
        summary.append(f"\n📊 {get_text('key_metrics', lang)}")
        summary.append(f"  • {get_text('total_revenue', lang)}: {self.analyzer.format_currency(kpis['total_revenue'])}")
        summary.append(f"  • {get_text('growth_rate', lang)}: {kpis['revenue_growth']:.1f}%")
        summary.append(f"  • {get_text('transactions', lang).capitalize()}: {kpis['total_transactions']:,}")

        # Critical alerts
        if alerts.get('critical'):
            summary.append(f"\n🔴 {get_text('critical_actions_short', lang)}")
            for alert in alerts.get('critical', []):
                summary.append(f"  • {alert.get('message')}")
                summary.append(f"    → {alert.get('action')}")

        # Prepare output string
        products_label = get_text('products', lang)
        summary.append(f"\n💡 {get_text('key_insights', lang)}")
        summary.append(f"  • Top {pareto.get('top_products_pct', 0):.0f}% {products_label} = {pareto.get('revenue_from_top_pct', 0):.1f}% {get_text('revenue', lang).lower()}")
        summary.append(f"  • {get_text('inventory_health', lang)}: {inventory.get('healthy_stock_pct', 0):.0f}% healthy")
        summary.append(f"  • {get_text('dead_stock', lang)}: {inventory.get('dead_stock_count', 0)} {products_label}")

        summary.append("\n" + "=" * 60)

        return "\n".join(summary)
    
        