#!/usr/bin/env python3
"""
Executive Dashboard - Quick Reference Implementation
Complete working example with all features
"""

# =============================================================================
# MINIMAL WORKING EXAMPLE
# =============================================================================

def minimal_dashboard_example():
    """Simplest possible dashboard generation - 5 lines of code"""
    from modules.business_analytics import BusinessAnalyzer
    from modules.dashboard import ExecutiveDashboard
    
    analyzer = BusinessAnalyzer('data.csv')
    dashboard = ExecutiveDashboard(analyzer)
    dashboard.create_full_dashboard()


# =============================================================================
# COMPLETE IMPLEMENTATION EXAMPLE
# =============================================================================

def complete_dashboard_workflow():
    """Full implementation with all features"""
    
    # 1. IMPORTS
    import pandas as pd
    from datetime import datetime
    from modules.business_analytics import BusinessAnalyzer
    from modules.dashboard import ExecutiveDashboard
    from modules.advanced_analytics import AdvancedAnalytics
    
    # 2. CONFIGURATION
    config = {
        'project_name': 'auto_partes',       # Project name
        
        # Data mapping
        'date_col': 'fecha',
        'product_col': 'producto',
        'description_col': 'glosa',
        'revenue_col': 'total',
        'quantity_col': 'cantidad',
        'transaction_col': 'trans_id',
        'cost_col': 'costo',
        
        # Analysis settings
        'analysis_date': datetime(2024, 7, 1),  # Or 'current' for today
        'top_products_threshold': 0.2,
        'dead_stock_days': 30,
        'currency_format': 'CLP',
        'language': 'EN',
        
        'output_path' : 'outputs/'          # Output directory
        
    }
    
    # 3. INITIALIZE
    analyzer = BusinessAnalyzer(
        data_source='data/auto_partes/auto_partes_transactions.csv',
        config=config
    )
    dashboard = ExecutiveDashboard(analyzer)
    advanced = AdvancedAnalytics(analyzer)
    
    # 4. GENERATE INSIGHTS
    # Quick summary
    print(dashboard.create_quick_summary())
    
    # KPIs
    kpis = analyzer.get_kpis(show=True)
    
    # Alerts
    alerts = analyzer.get_alerts(show=True)
    
    # Pareto insights
    pareto = analyzer.get_pareto_insights(show=True)
    
    # 5. VISUALIZATIONS
    # Main dashboard
    fig = dashboard.create_full_dashboard(figsize=(20, 12))
    fig.savefig(f"{config['output_path']}{config['project_name']}/executive_dashboard.png", dpi=300, bbox_inches='tight')
    print(f"✅ Dashboard saved to '{config['output_path']}{config['project_name']}/executive_dashboard.png'")
    
    # Trend analysis
    trend_fig = advanced.create_trend_analysis(figsize=(15, 10))
    trend_fig.savefig(f"{config['output_path']}{config['project_name']}/trend_analysis.png", dpi=300, bbox_inches='tight')
    print(f"✅ Trend analysis saved to '{config['output_path']}{config['project_name']}/trend_analysis.png'")
    
    # 6. ADVANCED ANALYTICS
    # Forecast
    forecast = advanced.forecast_revenue(days_ahead=30, show=True)
  
    # Cross-sell opportunities
    cross_sell = advanced.find_cross_sell_opportunities(show=True)
    
    # Anomalies
    anomalies = advanced.anomaly_detection(show=True)
    
    # 7. RECOMMENDATIONS
    recommendations = advanced.generate_recommendations(show=True)
    
    # 8. EXPORT
    # Export summary metrics
    analyzer.save_executive_summary()

    # Export top products
    analyzer.save_top_products()

    print(f"✅ Analysis complete!")

    return analyzer, dashboard, advanced


# =============================================================================
# CUSTOM ANALYSIS FUNCTIONS
# =============================================================================

def revenue_by_hour_analysis(analyzer):
    """Detailed hourly revenue analysis"""
    import matplotlib.pyplot as plt
    
    data = analyzer.data
    hourly = data.groupby('hour')[analyzer.config['revenue_col']].agg(['sum', 'mean', 'count'])
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    
    # Total revenue by hour
    ax1.bar(hourly.index, hourly['sum'], color='#2E86AB', alpha=0.8)
    ax1.set_title('Total Revenue by Hour')
    ax1.set_xlabel('Hour')
    ax1.set_ylabel('Total Revenue')
    ax1.grid(axis='y', alpha=0.3)
    
    # Average transaction by hour
    ax2.plot(hourly.index, hourly['mean'], marker='o', color='#52B788', linewidth=2)
    ax2.fill_between(hourly.index, 0, hourly['mean'], alpha=0.3, color='#52B788')
    ax2.set_title('Average Transaction Value by Hour')
    ax2.set_xlabel('Hour')
    ax2.set_ylabel('Average Transaction')
    ax2.grid(True, alpha=0.3)
    
    plt.tight_layout()
    return fig


def product_velocity_matrix(analyzer):
    """Create product velocity matrix (revenue vs units sold)"""
    import matplotlib.pyplot as plt
    
    # Get product metrics
    products = analyzer.product_analysis.head(20)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    scatter = ax.scatter(
        products[analyzer.config['quantity_col']],
        products[analyzer.config['revenue_col']],
        s=products[analyzer.config['revenue_col']] / 10000,  # Size by revenue
        alpha=0.6,
        c=range(len(products)),
        cmap='viridis'
    )
    
    # Add quadrant lines
    ax.axvline(products[analyzer.config['quantity_col']].median(), 
              color='gray', linestyle='--', alpha=0.5)
    ax.axhline(products[analyzer.config['revenue_col']].median(), 
              color='gray', linestyle='--', alpha=0.5)
    
    # Labels
    ax.set_xlabel('Units Sold', fontsize=12)
    ax.set_ylabel('Total Revenue', fontsize=12)
    ax.set_title('Product Velocity Matrix\n(Size = Revenue)', fontsize=14, fontweight='bold')
    
    # Add quadrant labels
    ax.text(0.95, 0.95, 'Stars\n(High Revenue, High Volume)', 
           transform=ax.transAxes, ha='right', va='top', fontsize=10, 
           bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5))
    ax.text(0.05, 0.95, 'Premium\n(High Revenue, Low Volume)', 
           transform=ax.transAxes, ha='left', va='top', fontsize=10,
           bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5))
    ax.text(0.95, 0.05, 'Volume\n(Low Revenue, High Volume)', 
           transform=ax.transAxes, ha='right', va='bottom', fontsize=10,
           bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5))
    ax.text(0.05, 0.05, 'Question\n(Low Revenue, Low Volume)', 
           transform=ax.transAxes, ha='left', va='bottom', fontsize=10,
           bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.5))
    
    plt.colorbar(scatter, label='Product Rank')
    ax.grid(True, alpha=0.3)
    
    return fig




# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
    from modules.reports import weekly_comparison_report
    print("Starting Executive Dashboard Generation...")
    print("=" * 60)
    
    # Run complete workflow
    analyzer, dashboard, advanced = complete_dashboard_workflow()
    
    # Additional custom analyses
    print("\n" + "=" * 60)
    print("ADDITIONAL ANALYSES")
    print("=" * 60)
    
    # Weekly comparison
    print("\n📊 Week-over-Week Analysis:")
    weekly_comparison_report = weekly_comparison_report(analyzer)
    
    # Product velocity
    velocity_fig = product_velocity_matrix(analyzer)
    
    velocity_fig.savefig(f"{analyzer.config['output_path']}{analyzer.config['project_name']}/product_velocity.png", dpi=300, bbox_inches='tight')
    print("\n✅ Product velocity matrix saved")
    
    # Hourly analysis
    hourly_fig = revenue_by_hour_analysis(analyzer)
    hourly_fig.savefig(f"{analyzer.config['output_path']}{analyzer.config['project_name']}/hourly_analysis.png", dpi=300, bbox_inches='tight')
    print("✅ Hourly analysis saved")
    
    print("\n" + "=" * 60)
    print("ALL ANALYSES COMPLETE!")
    print("Check 'outputs/' folder for generated reports")
    print("=" * 60)