"""
Feature Engine - Dynamic Feature Store for Business Analytics

A self-documenting, dependency-aware feature calculation engine that allows
declarative feature definitions with automatic execution ordering.

Key Components:
- FeatureMetadata: Feature definition with metadata
- FeatureRegistry: Central registry for all features
- FeatureExecutor: Executes features with dependency resolution
- @feature decorator: Easy feature registration

Example Usage:
    from feature_engine import feature, registry, executor

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
        df['profit_margin'] = ((df[revenue_col] - df[cost_col]) / df[revenue_col]) * 100
        return df

    # Execute with automatic dependency resolution
    result = executor.execute_with_dependencies(df, 'profit_margin', config)

    # Introspect available features
    all_features = registry.get_all_features()
    filter_features = registry.get_all_features(category='filter')

    # Get feature info
    info = registry.introspect('profit_margin')
"""

from feature_engine.metadata import FeatureMetadata
from feature_engine.decorators import feature
from feature_engine.registry import FeatureRegistry
from feature_engine.executor import FeatureExecutor
from feature_engine.introspection import introspect_feature, get_feature_catalog

# Create singleton instances
registry = FeatureRegistry()
executor = FeatureExecutor(registry)

__all__ = [
    'FeatureMetadata',
    'feature',
    'registry',
    'executor',
    'introspect_feature',
    'get_feature_catalog'
]

__version__ = '1.0.0'
