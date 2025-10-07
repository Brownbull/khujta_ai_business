# Feature Engine Quick Start Guide

## Installation

The feature engine is already included in the project. No installation needed!

```python
from feature_engine import feature, registry, executor
```

## 5-Minute Tutorial

### Step 1: Define Your First Feature

```python
from feature_engine import feature
import pandas as pd
import numpy as np

@feature(
    name='profit_margin',
    description='Calculate profit margin percentage',
    category='filter',  # Row-level calculation
    dtype='float',
    requires=['revenue_col', 'cost_col']
)
def calculate_profit_margin(df, config):
    """Calculate profit margin: (revenue - cost) / revenue * 100"""
    revenue_col = config['revenue_col']
    cost_col = config['cost_col']

    df['profit_margin'] = np.where(
        df[revenue_col] > 0,
        ((df[revenue_col] - df[cost_col]) / df[revenue_col]) * 100,
        0
    )
    return df
```

That's it! The feature is automatically registered.

### Step 2: Execute Your Feature

```python
from feature_engine import executor

# Your data
df = pd.DataFrame({
    'product': ['A', 'B', 'C'],
    'revenue': [100, 200, 300],
    'cost': [60, 120, 180]
})

# Your config
config = {
    'revenue_col': 'revenue',
    'cost_col': 'cost'
}

# Execute
result = executor.execute_single(df, 'profit_margin', config)

print(result[['product', 'revenue', 'cost', 'profit_margin']])
```

### Step 3: Add a Dependent Feature

```python
@feature(
    name='high_margin_flag',
    description='Flag products with margin > 30%',
    category='filter',
    dtype='boolean',
    depends_on=['profit_margin']  # Depends on profit_margin!
)
def flag_high_margin(df, config):
    """Flag high-margin products"""
    df['is_high_margin'] = df['profit_margin'] > 30
    return df
```

Execute with automatic dependency resolution:

```python
# Executor automatically runs profit_margin first, then high_margin_flag
result = executor.execute_with_dependencies(
    df,
    'high_margin_flag',
    config,
    verbose=True
)

# Output shows execution order:
# Executing 2 features...
# Order: profit_margin -> high_margin_flag
#   * Executing: profit_margin (filter)... [OK]
#   * Executing: high_margin_flag (filter)... [OK]
```

### Step 4: Introspect Features

```python
from feature_engine import registry

# See what's available
print(f"Total features: {len(registry)}")
print(f"Filters: {registry.count('filter')}")

# Get feature info
info = registry.introspect('profit_margin')
print(f"Description: {info['description']}")
print(f"Requires: {info['requires']}")

# Search features
results = registry.search('margin')
print(f"Found {len(results)} features matching 'margin'")
```

## Common Patterns

### Pattern 1: Simple Row-Level Calculation

```python
@feature(
    name='price_per_unit',
    description='Calculate price per unit',
    category='filter',
    dtype='float',
    requires=['revenue_col', 'quantity_col']
)
def calculate_price_per_unit(df, config):
    df['price_per_unit'] = df[config['revenue_col']] / df[config['quantity_col']]
    return df
```

### Pattern 2: Feature with Dependencies

```python
@feature(
    name='discount_amount',
    description='Calculate discount amount',
    category='filter',
    dtype='float',
    depends_on=['price_per_unit']  # Uses price_per_unit column
)
def calculate_discount(df, config):
    # price_per_unit column is guaranteed to exist
    df['discount_amount'] = df['original_price'] - df['price_per_unit']
    return df
```

### Pattern 3: Aggregation Attribute

```python
@feature(
    name='revenue_by_product',
    description='Total revenue per product',
    category='attribute',  # Aggregation
    dtype='dataframe',
    requires=['product_col', 'revenue_col'],
    is_aggregation=True
)
def aggregate_revenue(df, config):
    return df.groupby(config['product_col'])[config['revenue_col']].sum()
```

### Pattern 4: Optional Requirements

```python
@feature(
    name='profit_with_tax',
    description='Calculate profit including tax if available',
    category='filter',
    dtype='float',
    requires=['revenue_col'],
    optional_requires=['tax_col']  # Optional
)
def calculate_profit_with_tax(df, config):
    profit = df[config['revenue_col']]

    # Check if optional tax column is available
    if 'tax_col' in config and config['tax_col'] in df.columns:
        profit = profit - df[config['tax_col']]

    df['profit_after_tax'] = profit
    return df
```

## Validation and Debugging

### Validate Before Execution

```python
# Check if feature can be executed
is_valid, errors = executor.validate_inputs(
    ['profit_margin'],
    config,
    df
)

if not is_valid:
    print("Validation errors:")
    for error in errors:
        print(f"  - {error}")
```

### Dry Run

```python
# See execution plan without running
plan = executor.dry_run(['profit_margin', 'high_margin_flag'], config, df)

print(f"Valid: {plan['is_valid']}")
print(f"Execution order: {plan['execution_order']}")
print(f"Total features: {plan['total_features']}")
```

### View Dependencies

```python
# Get dependencies for a feature
deps = registry.get_dependencies('high_margin_flag', recursive=True)
print(f"Dependencies: {deps}")

# Get execution order for multiple features
order = registry.get_execution_order(['feature1', 'feature2', 'feature3'])
print(f"Will execute in order: {order}")
```

## Integration with Existing Code

### Use with Config Dictionary

The feature engine works seamlessly with your existing config:

```python
config = {
    'project_name': 'my_project',
    'date_col': 'fecha',
    'product_col': 'producto',
    'revenue_col': 'total',
    'quantity_col': 'cantidad',
    'transaction_col': 'trans_id'
}

# Features use the same config
result = executor.execute_single(df, 'my_feature', config)
```

### Execute Multiple Features

```python
# Execute several features at once
features_to_run = ['profit_margin', 'price_per_unit', 'high_margin_flag']

result = executor.execute(
    df,
    features_to_run,
    config,
    verbose=True
)
```

### Execute by Category

```python
# Execute all filters
result = executor.execute_by_category(
    df,
    category='filter',
    config=config
)

# Execute specific filters only
result = executor.execute_by_category(
    df,
    category='filter',
    config=config,
    feature_names=['profit_margin', 'price_per_unit']
)
```

## Tips and Best Practices

### 1. Name Features Clearly
```python
# Good
@feature(name='profit_margin', ...)

# Bad
@feature(name='pm', ...)
```

### 2. Write Descriptive Descriptions
```python
# Good
description='Calculate profit margin as (revenue - cost) / revenue * 100'

# Bad
description='Margin calc'
```

### 3. Declare All Dependencies
```python
@feature(
    name='my_feature',
    depends_on=['feature_a', 'feature_b']  # Be explicit!
)
```

### 4. Add Tags for Organization
```python
@feature(
    name='profit_margin',
    tags=['financial', 'profitability', 'kpi']  # Helps with discovery
)
```

### 5. Handle Missing Optional Inputs
```python
@feature(
    name='my_feature',
    optional_requires=['optional_col']
)
def my_feature(df, config):
    if 'optional_col' in config:
        # Use optional column
        pass
    else:
        # Graceful fallback
        pass
    return df
```

## Troubleshooting

### "Feature not found in registry"
Make sure the feature is imported and decorated before execution:
```python
from my_features import calculate_profit_margin  # Import to register
```

### "Circular dependency detected"
Check your `depends_on` declarations:
```python
# Feature A depends on B
# Feature B depends on A
# = Circular dependency!
```

### "Missing required config keys"
Ensure all required keys are in config:
```python
@feature(requires=['revenue_col', 'cost_col'], ...)
def my_feature(df, config):
    # config MUST have 'revenue_col' and 'cost_col'
    pass
```

## Next Steps

1. **Read the README**: [feature_engine/README.md](../feature_engine/README.md)
2. **See Examples**: Run `python test_feature_engine_simple.py`
3. **View Migration Guide**: [feature_engine/example_migration.py](../feature_engine/example_migration.py)
4. **Check Summary**: [FEATURE_ENGINE_SUMMARY.md](FEATURE_ENGINE_SUMMARY.md)

## Quick Reference Card

```python
# Define feature
@feature(name='my_feature', category='filter', dtype='float',
         requires=['col1'], depends_on=['other_feature'])
def my_feature(df, config): return df

# Execute single
executor.execute_single(df, 'my_feature', config)

# Execute with dependencies
executor.execute_with_dependencies(df, 'my_feature', config)

# Execute multiple
executor.execute(df, ['feature1', 'feature2'], config)

# Introspect
info = registry.introspect('my_feature')

# Search
results = registry.search('profit')

# Validate
is_valid, errors = executor.validate_inputs(['my_feature'], config, df)

# Get dependencies
deps = registry.get_dependencies('my_feature', recursive=True)

# Dry run
plan = executor.dry_run(['my_feature'], config, df)
```

---

**Ready to start?** Try running `python test_feature_engine_simple.py` to see it in action!
