# Executive Business Intelligence Dashboard

## 📁 Project Structure

```
business_intelligence/
│
├── modules/
│   ├── __init__.py
│   ├── business_analytics.py      # Core analytics engine
│   ├── dashboard.py               # Dashboard visualization
│   └── advanced_analytics.py      # Advanced features
│
├── notebooks/
│   └── executive_notebook.ipynb   # Clean executive notebook
│
├── data/
│   └── buenacarne/
│       └── sample_completeDet.csv # Your data file
│
├── outputs/
│   ├── executive_dashboard.png    # Generated dashboard
│   └── executive_summary.csv      # Exported metrics
│
└── requirements.txt               # Dependencies
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

**requirements.txt:**
```
pandas>=1.3.0
numpy>=1.21.0
matplotlib>=3.4.0
seaborn>=0.11.0
scipy>=1.7.0
jupyter>=1.0.0
```

### 2. Basic Usage in Notebook

```python
# Import modules
from modules.business_analytics import BusinessAnalyzer
from modules.dashboard import ExecutiveDashboard
from modules.advanced_analytics import AdvancedAnalytics

# Configure
config = {
    'analysis_date': 'current',
    'currency_format': 'CLP',
    'dead_stock_days': 30
}

# Initialize
analyzer = BusinessAnalyzer('data/your_data.csv', config)
dashboard = ExecutiveDashboard(analyzer)

# Generate dashboard
dashboard.create_full_dashboard()
```

## 📊 Available Functions

### Core Analytics (business_analytics.py)

| Function                 | Description                | Returns                                   |
| ------------------------ | -------------------------- | ----------------------------------------- |
| `get_kpis()`             | Key performance indicators | Dict with revenue, transactions, growth   |
| `get_alerts()`           | Critical business alerts   | Dict with critical/warning/success alerts |
| `get_pareto_insights()`  | 80/20 analysis             | Dict with top products and concentration  |
| `get_inventory_health()` | Inventory status           | Dict with stock health metrics            |
| `get_peak_times()`       | Busiest periods            | Dict with peak hours and days             |

### Dashboard Visualizations (dashboard.py)

| Function                  | Description                  | Output                    |
| ------------------------- | ---------------------------- | ------------------------- |
| `create_full_dashboard()` | Complete executive dashboard | Matplotlib figure (20x12) |
| `create_quick_summary()`  | Text summary                 | Formatted string          |
| Individual chart methods  | Specific visualizations      | Individual plots          |

### Advanced Analytics (advanced_analytics.py)

| Function                          | Description                | Use Case               |
| --------------------------------- | -------------------------- | ---------------------- |
| `forecast_revenue()`              | Simple revenue forecasting | Planning and budgeting |
| `find_cross_sell_opportunities()` | Product affinity analysis  | Bundle recommendations |
| `customer_segmentation_rfm()`     | RFM segmentation           | Customer targeting     |
| `anomaly_detection()`             | Detect unusual patterns    | Risk management        |
| `create_trend_analysis()`         | Trend visualizations       | Strategic planning     |
| `generate_recommendations()`      | AI-powered insights        | Action prioritization  |

## 🎨 Customization

### Custom Configuration

```python
config = {
    # Data columns
    'date_col': 'fecha',
    'product_col': 'producto',
    'description_col': 'glosa',
    'revenue_col': 'total',
    'quantity_col': 'cantidad',
    'transaction_col': 'trans_id',
    
    # Analysis parameters
    'analysis_date': '2025-01-21',
    'top_products_threshold': 0.2,  # Top 20%
    'dead_stock_days': 30,
    
    # Display
    'currency_format': 'CLP',  # or 'USD'
    'language': 'EN'  # or 'ES'
}
```

### Custom Colors

```python
dashboard.colors = {
    'primary': '#2E86AB',
    'success': '#52B788',
    'warning': '#F77F00',
    'danger': '#D62828',
    'dark': '#264653',
    'light': '#F1FAEE'
}
```

## 📈 Example Outputs

### Executive Summary Text
```
==================================================
EXECUTIVE SUMMARY
==================================================

📊 KEY METRICS:
  • Total Revenue: $ 40.608.696
  • Growth Rate: 5.2%
  • Transactions: 148

🔴 CRITICAL ACTIONS:
  • 15 products haven't sold in 30+ days
    → Consider liquidation or promotional campaigns

💡 KEY INSIGHTS:
  • Top 20% of products = 46.3% of revenue
  • Inventory Health: 100% healthy
  • Dead Stock: 0 products
==================================================
```

### Dashboard Components

1. **KPI Cards**: Revenue, Transactions, Avg Value, Products
2. **Pareto Chart**: Top revenue generators
3. **Inventory Gauge**: Health status donut chart
4. **Alerts Panel**: Color-coded action items
5. **Peak Times**: Hourly revenue distribution

## 🔧 Advanced Usage

### Scheduling Automated Reports

```python
import schedule
import time

def generate_daily_report():
    analyzer = BusinessAnalyzer('data/latest.csv', config)
    dashboard = ExecutiveDashboard(analyzer)
    dashboard.create_full_dashboard(save_path=f'reports/dashboard_{datetime.now():%Y%m%d}.png')
    print(f"Report generated at {datetime.now()}")

# Schedule daily at 8 AM
schedule.every().day.at("08:00").do(generate_daily_report)

while True:
    schedule.run_pending()
    time.sleep(60)
```

### Integration with Email

```python
def email_dashboard():
    # Generate dashboard
    analyzer = BusinessAnalyzer('data.csv', config)
    dashboard = ExecutiveDashboard(analyzer)
    
    # Create reports
    dashboard.create_full_dashboard(save_path='dashboard.png')
    summary = dashboard.create_quick_summary()
    
    # Send email (using your email service)
    send_email(
        to=['executives@company.com'],
        subject='Daily Business Intelligence Report',
        body=summary,
        attachments=['dashboard.png']
    )
```

## 📝 Data Requirements

### Minimum Required Columns
- **Transaction ID**: Unique identifier for each sale
- **Date**: Transaction date (datetime format)
- **Product ID**: Product identifier
- **Product Description**: Product name/description
- **Revenue**: Total sale amount
- **Quantity**: Units sold

### Optional Columns
- **Cost**: Product cost (for margin analysis)
- **Customer ID**: For customer segmentation
- **Hour/Time**: For detailed time analysis
- **Category**: Product categories

## 🎯 Best Practices

1. **Data Quality**: Clean your data before analysis
   - Remove duplicates
   - Handle missing values
   - Standardize date formats

2. **Regular Updates**: Schedule daily/weekly runs
   - Automate data pipeline
   - Version control reports
   - Track metric changes

3. **Customization**: Adapt to your business
   - Adjust thresholds
   - Add custom KPIs
   - Modify visualizations

4. **Action Tracking**: Follow up on recommendations
   - Document actions taken
   - Measure impact
   - Iterate on strategies

## 🤝 Support

For questions or customization needs:
- Review function docstrings
- Check example notebook
- Modify configuration parameters
- Extend classes for custom features

## 📄 License

MIT License - Feel free to adapt for your business needs