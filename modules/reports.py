from typing import Optional
from contextlib import redirect_stdout
def weekly_comparison_report(analyzer, save_path: Optional[str] = None):
    import pandas as pd
    """Generate week-over-week comparison"""
    data = analyzer.data
    
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

    print(report_str)
    if not save_path:
        # Save report to text file
        import os
        # Get save path if not defined
        if not save_path:
            output_dir = analyzer.config['output_path'] + analyzer.config['project_name']
            if not os.path.exists(output_dir):
                print(f"📂 Creating output directory: {output_dir}")
                os.makedirs(output_dir, exist_ok=True)
            save_path = output_dir + f'/weekly_comparison_{analyzer.run_dt}_{analyzer.run_time}.txt'
        
        # Save to text
    with open(save_path, 'w', encoding='utf-8') as out:
        with redirect_stdout(out):
            print(report_str)
                
    print(f"\n✅ Weekly comparison report exported to {save_path}")

    return metrics, changes

