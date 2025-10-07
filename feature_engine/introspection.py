"""
Introspection Tools

Runtime inspection and documentation generation for features.
"""

from typing import Dict, List, Optional, Any
import json
from datetime import datetime

from feature_engine.registry import FeatureRegistry
from feature_engine.metadata import FeatureCategory


def introspect_feature(registry: FeatureRegistry, feature_name: str) -> Dict:
    """
    Get detailed information about a specific feature.

    Args:
        registry: FeatureRegistry instance
        feature_name: Name of feature to introspect

    Returns:
        Dictionary with feature details
    """
    return registry.introspect(feature_name)


def get_feature_catalog(
    registry: FeatureRegistry,
    category: Optional[FeatureCategory] = None,
    format: str = 'dict'
) -> Any:
    """
    Generate a catalog of all features.

    Args:
        registry: FeatureRegistry instance
        category: Optional category filter
        format: Output format ('dict', 'json', 'markdown', 'text')

    Returns:
        Feature catalog in requested format
    """
    if category:
        features = registry.get_by_category(category)
    else:
        features = registry.get_all()

    catalog_data = {
        'generated_at': datetime.now().isoformat(),
        'total_features': len(features),
        'features': {}
    }

    # Group by category
    by_category = {}
    for name, metadata in features.items():
        cat = metadata.category.value
        if cat not in by_category:
            by_category[cat] = []

        by_category[cat].append({
            'name': name,
            'description': metadata.description,
            'dtype': metadata.dtype.value,
            'requires': metadata.requires,
            'depends_on': metadata.depends_on,
            'is_aggregation': metadata.is_aggregation,
            'tags': metadata.tags,
            'version': metadata.version
        })

    catalog_data['features'] = by_category

    # Format output
    if format == 'dict':
        return catalog_data

    elif format == 'json':
        return json.dumps(catalog_data, indent=2)

    elif format == 'markdown':
        return _format_catalog_markdown(catalog_data, by_category)

    elif format == 'text':
        return _format_catalog_text(catalog_data, by_category)

    else:
        raise ValueError(f"Unsupported format: {format}")


def _format_catalog_markdown(catalog_data: Dict, by_category: Dict) -> str:
    """Format catalog as Markdown"""
    lines = [
        "# Feature Catalog",
        "",
        f"**Generated:** {catalog_data['generated_at']}",
        f"**Total Features:** {catalog_data['total_features']}",
        ""
    ]

    for category, features in sorted(by_category.items()):
        lines.append(f"## {category.upper()}")
        lines.append("")
        lines.append(f"*{len(features)} features*")
        lines.append("")

        for feat in sorted(features, key=lambda x: x['name']):
            lines.append(f"### `{feat['name']}`")
            lines.append("")
            lines.append(f"**Description:** {feat['description']}")
            lines.append("")
            lines.append(f"**Type:** `{feat['dtype']}`")
            lines.append("")

            if feat['requires']:
                lines.append(f"**Requires:** `{', '.join(feat['requires'])}`")
                lines.append("")

            if feat['depends_on']:
                lines.append(f"**Depends On:** `{', '.join(feat['depends_on'])}`")
                lines.append("")

            if feat['tags']:
                lines.append(f"**Tags:** {', '.join(feat['tags'])}")
                lines.append("")

            lines.append(f"**Version:** {feat['version']}")
            lines.append("")
            lines.append("---")
            lines.append("")

    return "\n".join(lines)


def _format_catalog_text(catalog_data: Dict, by_category: Dict) -> str:
    """Format catalog as plain text"""
    lines = [
        "=" * 80,
        "FEATURE CATALOG",
        "=" * 80,
        "",
        f"Generated: {catalog_data['generated_at']}",
        f"Total Features: {catalog_data['total_features']}",
        ""
    ]

    for category, features in sorted(by_category.items()):
        lines.append("=" * 80)
        lines.append(f"{category.upper()} ({len(features)} features)")
        lines.append("=" * 80)
        lines.append("")

        for feat in sorted(features, key=lambda x: x['name']):
            lines.append(f"Feature: {feat['name']}")
            lines.append(f"  Description: {feat['description']}")
            lines.append(f"  Type: {feat['dtype']}")

            if feat['requires']:
                lines.append(f"  Requires: {', '.join(feat['requires'])}")

            if feat['depends_on']:
                lines.append(f"  Depends On: {', '.join(feat['depends_on'])}")

            if feat['tags']:
                lines.append(f"  Tags: {', '.join(feat['tags'])}")

            lines.append(f"  Version: {feat['version']}")
            lines.append("")

    lines.append("=" * 80)
    return "\n".join(lines)


def get_dependency_tree(registry: FeatureRegistry, feature_name: str, format: str = 'dict') -> Any:
    """
    Get dependency tree for a feature.

    Args:
        registry: FeatureRegistry instance
        feature_name: Name of feature
        format: Output format ('dict', 'text')

    Returns:
        Dependency tree in requested format
    """
    if not registry.exists(feature_name):
        raise ValueError(f"Feature '{feature_name}' not found")

    def build_tree(name: str, visited: set = None) -> Dict:
        if visited is None:
            visited = set()

        if name in visited:
            return {'name': name, 'circular': True}

        visited.add(name)
        metadata = registry.get(name)

        node = {
            'name': name,
            'category': metadata.category.value,
            'description': metadata.description,
            'dependencies': []
        }

        for dep in metadata.depends_on:
            if registry.exists(dep):
                node['dependencies'].append(build_tree(dep, visited.copy()))
            else:
                node['dependencies'].append({'name': dep, 'missing': True})

        return node

    tree = build_tree(feature_name)

    if format == 'dict':
        return tree
    elif format == 'text':
        return _format_tree_text(tree)
    else:
        raise ValueError(f"Unsupported format: {format}")


def _format_tree_text(node: Dict, prefix: str = "", is_last: bool = True) -> str:
    """Format dependency tree as text"""
    lines = []

    connector = "└── " if is_last else "├── "
    lines.append(f"{prefix}{connector}{node['name']}")

    if node.get('circular'):
        lines[-1] += " (circular dependency)"
    elif node.get('missing'):
        lines[-1] += " (missing)"
    else:
        lines[-1] += f" [{node['category']}]"

    if 'dependencies' in node and node['dependencies']:
        extension = "    " if is_last else "│   "
        for i, dep in enumerate(node['dependencies']):
            is_last_dep = i == len(node['dependencies']) - 1
            lines.append(_format_tree_text(dep, prefix + extension, is_last_dep))

    return "\n".join(lines)


def get_statistics(registry: FeatureRegistry) -> Dict:
    """
    Get statistics about registered features.

    Args:
        registry: FeatureRegistry instance

    Returns:
        Dictionary with statistics
    """
    all_features = registry.get_all()

    stats = {
        'total_features': len(all_features),
        'by_category': {},
        'by_dtype': {},
        'aggregation_count': 0,
        'avg_dependencies': 0,
        'max_dependencies': 0,
        'features_with_no_deps': 0,
        'tags_used': len(registry.get_tags()),
        'top_tags': []
    }

    # By category
    for category in registry.get_categories():
        stats['by_category'][category.value] = registry.count(category)

    # By dtype
    dtype_counts = {}
    dependency_counts = []
    tag_counts = {}

    for metadata in all_features.values():
        # Dtype
        dtype = metadata.dtype.value
        dtype_counts[dtype] = dtype_counts.get(dtype, 0) + 1

        # Aggregation
        if metadata.is_aggregation:
            stats['aggregation_count'] += 1

        # Dependencies
        dep_count = len(metadata.depends_on)
        dependency_counts.append(dep_count)

        if dep_count == 0:
            stats['features_with_no_deps'] += 1

        # Tags
        for tag in metadata.tags:
            tag_counts[tag] = tag_counts.get(tag, 0) + 1

    stats['by_dtype'] = dtype_counts

    if dependency_counts:
        stats['avg_dependencies'] = sum(dependency_counts) / len(dependency_counts)
        stats['max_dependencies'] = max(dependency_counts)

    # Top tags
    if tag_counts:
        stats['top_tags'] = sorted(
            tag_counts.items(),
            key=lambda x: x[1],
            reverse=True
        )[:10]

    return stats


def print_statistics(registry: FeatureRegistry) -> None:
    """Print feature statistics to console"""
    stats = get_statistics(registry)

    print("\n" + "=" * 70)
    print("FEATURE REGISTRY STATISTICS")
    print("=" * 70)

    print(f"\nTotal Features: {stats['total_features']}")

    print("\nBy Category:")
    for cat, count in sorted(stats['by_category'].items()):
        print(f"  {cat:15s}: {count:3d} features")

    print("\nBy Data Type:")
    for dtype, count in sorted(stats['by_dtype'].items()):
        print(f"  {dtype:15s}: {count:3d} features")

    print(f"\nAggregations: {stats['aggregation_count']} features")
    print(f"Features with no dependencies: {stats['features_with_no_deps']}")
    print(f"Average dependencies per feature: {stats['avg_dependencies']:.2f}")
    print(f"Max dependencies: {stats['max_dependencies']}")

    if stats['top_tags']:
        print("\nTop Tags:")
        for tag, count in stats['top_tags']:
            print(f"  {tag:15s}: {count:3d} features")

    print("=" * 70 + "\n")


def validate_registry(registry: FeatureRegistry) -> tuple[bool, List[str]]:
    """
    Validate all features in registry.

    Checks:
    - All dependencies exist
    - No circular dependencies
    - Consistent metadata

    Returns:
        (is_valid, list_of_issues)
    """
    issues = []
    all_features = registry.get_all()

    for name, metadata in all_features.items():
        # Check dependencies exist
        is_valid, missing = registry.validate_dependencies(name)
        if not is_valid:
            issues.append(f"Feature '{name}' has missing dependencies: {missing}")

        # Check for circular dependencies
        try:
            registry.get_execution_order([name])
        except ValueError as e:
            issues.append(f"Feature '{name}': {str(e)}")

    return len(issues) == 0, issues
