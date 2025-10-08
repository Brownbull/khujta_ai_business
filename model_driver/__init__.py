"""
ModelDriver - Simplified Feature Calculation Engine

A lightweight, flexible system for defining and executing data transformations
with automatic dependency resolution and staged output management.

Key Features:
- Simple function-based feature definition (no complex decorators)
- Dynamic output selection with automatic input resolution
- Staged pipeline execution (preprocess → filters → attributes → output)
- Minimal boilerplate, maximum flexibility

Example Usage:
    from model_driver import ModelDriver

    # Create driver
    driver = ModelDriver({
        'client_name': 'my_client',
        'model_name': 'my_model',
        'output_base': 'data_management/'
    })

    # Register a filter (simple function)
    def profit_margin(df):
        df['profit_margin'] = (df['revenue'] - df['cost']) / df['revenue'] * 100
        return df

    driver.register_filter('profit_margin', profit_margin,
                          inputs=['revenue', 'cost'],
                          outputs=['profit_margin'])

    # Set desired outputs
    driver.set_output_attributes(['profit_margin'])

    # Get required inputs
    required = driver.get_required_inputs()
    # ['revenue', 'cost']

    # Execute
    result = driver.execute(df)
"""

from model_driver.driver import ModelDriver
from model_driver.feature_simple import FeatureRegistry, FeatureMetadata
from model_driver.resolver import DependencyResolver, validate_feature_dependencies

__all__ = [
    'ModelDriver',
    'FeatureRegistry',
    'FeatureMetadata',
    'DependencyResolver',
    'validate_feature_dependencies'
]
__version__ = '1.0.0'
