from typing import Optional
from contextlib import redirect_stdout
import os
def weekly_comparison_report(analyzer, save: bool = False):
    import pandas as pd
    """Generate week-over-week comparison"""
    data = analyzer.data
    out_dir = analyzer.out_dir
    
    # Get last two weeks
    data['week'] = pd.to_datetime(data[analyzer.config['date_col']]).dt.isocalendar().week # Extract week number
    last_week = data['week'].max() # Last week number
    prev_week = last_week - 1 # Previous week number
    
    last_week_data = data[data['week'] == last_week] # Data for last week
    prev_week_data = data[data['week'] == prev_week] # Data for previous week
    
    # Calculate metrics
    metrics = {
        'Last Week': {
            'Revenue': last_week_data[analyzer.config['revenue_col']].sum(), # Total revenue
            'Transactions': last_week_data[analyzer.config['transaction_col']].nunique(), # Unique transactions
            'Products Sold': last_week_data[analyzer.config['product_col']].nunique(), # Unique products sold
            'Avg Transaction': last_week_data.groupby(analyzer.config['transaction_col'])[analyzer.config['revenue_col']].sum().mean() # Average transaction value
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
    report_lines = []
    report_lines.append("=" * 60)
    report_lines.append("WEEKLY COMPARISON REPORT")
    report_lines.append("=" * 60)
    
    for metric in ['Revenue', 'Transactions', 'Products Sold', 'Avg Transaction']:
        arrow = '↑' if changes[metric] > 0 else '↓' if changes[metric] < 0 else '→'
        color = '🟢' if changes[metric] > 0 else '🔴' if changes[metric] < -5 else '🟡'
        
        if metric == 'Revenue' or metric == 'Avg Transaction':
            last_val = analyzer.format_currency(metrics['Last Week'][metric])
            prev_val = analyzer.format_currency(metrics['Previous Week'][metric])
        else:
            last_val = f"{metrics['Last Week'][metric]:,}"
            prev_val = f"{metrics['Previous Week'][metric]:,}"
        
        report_lines.append(f"\n{metric}:")
        report_lines.append(f"  Last Week:     {last_val}")
        report_lines.append(f"  Previous Week: {prev_val}")
        report_lines.append(f"  Change:        {color} {arrow} {abs(changes[metric]):.2f}%")
    
    report_str = "\n".join(report_lines)
    
    # Save or print
    if save:
        # Resolve save path and ensure directory exists
        save_path = out_dir + f'/reports_weekly_comparison.txt'
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        # Write printed output into file using redirect_stdout
        with open(save_path, 'w', encoding='utf-8') as out:
            with redirect_stdout(out):
                print(report_str)

        print(f"✅ Dashboard summary exported to {save_path}")
    else:
        # Print to normal stdout
        print(report_str)
    
    return metrics, changes

def product_velocity_matrix(analyzer, save: bool = False):
    """Create product velocity matrix (revenue vs units sold)"""
    import matplotlib.pyplot as plt
    import matplotlib.patheffects as pe
    from matplotlib.ticker import FuncFormatter
    
    out_dir = analyzer.out_dir
    
    # Get product metrics
    products = analyzer.product_analysis.head(20) # Top 20 products by revenue
    scale = 10000 # Adjusted size divisor for better scaling
    fig, ax = plt.subplots(figsize=(10, 8)) # Larger figure for clarity
    
    scatter = ax.scatter(
        products[analyzer.config['quantity_col']], # Units sold
        products[analyzer.config['revenue_col']], # Revenue
        s=products[analyzer.config['revenue_col']] / scale,  # Size by revenue
        alpha=0.7, # Transparency for better visibility
        c=range(len(products)), # Color by index
        cmap='nipy_spectral', # Color map
        edgecolors='w', linewidths=0.5
    )
    
    # Add quadrant lines
    ax.axvline(products[analyzer.config['quantity_col']].median(), 
              color='gray', linestyle='--', alpha=0.5) # Vertical median line
    ax.axhline(products[analyzer.config['revenue_col']].median(), 
              color='gray', linestyle='--', alpha=0.5) # Horizontal median line
    
    # Labels
    ax.set_xlabel('Units Sold', fontsize=12) # X-axis label
    ax.set_ylabel('Total Revenue', fontsize=12) # Y-axis label
    ax.set_title('Product Velocity Matrix\n(Size = Revenue)', fontsize=14, fontweight='bold') # Title
    
    # Add quadrant labels
    ax.text(0.95, 0.95, 'Stars\n(High Revenue, High Volume)', 
           transform=ax.transAxes, ha='right', va='top', fontsize=10, 
           bbox=dict(boxstyle='round', facecolor='lightgreen', alpha=0.5)) # Top-right
    ax.text(0.05, 0.95, 'Premium\n(High Revenue, Low Volume)', 
           transform=ax.transAxes, ha='left', va='top', fontsize=10,
           bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.5)) # Top-left
    ax.text(0.95, 0.05, 'Volume\n(Low Revenue, High Volume)', 
           transform=ax.transAxes, ha='right', va='bottom', fontsize=10,
           bbox=dict(boxstyle='round', facecolor='lightblue', alpha=0.5)) # Bottom-right
    ax.text(0.05, 0.05, 'Question\n(Low Revenue, Low Volume)', 
           transform=ax.transAxes, ha='left', va='bottom', fontsize=10,
           bbox=dict(boxstyle='round', facecolor='lightcoral', alpha=0.5)) # Bottom-left
    
    cb = plt.colorbar(scatter, label='Product Rank') # Colorbar for product ranking
    # Invert the colorbar so low values appear at the top and high values at the bottom
    try:
        cb.ax.invert_yaxis()
    except Exception:
        # If colorbar inversion fails for any backend, continue silently
        pass
    ax.grid(True, alpha=0.3) # Grid for better readability
    # Format Y axis (revenue) with thousand separators
    ax.yaxis.set_major_formatter(FuncFormatter(lambda x, pos: f"{x:,.0f}"))
    plt.tight_layout() # Tight layout for better spacing

    # Annotate points with product labels (use description_col if available)
    desc_col = analyzer.config.get('description_col')
    # Determine top products to emphasize (by revenue)
    top_n = min(10, len(products))
    try:
        top_idx = products[analyzer.config['revenue_col']].nlargest(top_n).index
    except Exception:
        top_idx = products.index[:top_n]

    for i, (_, row) in enumerate(products.iterrows()):
        x = row[analyzer.config['quantity_col']]
        y = row[analyzer.config['revenue_col']]
        if desc_col and desc_col in products.columns:
            label = str(row[desc_col])[:30]
        else:
            label = str(row.name)[:30]

        # Emphasize top products
        if row.name in top_idx:
            txt_kwargs = dict(fontsize=9, fontweight='bold', color='black')
            offset = (4, 4)
        else:
            txt_kwargs = dict(fontsize=7, color='black', alpha=0.8)
            offset = (3, 3)

        txt = ax.annotate(
            label,
            xy=(x, y),
            xytext=offset,
            textcoords='offset points',
            ha='left',
            va='bottom',
            **txt_kwargs
        )
        # Add a light stroke to text to increase readability over markers
        txt.set_path_effects([pe.withStroke(linewidth=1, foreground='white')])
    
    # Save or show
    if save:
        # Get save path
        save_path = out_dir + f'/reports_product_velocity_matrix.png'
        fig.savefig(save_path, dpi=300, bbox_inches='tight')
        print(f"✅ Dashboard saved to '{save_path}'")
    else:
        plt.show()
    
    return fig