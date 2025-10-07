"""
Feature Registry

Central registry for managing and discovering features.
"""

from typing import Dict, List, Optional, Set
from collections import defaultdict
import warnings

from feature_engine.metadata import FeatureMetadata, FeatureCategory


class FeatureRegistry:
    """
    Central registry for all features.

    Manages feature storage, discovery, and dependency resolution.
    """

    def __init__(self):
        """Initialize empty registry"""
        self._features: Dict[str, FeatureMetadata] = {}
        self._by_category: Dict[FeatureCategory, List[str]] = defaultdict(list)
        self._by_tag: Dict[str, List[str]] = defaultdict(list)
        self._dependency_graph: Dict[str, Set[str]] = {}

    def register(self, metadata: FeatureMetadata) -> None:
        """
        Register a feature in the registry.

        Args:
            metadata: Feature metadata to register

        Raises:
            ValueError: If feature name already exists
        """
        if metadata.name in self._features:
            warnings.warn(
                f"Feature '{metadata.name}' already registered. Overwriting previous definition.",
                UserWarning
            )

        # Store feature
        self._features[metadata.name] = metadata

        # Index by category
        if metadata.name not in self._by_category[metadata.category]:
            self._by_category[metadata.category].append(metadata.name)

        # Index by tags
        for tag in metadata.tags:
            if metadata.name not in self._by_tag[tag]:
                self._by_tag[tag].append(metadata.name)

        # Build dependency graph
        self._dependency_graph[metadata.name] = set(metadata.depends_on)

        print(f"[OK] Registered feature: {metadata.name} ({metadata.category.value})")

    def register_multiple(self, features: List[FeatureMetadata]) -> None:
        """Register multiple features at once"""
        for feature in features:
            self.register(feature)

    def get(self, name: str) -> Optional[FeatureMetadata]:
        """Get feature by name"""
        return self._features.get(name)

    def get_all(self) -> Dict[str, FeatureMetadata]:
        """Get all registered features"""
        return self._features.copy()

    def get_by_category(self, category: FeatureCategory) -> Dict[str, FeatureMetadata]:
        """Get all features in a category"""
        if isinstance(category, str):
            category = FeatureCategory(category)

        feature_names = self._by_category.get(category, [])
        return {name: self._features[name] for name in feature_names}

    def get_by_tag(self, tag: str) -> Dict[str, FeatureMetadata]:
        """Get all features with a specific tag"""
        feature_names = self._by_tag.get(tag, [])
        return {name: self._features[name] for name in feature_names}

    def exists(self, name: str) -> bool:
        """Check if feature exists"""
        return name in self._features

    def get_categories(self) -> List[FeatureCategory]:
        """Get all categories with registered features"""
        return list(self._by_category.keys())

    def get_tags(self) -> List[str]:
        """Get all tags used by registered features"""
        return list(self._by_tag.keys())

    def get_feature_names(self, category: Optional[FeatureCategory] = None) -> List[str]:
        """
        Get list of feature names.

        Args:
            category: Optional category filter

        Returns:
            List of feature names
        """
        if category is None:
            return list(self._features.keys())

        if isinstance(category, str):
            category = FeatureCategory(category)

        return self._by_category.get(category, [])

    def get_dependencies(self, feature_name: str, recursive: bool = False) -> List[str]:
        """
        Get dependencies for a feature.

        Args:
            feature_name: Name of feature
            recursive: If True, get all transitive dependencies

        Returns:
            List of feature names that are dependencies
        """
        if feature_name not in self._features:
            raise ValueError(f"Feature '{feature_name}' not found in registry")

        if not recursive:
            return list(self._dependency_graph.get(feature_name, set()))

        # Get all transitive dependencies
        all_deps = set()
        to_process = [feature_name]
        processed = set()

        while to_process:
            current = to_process.pop(0)
            if current in processed:
                continue

            processed.add(current)
            direct_deps = self._dependency_graph.get(current, set())

            for dep in direct_deps:
                if dep not in all_deps:
                    all_deps.add(dep)
                    to_process.append(dep)

        return list(all_deps)

    def get_execution_order(self, feature_names: List[str]) -> List[str]:
        """
        Get execution order for a list of features using topological sort.

        Args:
            feature_names: List of features to execute

        Returns:
            Ordered list of features respecting dependencies

        Raises:
            ValueError: If circular dependency detected
        """
        # Add all dependencies
        all_features = set(feature_names)
        for name in feature_names:
            all_features.update(self.get_dependencies(name, recursive=True))

        # Topological sort using Kahn's algorithm
        in_degree = {name: 0 for name in all_features}
        adj_list = defaultdict(list)

        # Build adjacency list and in-degree counts
        for name in all_features:
            deps = self._dependency_graph.get(name, set())
            for dep in deps:
                if dep in all_features:
                    adj_list[dep].append(name)
                    in_degree[name] += 1

        # Find all nodes with no incoming edges
        queue = [name for name in all_features if in_degree[name] == 0]
        result = []

        while queue:
            # Sort queue for deterministic ordering
            queue.sort()
            current = queue.pop(0)
            result.append(current)

            # Reduce in-degree for neighbors
            for neighbor in adj_list[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # Check for circular dependencies
        if len(result) != len(all_features):
            raise ValueError(
                f"Circular dependency detected in features: {all_features - set(result)}"
            )

        return result

    def validate_dependencies(self, feature_name: str) -> tuple[bool, List[str]]:
        """
        Validate that all dependencies exist.

        Returns:
            (is_valid, missing_dependencies)
        """
        if feature_name not in self._features:
            return False, [feature_name]

        feature = self._features[feature_name]
        missing = [dep for dep in feature.depends_on if dep not in self._features]

        return len(missing) == 0, missing

    def introspect(self, feature_name: str) -> Dict:
        """
        Get detailed information about a feature.

        Args:
            feature_name: Name of feature

        Returns:
            Dictionary with feature details
        """
        if feature_name not in self._features:
            raise ValueError(f"Feature '{feature_name}' not found in registry")

        metadata = self._features[feature_name]

        return {
            'name': metadata.name,
            'description': metadata.description,
            'category': metadata.category.value,
            'dtype': metadata.dtype.value,
            'requires': metadata.requires,
            'optional_requires': metadata.optional_requires,
            'depends_on': metadata.depends_on,
            'all_dependencies': self.get_dependencies(feature_name, recursive=True),
            'is_aggregation': metadata.is_aggregation,
            'length': metadata.length,
            'decimal_scale': metadata.decimal_scale,
            'tags': metadata.tags,
            'version': metadata.version,
            'author': metadata.author
        }

    def search(self, query: str, search_in: List[str] = None) -> Dict[str, FeatureMetadata]:
        """
        Search for features by keyword.

        Args:
            query: Search query
            search_in: Fields to search in ['name', 'description', 'tags']

        Returns:
            Dictionary of matching features
        """
        if search_in is None:
            search_in = ['name', 'description', 'tags']

        query_lower = query.lower()
        results = {}

        for name, metadata in self._features.items():
            match = False

            if 'name' in search_in and query_lower in name.lower():
                match = True
            if 'description' in search_in and query_lower in metadata.description.lower():
                match = True
            if 'tags' in search_in and any(query_lower in tag.lower() for tag in metadata.tags):
                match = True

            if match:
                results[name] = metadata

        return results

    def clear(self) -> None:
        """Clear all registered features"""
        self._features.clear()
        self._by_category.clear()
        self._by_tag.clear()
        self._dependency_graph.clear()

    def count(self, category: Optional[FeatureCategory] = None) -> int:
        """Count registered features"""
        if category is None:
            return len(self._features)

        if isinstance(category, str):
            category = FeatureCategory(category)

        return len(self._by_category.get(category, []))

    def __len__(self) -> int:
        return len(self._features)

    def __contains__(self, name: str) -> bool:
        return name in self._features

    def __repr__(self) -> str:
        return f"<FeatureRegistry: {len(self._features)} features registered>"
