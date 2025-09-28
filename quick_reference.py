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
        'project_name': 'Buenacarne',       # Project name
        
        # Data mapping
        'date_col': 'fecha',
        'product_col': 'producto',
        'description_col': 'glosa',
        'revenue_col': 'total',
        'quantity_col': 'cantidad',
        'transaction_col': 'trans_id',
        'cost_col': 'costo',
        
        # Analysis settings
        'analysis_date': datetime(2018, 1, 21),
        'top_products_threshold': 0.2,
        'dead_stock_days': 30,
        'currency_format': 'CLP',
        'language': 'EN',
        
        'output_path' : 'outputs/'          # Output directory
        
    }
    
    # 3. INITIALIZE
    analyzer = BusinessAnalyzer(
        data_source='data/buenacarne/sample_completeDet.csv',
        config=config
    )
    dashboard = ExecutiveDashboard(analyzer)
    advanced = AdvancedAnalytics(analyzer)
    
    # 4. GENERATE INSIGHTS
    
    # Quick summary
    print(dashboard.create_quick_summary())
    
    # KPIs
    kpis = analyzer.get_kpis()
    print(f"\n💰 Revenue: {analyzer.format_currency(kpis['total_revenue'])}")
    print(f"📈 Growth: {kpis['revenue_growth']:.1f}%")
    print(f"🛒 Transactions: {kpis['total_transactions']:,}")
    
    # Alerts
    alerts = analyzer.get_alerts(show=True)
    
    # Pareto insights
    pareto = analyzer.get_pareto_insights(show=True)
    print(f"\n📊 80/20 Rule: Top {pareto['top_products_pct']:.0f}% = {pareto['revenue_from_top_pct']:.1f}% of revenue")
    
    # 5. VISUALIZATIONS
    
    # Main dashboard
    fig = dashboard.create_full_dashboard(figsize=(20, 12))
    fig.savefig('outputs/executive_dashboard.png', dpi=300, bbox_inches='tight')
    
    # Trend analysis
    trend_fig = advanced.create_trend_analysis(figsize=(15, 10))
    trend_fig.savefig('outputs/trend_analysis.png', dpi=300, bbox_inches='tight')
    
    # 6. ADVANCED ANALYTICS
    
    # Forecast
    forecast = advanced.forecast_revenue(days_ahead=30)
    print(f"\n📅 30-Day Forecast: {analyzer.format_currency(forecast['forecast_total'])}")
    print(f"   Confidence: {analyzer.format_currency(forecast['confidence_interval'][0])} - {analyzer.format_currency(forecast['confidence_interval'][1])}")
    
    # Cross-sell opportunities
    cross_sell = advanced.find_cross_sell_opportunities()
    if cross_sell:
        print("\n🎯 Bundle Opportunities:")
        for opp in cross_sell[:3]:
            print(f"   • {opp['product_1'][:30]} + {opp['product_2'][:30]}")
            print(f"     Frequency: {opp['frequency']} | Support: {opp['support']:.2f}%")
    
    # Anomalies
    anomalies = advanced.anomaly_detection()
    if anomalies:
        print("\n⚠️ Anomalies Detected:")
        for anomaly in anomalies[:3]:
            print(f"   • {anomaly['description']}")
    
    # 7. RECOMMENDATIONS
    recommendations = advanced.generate_recommendations()
    print("\n💡 TOP RECOMMENDATIONS:")
    for i, rec in enumerate(recommendations[:3], 1):
        print(f"\n{i}. [{rec['priority']}] {rec['title']}")
        print(f"   {rec['description']}")
        print(f"   Action: {rec['action']}")
        print(f"   Impact: {rec['expected_impact']} | Timeline: {rec['timeframe']}")
    
    # 8. EXPORT
    
    # Export summary metrics
    summary_data = {
        'Date': datetime.now().strftime('%Y-%m-%d'),
        'Total Revenue': kpis['total_revenue'],
        'Growth %': kpis['revenue_growth'],
        'Transactions': kpis['total_transactions'],
        'Top 20% Revenue Share': pareto['revenue_from_top_pct'],
        'Dead Stock Count': analyzer.get_inventory_health()['dead_stock_count'],
        'Forecast 30 Days': forecast['forecast_total']
    }
    
    summary_df = pd.DataFrame([summary_data])
    summary_df.to_csv('outputs/executive_summary.csv', index=False)
    
    # Export top products
    top_products_df = pd.DataFrame(pareto['top_products_list'])
    top_products_df.to_csv('outputs/top_products.csv', index=False)
    
    print("\n✅ Dashboard saved to 'outputs/executive_dashboard.png'")
    print("✅ Metrics exported to 'outputs/executive_summary.csv'")
    print("✅ Analysis complete!")
    
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


def weekly_comparison_report(analyzer):
    import pandas as pd
    """Generate week-over-week comparison"""
    data = analyzer.data
    
    # Get last two weeks
    data['week'] = pd.to_datetime(data[analyzer.config['date_col']]).dt.isocalendar().week
    last_week = data['week'].max()
    prev_week = last_week - 1
    
    last_week_data = data[data['week'] == last_week]
    prev_week_data = data[data['week'] == prev_week]
    
    # Calculate metrics
    metrics = {
        'Last Week': {
            'Revenue': last_week_data[analyzer.config['revenue_col']].sum(),
            'Transactions': last_week_data[analyzer.config['transaction_col']].nunique(),
            'Products Sold': last_week_data[analyzer.config['product_col']].nunique(),
            'Avg Transaction': last_week_data.groupby(analyzer.config['transaction_col'])[analyzer.config['revenue_col']].sum().mean()
        },
        'Previous Week': {
            'Revenue': prev_week_data[analyzer.config['revenue_col']].sum(),
            'Transactions': prev_week_data[analyzer.config['transaction_col']].nunique(),
            'Products Sold': prev_week_data[analyzer.config['product_col']].nunique(),
            'Avg Transaction': prev_week_data.groupby(analyzer.config['transaction_col'])[analyzer.config['revenue_col']].sum().mean()
        }
    }
    
    # Calculate changes
    changes = {}
    for metric in ['Revenue', 'Transactions', 'Products Sold', 'Avg Transaction']:
        prev_val = metrics['Previous Week'][metric]
        last_val = metrics['Last Week'][metric]
        change = ((last_val - prev_val) / prev_val * 100) if prev_val > 0 else 0
        changes[metric] = change
    
    # Print report
    print("=" * 60)
    print("WEEKLY COMPARISON REPORT")
    print("=" * 60)
    
    for metric in ['Revenue', 'Transactions', 'Products Sold', 'Avg Transaction']:
        arrow = '↑' if changes[metric] > 0 else '↓' if changes[metric] < 0 else '→'
        color = '🟢' if changes[metric] > 0 else '🔴' if changes[metric] < -5 else '🟡'
        
        if metric == 'Revenue' or metric == 'Avg Transaction':
            last_val = analyzer.format_currency(metrics['Last Week'][metric])
            prev_val = analyzer.format_currency(metrics['Previous Week'][metric])
        else:
            last_val = f"{metrics['Last Week'][metric]:,}"
            prev_val = f"{metrics['Previous Week'][metric]:,}"
        
        print(f"\n{metric}:")
        print(f"  Last Week:     {last_val}")
        print(f"  Previous Week: {prev_val}")
        print(f"  Change:        {color} {arrow} {abs(changes[metric]):.1f}%")
    
    return metrics, changes


# =============================================================================
# MAIN EXECUTION
# =============================================================================

if __name__ == "__main__":
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
    weekly_comparison_report(analyzer)
    
    # Product velocity
    velocity_fig = product_velocity_matrix(analyzer)
    velocity_fig.savefig('outputs/product_velocity.png', dpi=300, bbox_inches='tight')
    print("\n✅ Product velocity matrix saved")
    
    # Hourly analysis
    hourly_fig = revenue_by_hour_analysis(analyzer)
    hourly_fig.savefig('outputs/hourly_analysis.png', dpi=300, bbox_inches='tight')
    print("✅ Hourly analysis saved")
    
    print("\n" + "=" * 60)
    print("ALL ANALYSES COMPLETE!")
    print("Check 'outputs/' folder for generated reports")
    print("=" * 60)