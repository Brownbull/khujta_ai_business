# ModelDriver - Simplified Feature Pipeline

A clean, lightweight system for defining and executing data transformations with **automatic dependency resolution** and **dynamic input determination**.

## Key Innovation

**Problem Solved**: If you define attributes A, B, C that require inputs a1, a2, b1, c1, and then ask for only attributes A and C in the output, the system automatically determines that only inputs a1, a2, c1 are needed.

This eliminates the manual tracking of input requirements and enables flexible, on-demand feature computation.

## Quick Start

```python
from model_driver import ModelDriver
import pandas as pd

# 1. Create driver
driver = ModelDriver({
    'client_name': 'my_client',
    'model_name': 'sales_analysis',
    'output_base': 'data_management/'
})

# 2. Define features (simple functions)
def profit_margin(df):
    df['profit_margin'] = (df['revenue'] - df['cost']) / df['revenue'] * 100
    return df

def total_revenue(df):
    product_revenue = df.groupby('product')['revenue'].sum().reset_index()
    product_revenue.columns = ['product', 'total_revenue']
    return df.merge(product_revenue, on='product', how='left')

# 3. Register features
driver.register_filter('profit_margin', profit_margin,
                      inputs=['revenue', 'cost'],
                      outputs=['profit_margin'])

driver.register_attribute('total_revenue', total_revenue,
                         inputs=['product', 'revenue'],
                         outputs=['total_revenue'])

# 4. Select desired outputs
driver.set_output_attributes(['total_revenue'])

# 5. Check required inputs (automatic!)
required = driver.get_required_inputs()
# Output: ['product', 'revenue']
# Notice: 'cost' is NOT required because we're not computing profit_margin!

# 6. Execute
results = driver.execute(df)
```

## Architecture

### Components

1. **FeatureRegistry** (`feature_simple.py`)
   - Simple feature registration without decorator magic
   - Stores feature metadata (inputs, outputs, dependencies)
   - Supports filters (row-level) and attributes (aggregations)

2. **DependencyResolver** (`resolver.py`)
   - Backward dependency walking from outputs to inputs
   - Topological sort for execution ordering
   - Circular dependency detection
   - Execution plan generation

3. **ModelDriver** (`driver.py`)
   - Main orchestrator class
   - Configuration management
   - Staged pipeline execution
   - Output management

### Feature Types

- **Filters**: Row-level calculations (profit margin, price per unit, time features)
- **Attributes**: Aggregations or derived metrics (total revenue, average margin, etc.)

### Pipeline Stages

```
Input Data
    ↓
[1] Preprocessing (validation, type conversion)
    ↓
[2] Filters (row-level calculations)
    ↓
[3] Attributes (aggregations)
    ↓
[4] Output (select requested attributes)
    ↓
Final Output
```

## Key Features

### 1. Dynamic Input Resolution

```python
# Register multiple features
driver.register_filter('profit', calc_profit,
                      inputs=['revenue', 'cost'],
                      outputs=['profit'])

driver.register_filter('price_per_unit', calc_price,
                      inputs=['revenue', 'quantity'],
                      outputs=['price_per_unit'])

driver.register_attribute('total_revenue', calc_total_revenue,
                         inputs=['product', 'revenue'],
                         outputs=['total_revenue'])

# Case 1: Only need total_revenue
driver.set_output_attributes(['total_revenue'])
driver.get_required_inputs()
# → ['product', 'revenue']

# Case 2: Add profit
driver.set_output_attributes(['total_revenue', 'profit'])
driver.get_required_inputs()
# → ['cost', 'product', 'revenue']
# Notice: 'quantity' still NOT needed!
```

### 2. Dependency Tracking

```python
# Filter depends on nothing
driver.register_filter('profit_margin', calc_profit_margin,
                      inputs=['revenue', 'cost'],
                      outputs=['profit_margin'])

# Attribute depends on filter
driver.register_attribute('avg_profit_margin', calc_avg_margin,
                         inputs=['product', 'profit_margin'],
                         outputs=['avg_profit_margin'],
                         depends_on=['profit_margin'])  # ← Dependency

# When you request avg_profit_margin, profit_margin is auto-computed
driver.set_output_attributes(['avg_profit_margin'])
# Executes: profit_margin → avg_profit_margin (in correct order)
```

### 3. Staged Output

```python
driver = ModelDriver({
    'client_name': 'auto_partes',
    'model_name': 'sales_v1',
    'save_intermediates': True
})

results = driver.execute(df)

# Saves to: data_management/auto_partes/sales_v1/20251007_164812/
#   01_preprocess/
#     preprocessed.csv
#   02_features/
#     filtered.csv
#   03_attributes/
#     attributes.csv
#   04_output/
#     final_output.csv
#   execution_metadata.json
```

### 4. Execution Plans

```python
driver.print_execution_plan()

# Output:
# ======================================================================
# EXECUTION PLAN
# ======================================================================
#
# Output Features (2):
#   - total_revenue
#   - avg_profit_margin
#
# Required Features (3):
#   - total_revenue [attribute]
#   - avg_profit_margin [attribute]
#   - profit_margin [filter]
#
# Required Inputs (3):
#   - cost
#   - product
#   - revenue
#
# Execution Order:
#   1. profit_margin [filter]
#   2. avg_profit_margin [attribute] (after: profit_margin)
#   3. total_revenue [attribute]
# ======================================================================
```

## Comparison with Previous Approach

### Before (feature_engine)

- Complex decorator-based registration: `@register_filter(...)`
- ~1700 lines of code
- No automatic input resolution
- Manual dependency tracking
- Difficult to understand execution flow

### After (model_driver)

- Simple function + explicit registration
- ~800 lines of code (driver.py + resolver.py + feature_simple.py)
- Automatic input resolution based on output selection
- Automatic dependency resolution and execution ordering
- Clear, transparent execution flow

## Example Use Cases

### Use Case 1: Minimal Feature Set for Testing

```python
# You have 50 features defined, but only want to test 2
driver.set_output_attributes(['feature_a', 'feature_b'])
# Only computes feature_a, feature_b, and their dependencies
# Only loads required input columns
```

### Use Case 2: Different Outputs for Different Clients

```python
# Client A wants full analytics
driver_a.set_output_attributes(['revenue', 'margin', 'growth', 'forecast'])

# Client B only wants basic metrics
driver_b.set_output_attributes(['revenue', 'margin'])
# Automatically uses fewer inputs and executes faster
```

### Use Case 3: Incremental Feature Development

```python
# Start simple
driver.register_filter('profit', calc_profit, inputs=['revenue', 'cost'], ...)
driver.set_output_attributes(['profit'])

# Add more features over time
driver.register_attribute('total_profit', calc_total_profit,
                         inputs=['product', 'profit'],
                         depends_on=['profit'])

# Old code still works, new features available when needed
driver.set_output_attributes(['total_profit'])
# profit is computed automatically as a dependency
```

## Files

- `__init__.py` - Module exports
- `feature_simple.py` - FeatureRegistry and FeatureMetadata
- `resolver.py` - DependencyResolver with topological sort
- `driver.py` - ModelDriver main orchestrator
- `README.md` - This file

## Demo

Run the demo to see all features in action:

```bash
python model_driver_example.py
```

Demos include:
1. Basic usage with filters only
2. Features with dependencies
3. Minimal output = minimal inputs (key innovation)
4. Staged output with file saving

## Next Steps

To integrate with the business analytics project:

1. **Migrate existing features** from `waterfall/scripts/` or `feature_engine/`
2. **Create feature definitions** using simple functions
3. **Register features** in a central feature catalog
4. **Use ModelDriver** in notebooks and scripts
5. **Enable staged outputs** for data lineage tracking

## Benefits

✓ **Simpler**: No decorator magic, just functions + metadata
✓ **Flexible**: Select any subset of outputs
✓ **Efficient**: Only computes what's needed
✓ **Transparent**: Clear execution plans
✓ **Maintainable**: Easy to add/remove features
✓ **Debuggable**: Staged outputs for inspection
✓ **Scalable**: Works with small or large feature sets

---

Built following the requirements in [forest_plan.md](../forest_plan.md).
