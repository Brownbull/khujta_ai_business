"""
Feature Decorators

Provides @feature decorator for easy feature registration.
"""

from typing import Callable, List, Optional
from functools import wraps
from feature_engine.metadata import FeatureMetadata, FeatureCategory, DataType


def feature(
    name: str,
    description: str,
    category: str,
    dtype: str,
    requires: List[str] = None,
    depends_on: List[str] = None,
    optional_requires: List[str] = None,
    length: Optional[int] = None,
    decimal_scale: Optional[int] = None,
    is_aggregation: bool = False,
    tags: List[str] = None,
    version: str = '1.0.0',
    author: Optional[str] = None,
    auto_register: bool = True
):
    """
    Decorator to define and register a feature.

    Args:
        name: Unique feature identifier
        description: Human-readable description
        category: Feature category ('filter', 'attribute', 'score', 'preprocessing')
        dtype: Output data type ('integer', 'float', 'string', 'boolean', etc.)
        requires: List of required config keys or DataFrame columns
        depends_on: List of other features that must execute first
        optional_requires: List of optional config keys
        length: Maximum length for string/numeric types
        decimal_scale: Decimal places for float types
        is_aggregation: Whether feature performs aggregation
        tags: Optional tags for categorization
        version: Feature version
        author: Feature author/maintainer
        auto_register: Automatically register with global registry

    Example:
        @feature(
            name='profit_margin',
            description='Profit margin percentage',
            category='filter',
            dtype='float',
            requires=['revenue_col', 'cost_col'],
            optional_requires=['cost_col']
        )
        def calculate_profit_margin(df, config):
            revenue_col = config['revenue_col']
            cost_col = config.get('cost_col')

            if cost_col and cost_col in df.columns:
                df['profit_margin'] = ((df[revenue_col] - df[cost_col]) / df[revenue_col]) * 100
            return df
    """
    def decorator(func: Callable) -> Callable:
        # Create metadata
        metadata = FeatureMetadata(
            name=name,
            description=description,
            category=category,
            function=func,
            dtype=dtype,
            requires=requires or [],
            depends_on=depends_on or [],
            optional_requires=optional_requires or [],
            length=length,
            decimal_scale=decimal_scale,
            is_aggregation=is_aggregation,
            tags=tags or [],
            version=version,
            author=author
        )

        # Attach metadata to function
        func._feature_metadata = metadata

        # Auto-register if enabled
        if auto_register:
            try:
                from feature_engine import registry
                registry.register(metadata)
            except ImportError:
                # Registry not yet initialized, will be registered later
                pass

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        # Also attach metadata to wrapper
        wrapper._feature_metadata = metadata

        return wrapper

    return decorator


def get_feature_metadata(func: Callable) -> Optional[FeatureMetadata]:
    """
    Extract feature metadata from a decorated function.

    Args:
        func: Decorated function

    Returns:
        FeatureMetadata if function is decorated, None otherwise
    """
    return getattr(func, '_feature_metadata', None)


def is_feature(func: Callable) -> bool:
    """
    Check if a function is decorated with @feature.

    Args:
        func: Function to check

    Returns:
        True if function has feature metadata
    """
    return hasattr(func, '_feature_metadata')


# Convenience decorators for specific categories

def filter_feature(
    name: str,
    description: str,
    dtype: str = 'float',
    requires: List[str] = None,
    depends_on: List[str] = None,
    **kwargs
):
    """Convenience decorator for filter features (row-level calculations)"""
    return feature(
        name=name,
        description=description,
        category='filter',
        dtype=dtype,
        requires=requires,
        depends_on=depends_on,
        is_aggregation=False,
        **kwargs
    )


def attribute_feature(
    name: str,
    description: str,
    dtype: str = 'dict',
    requires: List[str] = None,
    depends_on: List[str] = None,
    **kwargs
):
    """Convenience decorator for attribute features (aggregations)"""
    return feature(
        name=name,
        description=description,
        category='attribute',
        dtype=dtype,
        requires=requires,
        depends_on=depends_on,
        is_aggregation=True,
        **kwargs
    )


def score_feature(
    name: str,
    description: str,
    dtype: str = 'dict',
    requires: List[str] = None,
    depends_on: List[str] = None,
    **kwargs
):
    """Convenience decorator for score features (insights)"""
    return feature(
        name=name,
        description=description,
        category='score',
        dtype=dtype,
        requires=requires,
        depends_on=depends_on,
        **kwargs
    )
