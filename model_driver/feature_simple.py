"""
Simplified Feature Registration

No decorators, no boilerplate - just functions and simple metadata.
"""

from typing import Callable, List, Dict, Optional, Any
from dataclasses import dataclass, field


@dataclass
class FeatureMetadata:
    """
    Minimal metadata for a feature.

    Much simpler than the decorator-based approach in feature_engine.
    """
    name: str
    function: Callable
    inputs: List[str]  # Required input columns
    outputs: List[str]  # Created output columns
    depends_on: List[str] = field(default_factory=list)  # Other features needed first
    dtype: str = 'float'
    description: str = ''
    category: str = 'filter'  # 'filter' or 'attribute'

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        return {
            'name': self.name,
            'inputs': self.inputs,
            'outputs': self.outputs,
            'depends_on': self.depends_on,
            'dtype': self.dtype,
            'description': self.description,
            'category': self.category
        }


class FeatureRegistry:
    """
    Simple registry for storing features.

    No automatic registration, no magic - explicit is better.
    """

    def __init__(self):
        self.filters: Dict[str, FeatureMetadata] = {}
        self.attributes: Dict[str, FeatureMetadata] = {}

    def register_filter(
        self,
        name: str,
        function: Callable,
        inputs: List[str],
        outputs: List[str],
        depends_on: List[str] = None,
        dtype: str = 'float',
        description: str = ''
    ) -> None:
        """
        Register a filter (row-level calculation).

        Args:
            name: Feature name
            function: Function that takes df and returns modified df
            inputs: List of required input columns
            outputs: List of output columns created
            depends_on: List of other features that must execute first
            dtype: Output data type
            description: Human-readable description

        Example:
            def profit_margin(df):
                df['profit_margin'] = (df['revenue'] - df['cost']) / df['revenue'] * 100
                return df

            registry.register_filter(
                'profit_margin',
                profit_margin,
                inputs=['revenue', 'cost'],
                outputs=['profit_margin'],
                dtype='float'
            )
        """
        metadata = FeatureMetadata(
            name=name,
            function=function,
            inputs=inputs,
            outputs=outputs,
            depends_on=depends_on or [],
            dtype=dtype,
            description=description,
            category='filter'
        )

        self.filters[name] = metadata
        print(f"[OK] Registered filter: {name}")

    def register_attribute(
        self,
        name: str,
        function: Callable,
        inputs: List[str],
        outputs: List[str],
        depends_on: List[str] = None,
        dtype: str = 'dataframe',
        description: str = ''
    ) -> None:
        """
        Register an attribute (aggregated calculation).

        Args:
            name: Feature name
            function: Function that takes df and returns aggregated result
            inputs: List of required input columns
            outputs: List of output columns in aggregated result
            depends_on: List of other features that must execute first
            dtype: Output data type
            description: Human-readable description

        Example:
            def total_revenue_by_product(df):
                return df.groupby('product')['revenue'].sum().reset_index()

            registry.register_attribute(
                'total_revenue_by_product',
                total_revenue_by_product,
                inputs=['product', 'revenue'],
                outputs=['product', 'total_revenue'],
                dtype='dataframe'
            )
        """
        metadata = FeatureMetadata(
            name=name,
            function=function,
            inputs=inputs,
            outputs=outputs,
            depends_on=depends_on or [],
            dtype=dtype,
            description=description,
            category='attribute'
        )

        self.attributes[name] = metadata
        print(f"[OK] Registered attribute: {name}")

    def get_filter(self, name: str) -> Optional[FeatureMetadata]:
        """Get a filter by name"""
        return self.filters.get(name)

    def get_attribute(self, name: str) -> Optional[FeatureMetadata]:
        """Get an attribute by name"""
        return self.attributes.get(name)

    def get_feature(self, name: str) -> Optional[FeatureMetadata]:
        """Get any feature (filter or attribute) by name"""
        return self.filters.get(name) or self.attributes.get(name)

    def list_filters(self) -> List[str]:
        """List all registered filter names"""
        return list(self.filters.keys())

    def list_attributes(self) -> List[str]:
        """List all registered attribute names"""
        return list(self.attributes.keys())

    def list_all(self) -> List[str]:
        """List all registered feature names"""
        return self.list_filters() + self.list_attributes()

    def clear(self) -> None:
        """Clear all registered features"""
        self.filters.clear()
        self.attributes.clear()

    def __len__(self) -> int:
        return len(self.filters) + len(self.attributes)

    def __contains__(self, name: str) -> bool:
        return name in self.filters or name in self.attributes

    def __repr__(self) -> str:
        return f"<FeatureRegistry: {len(self.filters)} filters, {len(self.attributes)} attributes>"


# Convenience functions for batch registration

def register_filters_from_dict(registry: FeatureRegistry, filters_dict: Dict[str, Dict]) -> None:
    """
    Register multiple filters from a dictionary.

    Args:
        registry: FeatureRegistry instance
        filters_dict: Dict mapping feature names to metadata dicts

    Example:
        filters = {
            'profit_margin': {
                'func': profit_margin,
                'inputs': ['revenue', 'cost'],
                'outputs': ['profit_margin'],
                'dtype': 'float'
            },
            'price_per_unit': {
                'func': price_per_unit,
                'inputs': ['revenue', 'quantity'],
                'outputs': ['price_per_unit'],
                'dtype': 'float'
            }
        }

        register_filters_from_dict(registry, filters)
    """
    for name, metadata in filters_dict.items():
        registry.register_filter(
            name=name,
            function=metadata['func'],
            inputs=metadata['inputs'],
            outputs=metadata['outputs'],
            depends_on=metadata.get('depends_on', []),
            dtype=metadata.get('dtype', 'float'),
            description=metadata.get('description', '')
        )


def register_attributes_from_dict(registry: FeatureRegistry, attributes_dict: Dict[str, Dict]) -> None:
    """
    Register multiple attributes from a dictionary.

    Args:
        registry: FeatureRegistry instance
        attributes_dict: Dict mapping feature names to metadata dicts

    Example:
        attributes = {
            'total_revenue_by_product': {
                'func': total_revenue_by_product,
                'inputs': ['product', 'revenue'],
                'outputs': ['product', 'total_revenue'],
                'dtype': 'dataframe'
            }
        }

        register_attributes_from_dict(registry, attributes)
    """
    for name, metadata in attributes_dict.items():
        registry.register_attribute(
            name=name,
            function=metadata['func'],
            inputs=metadata['inputs'],
            outputs=metadata['outputs'],
            depends_on=metadata.get('depends_on', []),
            dtype=metadata.get('dtype', 'dataframe'),
            description=metadata.get('description', '')
        )
