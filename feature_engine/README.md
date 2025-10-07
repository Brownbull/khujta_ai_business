# Feature Engine

A **dynamic, self-documenting feature store** for business analytics that provides declarative feature definitions with automatic dependency resolution.

## Overview

The Feature Engine transforms hardcoded calculation methods into a flexible, discoverable system where:

- ✅ **Features are self-documenting** - Each feature declares its inputs, outputs, and dependencies
- ✅ **Dependencies are auto-resolved** - No need to manually manage execution order
- ✅ **Runtime introspection** - Discover available features and their requirements
- ✅ **Easy to extend** - Add features by decorating functions
- ✅ **Input validation** - Validate before execution to catch errors early

## Architecture

```
feature_engine/
├── metadata.py          # FeatureMetadata class
├── decorators.py        # @feature decorator
├── registry.py          # FeatureRegistry for storage & discovery
├── executor.py          # FeatureExecutor for execution
├── introspection.py     # Runtime inspection tools
└── example_migration.py # Migration examples
```

## Quick Start

### 1. Define a Feature

```python
from feature_engine import feature

@feature(
    name='profit_margin',
    description='Profit margin percentage',
    category='filter',  # 'filter', 'attribute', 'score'
    dtype='float',
    requires=['revenue_col', 'cost_col'],
    tags=['financial', 'profitability']
)
def calculate_profit_margin(df, config):
    revenue_col = config['revenue_col']
    cost_col = config['cost_col']

    df['profit_margin'] = ((df[revenue_col] - df[cost_col]) / df[revenue_col]) * 100
    return df
```

### 2. Execute Features

```python
from feature_engine import executor

# Execute with automatic dependency resolution
result_df = executor.execute_with_dependencies(
    df,
    'profit_margin',
    config
)
```

### 3. Introspect Features

```python
from feature_engine import registry

# Get all features
all_features = registry.get_all()

# Get features by category
filters = registry.get_by_category('filter')

# Get feature info
info = registry.introspect('profit_margin')
# Returns: {
#   'name': 'profit_margin',
#   'requires': ['revenue_col', 'cost_col'],
#   'depends_on': [],
#   'description': 'Profit margin percentage',
#   ...
# }
```

## Feature Decorator

### Basic Usage

```python
@feature(
    name='feature_name',           # Required: Unique identifier
    description='What it does',    # Required: Human-readable description
    category='filter',             # Required: 'filter', 'attribute', 'score', 'preprocessing'
    dtype='float',                 # Required: Output data type
    requires=['config_key'],       # Required config keys or columns
    depends_on=['other_feature'],  # Features that must run first
    optional_requires=['opt_key'], # Optional config keys
    tags=['tag1', 'tag2'],        # Tags for categorization
    version='1.0.0'               # Feature version
)
def my_feature(df, config):
    # Your calculation logic
    return df  # or return results dict
```

### Feature Categories

- **`filter`**: Row-level calculations (no aggregation). Returns modified DataFrame.
- **`attribute`**: Aggregated metrics. Returns results dict or DataFrame.
- **`score`**: Scoring and insights. Returns results dict.
- **`preprocessing`**: Data cleaning and validation. Returns modified DataFrame.

### Dependencies

Features can depend on other features:

```python
@feature(
    name='discount_percentage',
    category='filter',
    dtype='float',
    depends_on=['price_per_unit']  # Must run after price_per_unit
)
def calculate_discount(df, config):
    # Can use price_per_unit column created by dependency
    df['discount_pct'] = ...
    return df
```

The executor automatically resolves dependencies and executes in correct order.

## Registry Operations

### Registration

Features are auto-registered when decorated:

```python
@feature(name='my_feature', ...)
def my_feature(df, config):
    pass

# Auto-registered in global registry
```

Manual registration:

```python
from feature_engine import registry
from feature_engine.metadata import FeatureMetadata

metadata = FeatureMetadata(
    name='my_feature',
    function=my_function,
    ...
)
registry.register(metadata)
```

### Discovery

```python
# Check if feature exists
if registry.exists('profit_margin'):
    print("Feature available")

# Get feature names
all_names = registry.get_feature_names()
filter_names = registry.get_feature_names(category='filter')

# Search features
results = registry.search('profit', search_in=['name', 'description'])

# Get dependencies
deps = registry.get_dependencies('my_feature', recursive=True)

# Get execution order
order = registry.get_execution_order(['feature1', 'feature2'])
```

## Executor Operations

### Execute Features

```python
from feature_engine import executor

# Execute single feature
result = executor.execute_single(df, 'profit_margin', config)

# Execute multiple features
result = executor.execute(df, ['feature1', 'feature2'], config)

# Execute with dependencies (recommended)
result = executor.execute_with_dependencies(df, 'my_feature', config)

# Execute by category
result = executor.execute_by_category(df, 'filter', config)
```

### Validation

```python
# Validate before execution
is_valid, errors = executor.validate_inputs(
    ['feature1', 'feature2'],
    config,
    df
)

if not is_valid:
    for error in errors:
        print(error)

# Dry run (no execution)
plan = executor.dry_run(['feature1', 'feature2'], config, df)
print(f"Execution order: {plan['execution_order']}")
print(f"Valid: {plan['is_valid']}")
```

## Introspection

### Feature Catalog

```python
from feature_engine.introspection import get_feature_catalog

# Get catalog as dict
catalog = get_feature_catalog(registry, format='dict')

# Get catalog as Markdown
markdown = get_feature_catalog(registry, format='markdown')

# Get catalog as plain text
text = get_feature_catalog(registry, format='text')

# Save to file
with open('feature_catalog.md', 'w') as f:
    f.write(markdown)
```

### Dependency Tree

```python
from feature_engine.introspection import get_dependency_tree

# Get dependency tree
tree = get_dependency_tree(registry, 'my_feature', format='text')
print(tree)

# Output:
# └── my_feature [filter]
#     ├── dependency1 [filter]
#     └── dependency2 [attribute]
```

### Statistics

```python
from feature_engine.introspection import print_statistics

# Print registry statistics
print_statistics(registry)

# Output:
# ==========================================
# FEATURE REGISTRY STATISTICS
# ==========================================
# Total Features: 15
#
# By Category:
#   filter         : 8 features
#   attribute      : 5 features
#   score          : 2 features
# ...
```

## Migration Guide

### From Old Pattern

**Before:**
```python
class FilterEngine:
    def _filter_profit_margin(self, df):
        df['profit_margin'] = ...
        return df
```

**After:**
```python
@feature(
    name='profit_margin',
    description='Profit margin percentage',
    category='filter',
    dtype='float',
    requires=['revenue_col', 'cost_col']
)
def calculate_profit_margin(df, config):
    df['profit_margin'] = ...
    return df
```

See [example_migration.py](example_migration.py) for complete examples.

## Best Practices

### 1. Clear Naming
- Use descriptive feature names: `profit_margin` not `pm`
- Use verb prefixes for clarity: `calculate_`, `compute_`, `aggregate_`

### 2. Complete Metadata
- Always provide meaningful descriptions
- List all required inputs in `requires`
- Declare dependencies in `depends_on`
- Add relevant tags for discovery

### 3. Validation
- Validate inputs at function start
- Handle missing optional inputs gracefully
- Return consistent data types

### 4. Dependencies
- Declare explicit dependencies, don't assume execution order
- Keep dependency chains shallow when possible
- Avoid circular dependencies

### 5. Testing
- Test features in isolation
- Test with and without optional inputs
- Test dependency resolution

## Examples

### Example 1: Simple Filter

```python
@feature(
    name='is_weekend',
    description='Flag weekend transactions',
    category='filter',
    dtype='boolean',
    requires=['date_col']
)
def flag_weekend(df, config):
    date_col = config['date_col']
    df['is_weekend'] = df[date_col].dt.dayofweek.isin([5, 6])
    return df
```

### Example 2: Feature with Dependencies

```python
@feature(
    name='price_per_unit',
    category='filter',
    dtype='float',
    requires=['revenue_col', 'quantity_col']
)
def calculate_price_per_unit(df, config):
    df['price_per_unit'] = df[config['revenue_col']] / df[config['quantity_col']]
    return df

@feature(
    name='discount_flag',
    category='filter',
    dtype='boolean',
    depends_on=['price_per_unit']  # Requires price_per_unit
)
def flag_discount(df, config):
    avg_price = df.groupby(config['product_col'])['price_per_unit'].mean()
    df['avg_price'] = df[config['product_col']].map(avg_price)
    df['has_discount'] = df['price_per_unit'] < df['avg_price'] * 0.9
    return df
```

### Example 3: Aggregation Attribute

```python
@feature(
    name='revenue_by_day',
    description='Daily revenue aggregation',
    category='attribute',
    dtype='dict',
    requires=['date_col', 'revenue_col'],
    is_aggregation=True
)
def aggregate_daily_revenue(df, config):
    daily = df.groupby(pd.Grouper(key=config['date_col'], freq='D'))
    return {
        'daily_revenue': daily[config['revenue_col']].sum().to_dict(),
        'daily_transactions': daily[config['transaction_col']].count().to_dict()
    }
```

## API Reference

See docstrings in each module for detailed API documentation:

- `metadata.py` - FeatureMetadata, FeatureCategory, DataType
- `decorators.py` - @feature decorator and variants
- `registry.py` - FeatureRegistry operations
- `executor.py` - FeatureExecutor operations
- `introspection.py` - Introspection and documentation tools

## Contributing

To add new features:

1. Define feature with `@feature` decorator
2. Test feature in isolation
3. Update feature catalog: `python -m feature_engine.introspection`
4. Document in relevant module

## License

Part of the Business Analytics Engine project.
