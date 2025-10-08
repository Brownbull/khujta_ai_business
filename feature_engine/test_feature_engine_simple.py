"""
Simple Test for Feature Engine
"""

import pandas as pd
import numpy as np
from feature_engine import feature, registry, executor

# Create test data
df = pd.DataFrame({
    'producto': ['A', 'B', 'C', 'A', 'B'],
    'total': [100, 200, 300, 110, 190],
    'costo': [60, 120, 180, 65, 115],
    'cantidad': [2, 4, 6, 2, 4]
})

config = {
    'revenue_col': 'total',
    'cost_col': 'costo',
    'quantity_col': 'cantidad',
    'product_col': 'producto'
}

# Define test features
@feature(
    name='profit_margin',
    description='Profit margin percentage',
    category='filter',
    dtype='float',
    requires=['revenue_col', 'cost_col']
)
def calculate_profit_margin(df, config):
    revenue_col = config['revenue_col']
    cost_col = config['cost_col']

    df['profit_margin'] = np.where(
        df[revenue_col] > 0,
        ((df[revenue_col] - df[cost_col]) / df[revenue_col]) * 100,
        0
    )
    return df

@feature(
    name='price_per_unit',
    description='Price per unit',
    category='filter',
    dtype='float',
    requires=['revenue_col', 'quantity_col']
)
def calculate_price_per_unit(df, config):
    revenue_col = config['revenue_col']
    quantity_col = config['quantity_col']

    df['price_per_unit'] = np.where(
        df[quantity_col] > 0,
        df[revenue_col] / df[quantity_col],
        0
    )
    return df

@feature(
    name='discount_check',
    description='Check for discounts',
    category='filter',
    dtype='float',
    requires=['product_col'],
    depends_on=['price_per_unit']
)
def calculate_discount(df, config):
    product_col = config['product_col']
    avg_prices = df.groupby(product_col)['price_per_unit'].mean()
    df['avg_price'] = df[product_col].map(avg_prices)
    df['discount_pct'] = ((df['avg_price'] - df['price_per_unit']) / df['avg_price']) * 100
    return df

print("="*70)
print("FEATURE ENGINE - SIMPLE TEST")
print("="*70)

# Test 1: Registry
print("\nTest 1: Registry Operations")
print(f"  Total features: {len(registry)}")
print(f"  Filter features: {registry.count('filter')}")
assert registry.exists('profit_margin'), "Feature not registered"
print("  [PASS] Registry working")

# Test 2: Introspection
print("\nTest 2: Introspection")
info = registry.introspect('profit_margin')
print(f"  Feature: {info['name']}")
print(f"  Requires: {info['requires']}")
print("  [PASS] Introspection working")

# Test 3: Dependencies
print("\nTest 3: Dependency Resolution")
deps = registry.get_dependencies('discount_check', recursive=True)
print(f"  Dependencies for 'discount_check': {deps}")
assert 'price_per_unit' in deps, "Dependency not found"
print("  [PASS] Dependencies resolved")

# Test 4: Execution Order
print("\nTest 4: Execution Order")
order = registry.get_execution_order(['discount_check', 'profit_margin'])
print(f"  Execution order: {order}")
assert order.index('price_per_unit') < order.index('discount_check'), "Wrong order"
print("  [PASS] Execution order correct")

# Test 5: Validation
print("\nTest 5: Input Validation")
is_valid, errors = executor.validate_inputs(['profit_margin'], config, df)
print(f"  Valid: {is_valid}")
if errors:
    print(f"  Errors: {errors}")
assert is_valid, "Validation failed"
print("  [PASS] Validation working")

# Test 6: Feature Execution
print("\nTest 6: Feature Execution")
result = executor.execute_single(df, 'profit_margin', config, verbose=False)
assert 'profit_margin' in result.columns, "Column not created"
print(f"  Columns created: {[c for c in result.columns if c not in df.columns]}")
print("  [PASS] Feature execution working")

# Test 7: Dependency Execution
print("\nTest 7: Execution with Dependencies")
result = executor.execute_with_dependencies(df, 'discount_check', config, verbose=True)
assert 'price_per_unit' in result.columns, "Dependency not executed"
assert 'discount_pct' in result.columns, "Feature not executed"
print("  [PASS] Dependency execution working")

print("\n" + "="*70)
print("ALL TESTS PASSED!")
print("="*70)
print(f"\nFinal Result Columns: {list(result.columns)}")
print("\nSample Data:")
print(result[['producto', 'total', 'price_per_unit', 'discount_pct']].head())
