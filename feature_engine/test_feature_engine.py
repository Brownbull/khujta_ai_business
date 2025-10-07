"""
Test Suite for Feature Engine

Tests all core functionality of the feature engine.
"""

import pandas as pd
import numpy as np
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from feature_engine import feature, registry, executor
from feature_engine.metadata import FeatureCategory, DataType
from feature_engine.introspection import (
    get_feature_catalog,
    get_dependency_tree,
    get_statistics,
    validate_registry
)


def create_test_data():
    """Create sample test data"""
    return pd.DataFrame({
        'producto': ['A', 'B', 'C', 'A', 'B', 'C'],
        'glosa': ['Product A', 'Product B', 'Product C'] * 2,
        'total': [100, 200, 300, 110, 190, 310],
        'costo': [60, 120, 180, 65, 115, 185],
        'cantidad': [2, 4, 6, 2, 4, 6],
        'trans_id': ['T1', 'T2', 'T3', 'T4', 'T5', 'T6'],
        'fecha': pd.date_range('2024-01-01', periods=6)
    })


def create_test_config():
    """Create sample config"""
    return {
        'project_name': 'test',
        'revenue_col': 'total',
        'cost_col': 'costo',
        'quantity_col': 'cantidad',
        'product_col': 'producto',
        'description_col': 'glosa',
        'transaction_col': 'trans_id',
        'date_col': 'fecha'
    }


# =============================================================================
# TEST FEATURES
# =============================================================================

@feature(
    name='test_profit_margin',
    description='Test profit margin calculation',
    category='filter',
    dtype='float',
    requires=['revenue_col', 'cost_col'],
    tags=['test', 'financial']
)
def test_calculate_profit_margin(df, config):
    """Calculate profit margin for testing"""
    revenue_col = config['revenue_col']
    cost_col = config['cost_col']

    df['profit_margin'] = np.where(
        df[revenue_col] > 0,
        ((df[revenue_col] - df[cost_col]) / df[revenue_col]) * 100,
        0
    )
    df['profit'] = df[revenue_col] - df[cost_col]

    return df


@feature(
    name='test_price_per_unit',
    description='Test price per unit calculation',
    category='filter',
    dtype='float',
    requires=['revenue_col', 'quantity_col'],
    tags=['test', 'pricing']
)
def test_calculate_price_per_unit(df, config):
    """Calculate price per unit for testing"""
    revenue_col = config['revenue_col']
    quantity_col = config['quantity_col']

    df['price_per_unit'] = np.where(
        df[quantity_col] > 0,
        df[revenue_col] / df[quantity_col],
        0
    )

    return df


@feature(
    name='test_discount',
    description='Test discount calculation with dependency',
    category='filter',
    dtype='float',
    requires=['product_col'],
    depends_on=['test_price_per_unit'],  # Dependency!
    tags=['test', 'pricing']
)
def test_calculate_discount(df, config):
    """Calculate discount (depends on price_per_unit)"""
    product_col = config['product_col']

    # Calculate average price per product
    avg_prices = df.groupby(product_col)['price_per_unit'].mean()
    df['avg_product_price'] = df[product_col].map(avg_prices)

    # Discount percentage
    df['discount_pct'] = np.where(
        df['avg_product_price'] > 0,
        ((df['avg_product_price'] - df['price_per_unit']) / df['avg_product_price']) * 100,
        0
    )

    return df


@feature(
    name='test_product_metrics',
    description='Test product aggregation',
    category='attribute',
    dtype='dataframe',
    requires=['product_col', 'description_col', 'revenue_col', 'quantity_col'],
    is_aggregation=True,
    tags=['test', 'aggregation']
)
def test_aggregate_products(df, config):
    """Aggregate product metrics for testing"""
    product_col = config['product_col']
    revenue_col = config['revenue_col']
    quantity_col = config['quantity_col']
    description_col = config['description_col']

    result = df.groupby(product_col).agg({
        description_col: 'first',
        revenue_col: 'sum',
        quantity_col: 'sum'
    }).rename(columns={
        description_col: 'description',
        revenue_col: 'total_revenue',
        quantity_col: 'total_quantity'
    })

    return result


# =============================================================================
# TESTS
# =============================================================================

def test_1_registry_operations():
    """Test registry operations"""
    print("\n" + "="*70)
    print("TEST 1: Registry Operations")
    print("="*70)

    # Check features are registered
    assert registry.exists('test_profit_margin'), "Feature not registered"
    assert registry.exists('test_price_per_unit'), "Feature not registered"
    print("✓ Features registered")

    # Get feature
    feature_meta = registry.get('test_profit_margin')
    assert feature_meta is not None, "Feature not found"
    assert feature_meta.name == 'test_profit_margin', "Wrong feature name"
    print("✓ Feature retrieval works")

    # Get by category
    filters = registry.get_by_category('filter')
    assert len(filters) > 0, "No filters found"
    print(f"✓ Found {len(filters)} filter features")

    # Get by tag
    test_features = registry.get_by_tag('test')
    assert len(test_features) > 0, "No test features found"
    print(f"✓ Found {len(test_features)} test features")

    # Search
    results = registry.search('profit')
    assert len(results) > 0, "Search failed"
    print(f"✓ Search found {len(results)} features")

    print("\n✅ All registry tests passed")


def test_2_dependency_resolution():
    """Test dependency resolution"""
    print("\n" + "="*70)
    print("TEST 2: Dependency Resolution")
    print("="*70)

    # Get dependencies
    deps = registry.get_dependencies('test_discount', recursive=True)
    assert 'test_price_per_unit' in deps, "Dependency not found"
    print(f"✓ Dependencies resolved: {deps}")

    # Get execution order
    order = registry.get_execution_order(['test_discount', 'test_profit_margin'])
    print(f"✓ Execution order: {order}")

    # Validate dependencies
    is_valid, missing = registry.validate_dependencies('test_discount')
    assert is_valid, f"Dependencies invalid: {missing}"
    print("✓ Dependencies valid")

    print("\n✅ All dependency tests passed")


def test_3_executor_validation():
    """Test executor validation"""
    print("\n" + "="*70)
    print("TEST 3: Executor Validation")
    print("="*70)

    df = create_test_data()
    config = create_test_config()

    # Validate inputs
    is_valid, errors = executor.validate_inputs(
        ['test_profit_margin', 'test_price_per_unit'],
        config,
        df
    )
    assert is_valid, f"Validation failed: {errors}"
    print("✓ Input validation passed")

    # Dry run
    plan = executor.dry_run(['test_profit_margin'], config, df)
    assert plan['is_valid'], "Dry run validation failed"
    assert len(plan['execution_order']) > 0, "Empty execution order"
    print(f"✓ Dry run passed: {plan['execution_order']}")

    print("\n✅ All validation tests passed")


def test_4_feature_execution():
    """Test feature execution"""
    print("\n" + "="*70)
    print("TEST 4: Feature Execution")
    print("="*70)

    df = create_test_data()
    config = create_test_config()

    # Execute single feature
    result = executor.execute_single(
        df,
        'test_profit_margin',
        config,
        verbose=False
    )
    assert 'profit_margin' in result.columns, "Column not created"
    assert 'profit' in result.columns, "Column not created"
    print("✓ Single feature execution works")

    # Execute multiple features
    result = executor.execute(
        df,
        ['test_profit_margin', 'test_price_per_unit'],
        config,
        verbose=False
    )
    assert 'profit_margin' in result.columns, "Column not created"
    assert 'price_per_unit' in result.columns, "Column not created"
    print("✓ Multiple feature execution works")

    # Execute with dependencies
    result = executor.execute_with_dependencies(
        df,
        'test_discount',  # Depends on test_price_per_unit
        config,
        verbose=False
    )
    assert 'price_per_unit' in result.columns, "Dependency not executed"
    assert 'discount_pct' in result.columns, "Feature not executed"
    print("✓ Dependency execution works")

    # Execute by category
    result = executor.execute_by_category(
        df,
        'filter',
        config,
        feature_names=['test_profit_margin', 'test_price_per_unit'],
        verbose=False
    )
    assert isinstance(result, pd.DataFrame), "Wrong result type"
    print("✓ Category execution works")

    print("\n✅ All execution tests passed")


def test_5_introspection():
    """Test introspection tools"""
    print("\n" + "="*70)
    print("TEST 5: Introspection")
    print("="*70)

    # Get catalog
    catalog = get_feature_catalog(registry, format='dict')
    assert 'features' in catalog, "Catalog missing features"
    print(f"✓ Catalog generated: {catalog['total_features']} features")

    # Get dependency tree
    tree = get_dependency_tree(registry, 'test_discount', format='dict')
    assert tree['name'] == 'test_discount', "Wrong tree root"
    print("✓ Dependency tree generated")

    # Get statistics
    stats = get_statistics(registry)
    assert stats['total_features'] > 0, "No features in stats"
    print(f"✓ Statistics: {stats['total_features']} features, {len(stats['by_category'])} categories")

    # Validate registry
    is_valid, issues = validate_registry(registry)
    if not is_valid:
        print(f"⚠ Registry validation issues: {issues}")
    else:
        print("✓ Registry validation passed")

    print("\n✅ All introspection tests passed")


def test_6_error_handling():
    """Test error handling"""
    print("\n" + "="*70)
    print("TEST 6: Error Handling")
    print("="*70)

    df = create_test_data()
    config = create_test_config()

    # Test missing feature
    try:
        executor.execute_single(df, 'nonexistent_feature', config, verbose=False)
        assert False, "Should have raised error"
    except ValueError:
        print("✓ Missing feature error caught")

    # Test missing config key
    bad_config = {'revenue_col': 'total'}  # Missing other required keys
    is_valid, errors = executor.validate_inputs(
        ['test_profit_margin'],
        bad_config,
        df
    )
    assert not is_valid, "Should have detected missing config"
    print("✓ Missing config error caught")

    # Test circular dependency (would need to create one)
    print("✓ Error handling works")

    print("\n✅ All error handling tests passed")


def test_7_aggregation_features():
    """Test aggregation features"""
    print("\n" + "="*70)
    print("TEST 7: Aggregation Features")
    print("="*70)

    df = create_test_data()
    config = create_test_config()

    # Execute aggregation
    result = executor.execute_single(
        df,
        'test_product_metrics',
        config,
        verbose=False
    )

    # Result should be a dict with the aggregation result
    assert isinstance(result, (dict, pd.DataFrame)), "Wrong result type for aggregation"
    print("✓ Aggregation execution works")

    print("\n✅ All aggregation tests passed")


def run_all_tests():
    """Run all tests"""
    print("\n" + "="*80)
    print("FEATURE ENGINE TEST SUITE")
    print("="*80)

    try:
        test_1_registry_operations()
        test_2_dependency_resolution()
        test_3_executor_validation()
        test_4_feature_execution()
        test_5_introspection()
        test_6_error_handling()
        test_7_aggregation_features()

        print("\n" + "="*80)
        print("✅ ALL TESTS PASSED")
        print("="*80)
        print(f"\nRegistry: {len(registry)} features")
        print(f"  Filters: {registry.count('filter')}")
        print(f"  Attributes: {registry.count('attribute')}")
        print(f"  Tags: {len(registry.get_tags())}")
        print("")

        return True

    except AssertionError as e:
        print("\n" + "="*80)
        print("❌ TEST FAILED")
        print("="*80)
        print(f"Error: {str(e)}")
        return False

    except Exception as e:
        print("\n" + "="*80)
        print("❌ UNEXPECTED ERROR")
        print("="*80)
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = run_all_tests()
    sys.exit(0 if success else 1)
