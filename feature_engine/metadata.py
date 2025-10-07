"""
Feature Metadata Classes

Defines the structure and metadata for feature definitions.
"""

from typing import List, Callable, Optional, Any, Dict
from dataclasses import dataclass, field
from enum import Enum


class FeatureCategory(Enum):
    """Feature categories matching the waterfall pipeline stages"""
    FILTER = 'filter'  # Row-level calculations (no aggregation)
    ATTRIBUTE = 'attribute'  # Aggregated metrics
    SCORE = 'score'  # Scoring and insights
    PREPROCESSING = 'preprocessing'  # Data cleaning and preparation


class DataType(Enum):
    """Supported data types for features"""
    INTEGER = 'integer'
    FLOAT = 'float'
    STRING = 'string'
    BOOLEAN = 'boolean'
    DATETIME = 'datetime'
    LONG = 'long'
    DICT = 'dict'
    DATAFRAME = 'dataframe'
    LIST = 'list'


@dataclass
class FeatureMetadata:
    """
    Metadata for a feature definition.

    Attributes:
        name: Unique feature identifier
        description: Human-readable description
        category: Feature category (filter, attribute, score)
        function: Callable that performs the calculation
        dtype: Expected output data type
        requires: List of required config keys or DataFrame columns
        depends_on: List of other features that must execute first
        optional_requires: List of optional config keys
        length: Maximum length for string/numeric types
        decimal_scale: Decimal places for float types
        is_aggregation: Whether feature performs aggregation
        tags: Optional tags for categorization
        version: Feature version for tracking changes
        author: Feature author/maintainer
    """
    name: str
    description: str
    category: FeatureCategory
    function: Callable
    dtype: DataType
    requires: List[str] = field(default_factory=list)
    depends_on: List[str] = field(default_factory=list)
    optional_requires: List[str] = field(default_factory=list)
    length: Optional[int] = None
    decimal_scale: Optional[int] = None
    is_aggregation: bool = False
    tags: List[str] = field(default_factory=list)
    version: str = '1.0.0'
    author: Optional[str] = None

    def __post_init__(self):
        """Validate and normalize metadata after initialization"""
        # Convert string enums to actual enums
        if isinstance(self.category, str):
            self.category = FeatureCategory(self.category)
        if isinstance(self.dtype, str):
            self.dtype = DataType(self.dtype)

        # Validate function is callable
        if not callable(self.function):
            raise ValueError(f"Feature '{self.name}' function must be callable")

        # Ensure no duplicate dependencies
        self.depends_on = list(set(self.depends_on))
        self.requires = list(set(self.requires))
        self.optional_requires = list(set(self.optional_requires))

    def to_dict(self) -> Dict[str, Any]:
        """Convert metadata to dictionary for serialization"""
        return {
            'name': self.name,
            'description': self.description,
            'category': self.category.value,
            'dtype': self.dtype.value,
            'requires': self.requires,
            'depends_on': self.depends_on,
            'optional_requires': self.optional_requires,
            'length': self.length,
            'decimal_scale': self.decimal_scale,
            'is_aggregation': self.is_aggregation,
            'tags': self.tags,
            'version': self.version,
            'author': self.author
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any], function: Callable) -> 'FeatureMetadata':
        """Create metadata from dictionary (for deserialization)"""
        return cls(
            name=data['name'],
            description=data['description'],
            category=FeatureCategory(data['category']),
            function=function,
            dtype=DataType(data['dtype']),
            requires=data.get('requires', []),
            depends_on=data.get('depends_on', []),
            optional_requires=data.get('optional_requires', []),
            length=data.get('length'),
            decimal_scale=data.get('decimal_scale'),
            is_aggregation=data.get('is_aggregation', False),
            tags=data.get('tags', []),
            version=data.get('version', '1.0.0'),
            author=data.get('author')
        )

    def get_all_dependencies(self) -> List[str]:
        """Get all dependencies (required + optional)"""
        return self.requires + self.optional_requires

    def is_compatible_with_config(self, config: Dict) -> tuple[bool, List[str]]:
        """
        Check if feature is compatible with given config.

        Returns:
            (is_compatible, missing_required_keys)
        """
        missing = [key for key in self.requires if key not in config]
        return len(missing) == 0, missing

    def __repr__(self) -> str:
        return f"<FeatureMetadata(name='{self.name}', category={self.category.value}, dtype={self.dtype.value})>"

    def __str__(self) -> str:
        return f"{self.name} ({self.category.value}): {self.description}"
