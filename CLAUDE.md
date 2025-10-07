# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is an **Executive Business Intelligence Dashboard** system built in Python. It analyzes business transaction data and generates automated insights, KPIs, dashboards, and actionable recommendations for executives. The system uses modular analytics engines to process sales data and create comprehensive visualizations.

## Common Commands

### Environment Setup
```bash
# Install dependencies
pip install -r requirements.txt

# Activate virtual environment (if exists)
venv\Scripts\activate  # Windows
```

### Running Analysis

**NEW Waterfall Pipeline (Recommended):**
```bash
# Run waterfall pipeline with examples
python waterfall_example.py

# Or import and use programmatically
python
>>> from scripts.main_driver import run_minimal_pipeline
>>> results = run_minimal_pipeline('data/auto_partes/auto_partes_transactions.csv', 'my_project')
```

**Legacy Approach:**
```bash
# Run the complete workflow with all analytics
python quick_reference.py

# Run Jupyter notebooks
jupyter notebook
# Then open: exec_note.ipynb (executive summary) or full_note.ipynb (complete analysis)
```

### Jupyter Notebooks
- `exec_note.ipynb` - Clean executive notebook with core KPIs and dashboard
- `full_note.ipynb` - Comprehensive analysis with all features
- Both notebooks can save outputs or just display results (controlled by `save` parameter)

## Code Architecture

### NEW: Waterfall Pipeline Architecture (Recommended)

The project now includes a **waterfall pipeline architecture** (`scripts/` folder) that provides a clean, step-by-step data flow from raw input to insights:

```
┌────────────────────────────────────────────────────────────┐
│  1. INPUT → 2. PREPROCESSING → 3. FILTERS → 4. ATTRIBUTES → 5. SCORES  │
└────────────────────────────────────────────────────────────┘
```

**Waterfall Pipeline Modules** (`scripts/`):

1. **main_driver.py** - Pipeline orchestrator
   - Coordinates entire waterfall flow
   - Manages pipeline state and metadata
   - Provides `run_pipeline()` and `run_minimal_pipeline()` functions

2. **preprocessing.py** - Data validation and cleaning
   - Validates required columns
   - Removes duplicates and handles missing values
   - Parses dates and standardizes data types
   - Detects outliers (non-destructive)

3. **filters.py** - Row-level calculations
   - Time extraction (hour, weekday, month, etc.)
   - Profit margin and price per unit
   - Time of day classification
   - Weekend flags and transaction categorization
   - Custom filter registration

4. **attributes.py** - Aggregated metrics
   - Product, revenue, inventory, time metrics
   - KPIs and Pareto analysis
   - Forecasting and cross-sell opportunities
   - RFM customer segmentation
   - Anomaly detection

5. **score.py** - Scoring and insights
   - Business health scoring (0-100)
   - Alert generation (critical/warning/success)
   - Actionable recommendations
   - Product and inventory scoring

**Quick Start with Waterfall Pipeline:**
```python
from scripts.main_driver import run_minimal_pipeline

# One-line execution
results = run_minimal_pipeline(
    file_path='data/auto_partes/auto_partes_transactions.csv',
    project_name='my_analysis'
)
```

See `waterfall_example.py` for 6 detailed usage examples.

---

### Legacy Module System (Still Supported)

The original modular architecture remains available in `modules/`:

**1. BusinessAnalyzer** (`modules/business_analytics.py`)
- Main orchestrator for all analytics operations
- Loads and prepares transaction data (date parsing, time columns, etc.)
- Calculates core metrics: KPIs, alerts, pareto analysis, inventory health, peak times
- Handles data export and file management
- Auto-generates timestamped output directories: `outputs/{project_name}/{YYYYMMDD_HHMM}/`

**2. ExecutiveDashboard** (`modules/dashboard.py`)
- Visualization engine for creating executive dashboards
- Generates multi-panel dashboard with KPI cards, charts, and alerts
- Creates quick text summaries for rapid insight review
- Uses matplotlib/seaborn with custom color schemes

**3. AdvancedAnalytics** (`modules/advanced_analytics.py`)
- Extended analytics: forecasting, cross-sell analysis, anomaly detection
- RFM customer segmentation
- Trend analysis and AI-powered recommendations
- Statistical analysis using scipy

**4. Reports Module** (`modules/reports.py`)
- Week-over-week comparison reports
- Product velocity matrices
- Custom reporting functions

### Configuration Pattern
All modules use a consistent configuration dictionary:
```python
config = {
    'project_name': 'project_name',        # Project identifier
    'analysis_date': 'YYYY-MM-DD',         # Analysis reference date or 'current'
    'date_col': 'fecha',                   # Column name for transaction date
    'product_col': 'producto',             # Column name for product ID
    'description_col': 'glosa',            # Column name for product description
    'revenue_col': 'total',                # Column name for revenue/total
    'quantity_col': 'cantidad',            # Column name for quantity sold
    'transaction_col': 'trans_id',         # Column name for transaction ID
    'cost_col': 'costo',                   # Column name for cost (optional)
    'top_products_threshold': 0.2,         # Threshold for top products (20%)
    'dead_stock_days': 30,                 # Days without sales for dead stock alert
    'currency_format': 'CLP',              # Currency formatting
    'language': 'EN',                      # Output language
    'out_dir': 'outputs'                   # Base output directory
}
```

### Data Flow
1. **Load**: `BusinessAnalyzer` loads CSV data and applies configuration
2. **Prepare**: Auto-converts dates, creates time-based columns (hour, weekday)
3. **Calculate**: Computes all metrics (product analysis, inventory, revenue)
4. **Analyze**: Each module (`BusinessAnalyzer`, `AdvancedAnalytics`) generates insights
5. **Visualize**: `ExecutiveDashboard` creates comprehensive visual reports
6. **Export**: Save dashboards (PNG), summaries (CSV/TXT) to timestamped folders

### Key Methods by Module

**BusinessAnalyzer Core Methods:**
- `load_data(source)` - Load and prepare CSV data
- `get_kpis(show=True)` - Revenue, transactions, growth rate, average transaction
- `get_alerts(show=True)` - Critical/warning/success business alerts
- `get_pareto_insights(show=True)` - 80/20 rule analysis, top revenue generators
- `get_inventory_health(show=True)` - Dead stock detection, at-risk products
- `get_peak_times(show=True)` - Busiest hours/days for operational optimization
- `save_executive_summary()` - Export all metrics to CSV

**ExecutiveDashboard Core Methods:**
- `create_full_dashboard(figsize=(20,12), save=False)` - Complete executive dashboard
- `create_quick_summary(save=False)` - Text-based executive summary

**AdvancedAnalytics Core Methods:**
- `forecast_revenue(days_ahead=30, save=False)` - Revenue forecasting
- `find_cross_sell_opportunities(save=False)` - Product affinity analysis
- `customer_segmentation_rfm(save=False)` - RFM segmentation
- `anomaly_detection(save=False)` - Unusual pattern detection
- `create_trend_analysis(figsize=(15,10), save=False)` - Trend visualizations
- `generate_recommendations(save=False)` - AI-powered action items

### Sample Data Structure
The system expects CSV files with transaction-level data:
- **Required columns**: transaction ID, date, product ID, product description, revenue, quantity
- **Optional columns**: cost, customer ID, hour/time, category
- Sample datasets available in `data/` directory (auto_partes, bookstore, cafe_andino, etc.)

## Output Structure
All outputs are auto-saved to timestamped directories:
```
outputs/
└── {project_name}/
    └── {YYYYMMDD_HHMM}/
        ├── executive_dashboard.png
        ├── trend_analysis.png
        ├── executive_summary.csv
        ├── kpis.txt
        ├── alerts.txt
        ├── pareto.txt
        ├── inventory.txt
        └── peak_times.txt
```

## Important Implementation Details

1. **Timestamped Runs**: Each analysis run creates a unique timestamped folder (`run_dt` and `run_time` set in `__init__`)
2. **Save Parameter**: All major methods accept `save=True/False` to control file output
3. **Show Parameter**: Methods print results to console when `show=True` (default)
4. **Data Preparation**: Date parsing is automatic; time columns auto-generated if missing
5. **Metric Caching**: BusinessAnalyzer caches calculated metrics (product_analysis, revenue_metrics, etc.)
6. **Error Handling**: Uses `warnings.filterwarnings('ignore')` and `redirect_stdout` for clean output

## Quick Reference Implementation
See `quick_reference.py` for:
- Minimal 5-line dashboard example
- Complete workflow with all features
- Custom analysis functions
- Automated report generation examples

## Common Development Tasks

### Adding a New Analytics Function
Add to the appropriate module:
- Core business metrics → `business_analytics.py`
- Visualizations → `dashboard.py`
- Advanced statistical analysis → `advanced_analytics.py`
- Custom reports → `reports.py`

### Testing with Different Datasets
Multiple sample datasets exist in `data/`:
- `auto_partes/` - Auto parts store
- `bookstore/` - Bookstore transactions
- `cafe_andino/` - Coffee shop
- `cerveza_losandes/` - Brewery
- `estilo_santiago/` - Clothing store
- `farmacia_salud/` - Pharmacy
- `techo_max/` - Home improvement
- `buenacarne/` - Original sample data

Each has a `{name}_transactions.csv` file ready for analysis.

### Customizing Visualizations
Dashboard colors are defined in `ExecutiveDashboard.colors` dictionary and can be modified after initialization:
```python
dashboard.colors['primary'] = '#NEW_COLOR'
```
