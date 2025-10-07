"""
Example Migration: Old Pattern → New Feature Engine Pattern

This file demonstrates how to migrate from the hardcoded filter/attribute
methods to the new dynamic feature store approach.
"""

import pandas as pd
import numpy as np
from feature_engine import feature, registry, executor


# =============================================================================
# BEFORE: Old Pattern (from waterfall/scripts/filters.py)
# =============================================================================

class OldFilterEngine:
    """Old hardcoded approach"""

    def __init__(self, config):
        self.config = config

    def _filter_profit_margin(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate profit margin percentage"""
        revenue_col = self.config['revenue_col']
        cost_col = self.config.get('cost_col')

        if cost_col and cost_col in df.columns:
            df['profit_margin'] = np.where(
                df[revenue_col] > 0,
                ((df[revenue_col] - df[cost_col]) / df[revenue_col]) * 100,
                0
            )
            df['profit'] = df[revenue_col] - df[cost_col]

        return df

    def _filter_price_per_unit(self, df: pd.DataFrame) -> pd.DataFrame:
        """Calculate price per unit"""
        revenue_col = self.config['revenue_col']
        quantity_col = self.config['quantity_col']

        df['price_per_unit'] = np.where(
            df[quantity_col] > 0,
            df[revenue_col] / df[quantity_col],
            0
        )

        return df


# =============================================================================
# AFTER: New Pattern (with @feature decorator)
# =============================================================================

@feature(
    name='profit_margin',
    description='Profit margin percentage calculated as (revenue - cost) / revenue * 100',
    category='filter',
    dtype='float',
    requires=['revenue_col', 'cost_col'],
    optional_requires=['cost_col'],
    tags=['financial', 'profitability'],
    version='1.0.0',
    author='Business Analytics Team'
)
def calculate_profit_margin(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """
    Calculate profit margin percentage.

    Creates two new columns:
    - profit_margin: Percentage margin
    - profit: Absolute profit amount

    Args:
        df: Input DataFrame
        config: Configuration with revenue_col and cost_col

    Returns:
        DataFrame with profit_margin and profit columns added
    """
    revenue_col = config['revenue_col']
    cost_col = config.get('cost_col')

    if cost_col and cost_col in df.columns:
        # Profit margin = (revenue - cost) / revenue * 100
        df['profit_margin'] = np.where(
            df[revenue_col] > 0,
            ((df[revenue_col] - df[cost_col]) / df[revenue_col]) * 100,
            0
        )

        # Profit amount
        df['profit'] = df[revenue_col] - df[cost_col]
    else:
        print(f"ℹ Info: cost_col not available, skipping profit_margin calculation")

    return df


@feature(
    name='price_per_unit',
    description='Price per unit calculated as total revenue divided by quantity',
    category='filter',
    dtype='float',
    requires=['revenue_col', 'quantity_col'],
    tags=['pricing', 'unit_economics'],
    version='1.0.0'
)
def calculate_price_per_unit(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """
    Calculate price per unit.

    Args:
        df: Input DataFrame
        config: Configuration with revenue_col and quantity_col

    Returns:
        DataFrame with price_per_unit column added
    """
    revenue_col = config['revenue_col']
    quantity_col = config['quantity_col']

    # Price per unit = revenue / quantity
    df['price_per_unit'] = np.where(
        df[quantity_col] > 0,
        df[revenue_col] / df[quantity_col],
        0
    )

    return df


@feature(
    name='discount_percentage',
    description='Discount percentage relative to average product price',
    category='filter',
    dtype='float',
    requires=['product_col'],
    depends_on=['price_per_unit'],  # Must calculate price_per_unit first!
    tags=['pricing', 'discounts'],
    version='1.0.0'
)
def calculate_discount_percentage(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """
    Calculate discount percentage for each transaction.

    This feature DEPENDS on price_per_unit being calculated first.
    The executor will automatically handle this dependency.

    Args:
        df: Input DataFrame (must have price_per_unit column)
        config: Configuration with product_col

    Returns:
        DataFrame with discount_pct column added
    """
    product_col = config['product_col']

    # Calculate average price per product
    avg_prices = df.groupby(product_col)['price_per_unit'].mean()

    # Map average price to each row
    df['avg_product_price'] = df[product_col].map(avg_prices)

    # Calculate discount percentage
    df['discount_pct'] = np.where(
        df['avg_product_price'] > 0,
        ((df['avg_product_price'] - df['price_per_unit']) / df['avg_product_price']) * 100,
        0
    )

    # Flag if discounted
    df['has_discount'] = df['price_per_unit'] < (df['avg_product_price'] * 0.9)

    return df


# =============================================================================
# Example Attribute (Aggregation)
# =============================================================================

@feature(
    name='product_metrics',
    description='Aggregated metrics per product',
    category='attribute',
    dtype='dataframe',
    requires=['product_col', 'description_col', 'revenue_col', 'quantity_col', 'transaction_col'],
    tags=['products', 'aggregation'],
    is_aggregation=True,
    version='1.0.0'
)
def calculate_product_metrics(df: pd.DataFrame, config: dict) -> pd.DataFrame:
    """
    Calculate aggregated product-level metrics.

    Args:
        df: Input DataFrame
        config: Configuration dict

    Returns:
        DataFrame with product metrics
    """
    product_col = config['product_col']
    revenue_col = config['revenue_col']
    quantity_col = config['quantity_col']
    transaction_col = config['transaction_col']
    description_col = config['description_col']

    # Aggregate by product
    product_metrics = df.groupby(product_col).agg({
        description_col: 'first',
        revenue_col: 'sum',
        quantity_col: 'sum',
        transaction_col: 'nunique'
    }).rename(columns={
        description_col: 'description',
        revenue_col: 'total_revenue',
        quantity_col: 'total_quantity',
        transaction_col: 'transaction_count'
    })

    # Sort by revenue
    product_metrics = product_metrics.sort_values('total_revenue', ascending=False)

    return product_metrics


# =============================================================================
# USAGE COMPARISON
# =============================================================================

def demo_old_pattern():
    """Demonstrate old pattern usage"""
    print("\n" + "="*70)
    print("OLD PATTERN (Hardcoded)")
    print("="*70)

    # Create sample data
    df = pd.DataFrame({
        'producto': ['A', 'B', 'C'],
        'total': [100, 200, 300],
        'costo': [60, 120, 180],
        'cantidad': [2, 4, 6]
    })

    config = {
        'revenue_col': 'total',
        'cost_col': 'costo',
        'quantity_col': 'cantidad'
    }

    # Old way: Manual method calls
    engine = OldFilterEngine(config)
    df = engine._filter_profit_margin(df)
    df = engine._filter_price_per_unit(df)

    print("\nResult:")
    print(df[['producto', 'profit_margin', 'price_per_unit']])

    # Problems with old pattern:
    # ❌ No way to know what inputs are required
    # ❌ No automatic dependency resolution
    # ❌ Hard to discover available features
    # ❌ Manual execution order management


def demo_new_pattern():
    """Demonstrate new pattern usage"""
    print("\n" + "="*70)
    print("NEW PATTERN (Dynamic Feature Engine)")
    print("="*70)

    # Create sample data
    df = pd.DataFrame({
        'producto': ['A', 'B', 'C', 'A', 'B'],
        'total': [100, 200, 300, 110, 190],
        'costo': [60, 120, 180, 65, 115],
        'cantidad': [2, 4, 6, 2, 4],
        'trans_id': ['T1', 'T2', 'T3', 'T4', 'T5']
    })

    config = {
        'revenue_col': 'total',
        'cost_col': 'costo',
        'quantity_col': 'cantidad',
        'product_col': 'producto'
    }

    # New way: Automatic execution with dependency resolution

    # 1. Introspect available features
    print("\n1. Available Features:")
    print(f"   Total: {len(registry)} features")
    print(f"   Filters: {registry.count('filter')}")
    print(f"   Attributes: {registry.count('attribute')}")

    # 2. Understand a specific feature
    print("\n2. Feature Details:")
    info = registry.introspect('profit_margin')
    print(f"   Name: {info['name']}")
    print(f"   Requires: {info['requires']}")
    print(f"   Dependencies: {info['depends_on']}")

    # 3. Execute with automatic dependency resolution
    print("\n3. Execute with Dependencies:")
    # This will automatically execute price_per_unit first, then discount_percentage
    result_df = executor.execute_with_dependencies(
        df,
        'discount_percentage',  # This depends on 'price_per_unit'
        config,
        verbose=True
    )

    print("\nResult:")
    print(result_df[['producto', 'price_per_unit', 'discount_pct', 'has_discount']].head())

    # 4. Dry run to see execution plan
    print("\n4. Dry Run (Execution Plan):")
    plan = executor.dry_run(['profit_margin', 'discount_percentage'], config, df)
    print(f"   Valid: {plan['is_valid']}")
    print(f"   Execution Order: {' → '.join(plan['execution_order'])}")

    # Benefits of new pattern:
    # ✅ Self-documenting: Each feature declares requirements
    # ✅ Automatic dependency resolution
    # ✅ Runtime introspection
    # ✅ Validation before execution
    # ✅ Easy to add new features


if __name__ == '__main__':
    print("\n" + "="*70)
    print("FEATURE ENGINE MIGRATION EXAMPLE")
    print("="*70)

    # Show old pattern
    demo_old_pattern()

    # Show new pattern
    demo_new_pattern()

    print("\n" + "="*70)
    print("MIGRATION COMPLETE")
    print("="*70)
    print("\nKey Improvements:")
    print("  ✅ Declarative feature definitions")
    print("  ✅ Automatic dependency resolution")
    print("  ✅ Runtime introspection and discovery")
    print("  ✅ Input validation")
    print("  ✅ Self-documenting code")
    print("  ✅ Easy to extend and test")
    print("")
