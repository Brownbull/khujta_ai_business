"""
ModelDriver Demo - Simple Example

Demonstrates the ModelDriver system with a simple sales analysis example.
"""

import pandas as pd
import numpy as np
from model_driver import ModelDriver


# =========================================================================
# SAMPLE DATA
# =========================================================================

def create_sample_data():
    """Create sample sales data for testing."""
    np.random.seed(42)

    data = {
        'transaction_id': range(1, 101),
        'product': np.random.choice(['A', 'B', 'C'], 100),
        'revenue': np.random.uniform(10, 1000, 100),
        'cost': np.random.uniform(5, 500, 100),
        'quantity': np.random.randint(1, 10, 100),
    }

    df = pd.DataFrame(data)
    return df


# =========================================================================
# FEATURE DEFINITIONS (Simple Functions)
# =========================================================================

def calc_profit_margin(df):
    """Calculate profit margin percentage."""
    df['profit_margin'] = np.where(
        df['revenue'] > 0,
        ((df['revenue'] - df['cost']) / df['revenue']) * 100,
        0
    )
    return df


def calc_profit(df):
    """Calculate profit amount."""
    df['profit'] = df['revenue'] - df['cost']
    return df


def calc_price_per_unit(df):
    """Calculate price per unit."""
    df['price_per_unit'] = np.where(
        df['quantity'] > 0,
        df['revenue'] / df['quantity'],
        0
    )
    return df


def calc_total_revenue(df):
    """Calculate total revenue by product (aggregation)."""
    product_revenue = df.groupby('product')['revenue'].sum().reset_index()
    product_revenue.columns = ['product', 'total_revenue']

    # Merge back to original df
    df = df.merge(product_revenue, on='product', how='left')
    return df


def calc_avg_profit_margin(df):
    """Calculate average profit margin by product (aggregation)."""
    # This depends on profit_margin being calculated first
    product_margin = df.groupby('product')['profit_margin'].mean().reset_index()
    product_margin.columns = ['product', 'avg_profit_margin']

    # Merge back to original df
    df = df.merge(product_margin, on='product', how='left')
    return df


# =========================================================================
# DEMO SCENARIOS
# =========================================================================

def demo_basic_usage():
    """Demo 1: Basic usage with filters only."""
    print("\n" + "="*70)
    print("DEMO 1: Basic Usage - Filters Only")
    print("="*70)

    # Create driver
    driver = ModelDriver({
        'client_name': 'demo_client',
        'model_name': 'basic_demo',
        'output_base': 'data_management/',
        'save_intermediates': False  # Don't save for demo
    })

    # Register filters
    driver.register_filter('profit_margin', calc_profit_margin,
                          inputs=['revenue', 'cost'],
                          outputs=['profit_margin'],
                          description='Calculate profit margin percentage')

    driver.register_filter('profit', calc_profit,
                          inputs=['revenue', 'cost'],
                          outputs=['profit'],
                          description='Calculate profit amount')

    driver.register_filter('price_per_unit', calc_price_per_unit,
                          inputs=['revenue', 'quantity'],
                          outputs=['price_per_unit'],
                          description='Calculate price per unit')

    # Set desired outputs
    driver.set_output_attributes(['profit_margin', 'price_per_unit'])

    # Show required inputs
    required = driver.get_required_inputs()
    print(f"\nRequired inputs: {required}")

    # Execute
    df = create_sample_data()
    result = driver.execute(df)

    # Show results
    print("\nOutput DataFrame:")
    print(result['output'].head(10))
    print(f"\nShape: {result['output'].shape}")


def demo_with_dependencies():
    """Demo 2: Features with dependencies."""
    print("\n" + "="*70)
    print("DEMO 2: Features with Dependencies")
    print("="*70)

    # Create driver
    driver = ModelDriver({
        'client_name': 'demo_client',
        'model_name': 'dependency_demo',
        'output_base': 'data_management/',
        'save_intermediates': False
    })

    # Register filters (row-level)
    driver.register_filter('profit_margin', calc_profit_margin,
                          inputs=['revenue', 'cost'],
                          outputs=['profit_margin'])

    # Register attributes (aggregations)
    driver.register_attribute('total_revenue', calc_total_revenue,
                             inputs=['product', 'revenue'],
                             outputs=['total_revenue'],
                             description='Total revenue by product')

    driver.register_attribute('avg_profit_margin', calc_avg_profit_margin,
                             inputs=['product', 'profit_margin'],
                             outputs=['avg_profit_margin'],
                             depends_on=['profit_margin'],  # Depends on filter!
                             description='Average profit margin by product')

    # Set desired outputs (only the aggregations)
    driver.set_output_attributes(['total_revenue', 'avg_profit_margin'])

    # Show execution plan
    print("\nExecution Plan:")
    driver.print_execution_plan()

    # Execute
    df = create_sample_data()
    result = driver.execute(df)

    # Show results
    print("\nOutput DataFrame:")
    print(result['output'].head(10))


def demo_minimal_output():
    """Demo 3: Requesting minimal output automatically determines minimal inputs."""
    print("\n" + "="*70)
    print("DEMO 3: Minimal Output = Minimal Inputs (Key Innovation)")
    print("="*70)

    # Create driver
    driver = ModelDriver({
        'client_name': 'demo_client',
        'model_name': 'minimal_demo',
        'output_base': 'data_management/',
        'save_intermediates': False
    })

    # Register ALL features
    driver.register_filter('profit_margin', calc_profit_margin,
                          inputs=['revenue', 'cost'],
                          outputs=['profit_margin'])

    driver.register_filter('profit', calc_profit,
                          inputs=['revenue', 'cost'],
                          outputs=['profit'])

    driver.register_filter('price_per_unit', calc_price_per_unit,
                          inputs=['revenue', 'quantity'],
                          outputs=['price_per_unit'])

    driver.register_attribute('total_revenue', calc_total_revenue,
                             inputs=['product', 'revenue'],
                             outputs=['total_revenue'])

    driver.register_attribute('avg_profit_margin', calc_avg_profit_margin,
                             inputs=['product', 'profit_margin'],
                             outputs=['avg_profit_margin'],
                             depends_on=['profit_margin'])

    # Case 1: Ask for only total_revenue
    print("\nCase 1: Requesting only 'total_revenue'")
    driver.set_output_attributes(['total_revenue'])
    required = driver.get_required_inputs()
    print(f"  Required inputs: {required}")
    print(f"  Features to execute: {driver.execution_plan['required_features']}")

    # Case 2: Ask for avg_profit_margin
    print("\nCase 2: Requesting only 'avg_profit_margin'")
    driver.set_output_attributes(['avg_profit_margin'])
    required = driver.get_required_inputs()
    print(f"  Required inputs: {required}")
    print(f"  Features to execute: {driver.execution_plan['required_features']}")

    # Case 3: Ask for both
    print("\nCase 3: Requesting both 'total_revenue' and 'avg_profit_margin'")
    driver.set_output_attributes(['total_revenue', 'avg_profit_margin'])
    required = driver.get_required_inputs()
    print(f"  Required inputs: {required}")
    print(f"  Features to execute: {driver.execution_plan['required_features']}")

    # Execute final case
    df = create_sample_data()
    result = driver.execute(df)

    print("\nOutput DataFrame:")
    print(result['output'].head(10))


def demo_with_save():
    """Demo 4: Save intermediate outputs."""
    print("\n" + "="*70)
    print("DEMO 4: Staged Output with Save")
    print("="*70)

    # Create driver with save enabled
    driver = ModelDriver({
        'client_name': 'demo_client',
        'model_name': 'save_demo',
        'output_base': 'data_management/',
        'save_intermediates': True  # Enable saving
    })

    # Register features
    driver.register_filter('profit_margin', calc_profit_margin,
                          inputs=['revenue', 'cost'],
                          outputs=['profit_margin'])

    driver.register_attribute('avg_profit_margin', calc_avg_profit_margin,
                             inputs=['product', 'profit_margin'],
                             outputs=['avg_profit_margin'],
                             depends_on=['profit_margin'])

    # Set output
    driver.set_output_attributes(['avg_profit_margin'])

    # Execute
    df = create_sample_data()
    result = driver.execute(df)

    print(f"\nStaged outputs saved to:")
    print(f"  {driver.run_dir}")
    print("\nDirectory structure:")
    print("  01_preprocess/")
    print("    - preprocessed.csv")
    print("  02_features/")
    print("    - filtered.csv")
    print("  03_attributes/")
    print("    - attributes.csv")
    print("  04_output/")
    print("    - final_output.csv")
    print("  execution_metadata.json")


# =========================================================================
# RUN ALL DEMOS
# =========================================================================

if __name__ == '__main__':
    print("\n" + "="*70)
    print("MODEL DRIVER - DEMO EXAMPLES")
    print("="*70)

    demo_basic_usage()
    demo_with_dependencies()
    demo_minimal_output()
    demo_with_save()

    print("\n" + "="*70)
    print("ALL DEMOS COMPLETE")
    print("="*70)
