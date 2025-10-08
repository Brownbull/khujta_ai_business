"""
Dependency Resolver

Determines which features are needed based on requested outputs
and automatically resolves the required input columns.

This is the KEY innovation that solves the "dynamic input based on output" problem.
"""

from typing import List, Set, Tuple, Dict
from collections import defaultdict
from model_driver.feature_simple import FeatureRegistry, FeatureMetadata


class DependencyResolver:
    """
    Resolves dependencies and determines required inputs based on requested outputs.

    Example:
        resolver = DependencyResolver(registry)

        # I want these outputs
        required_features, required_inputs = resolver.resolve(['profit_margin', 'total_revenue'])

        # Returns:
        # required_features = ['profit_margin', 'total_revenue']
        # required_inputs = ['revenue', 'cost', 'product']
    """

    def __init__(self, registry: FeatureRegistry):
        """
        Initialize resolver with a feature registry.

        Args:
            registry: FeatureRegistry containing all registered features
        """
        self.registry = registry

    def resolve(self, output_features: List[str]) -> Tuple[List[str], List[str]]:
        """
        Resolve dependencies and determine required inputs.

        Args:
            output_features: List of feature names that are desired as output

        Returns:
            (required_features, required_inputs)
            - required_features: All features that need to execute (including dependencies)
            - required_inputs: All input columns required from raw data

        Raises:
            ValueError: If a feature is not found or circular dependency detected
        """
        required_features = set()
        required_inputs = set()

        # Walk dependency tree for each output feature
        def walk(feature_name: str, path: List[str] = None):
            """Recursively walk dependencies"""
            if path is None:
                path = []

            # Check for circular dependency
            if feature_name in path:
                raise ValueError(
                    f"Circular dependency detected: {' -> '.join(path + [feature_name])}"
                )

            # Already processed
            if feature_name in required_features:
                return

            # Get feature metadata
            feature = self.registry.get_feature(feature_name)
            if feature is None:
                raise ValueError(f"Feature '{feature_name}' not found in registry")

            # Mark as required
            required_features.add(feature_name)

            # Add input columns needed by this feature
            # BUT exclude columns that are outputs from other features
            for input_col in feature.inputs:
                # Check if this input is actually an output from another feature
                is_feature_output = False
                for other_feature_name in self.registry.list_all():
                    other_feature = self.registry.get_feature(other_feature_name)
                    if input_col in other_feature.outputs:
                        is_feature_output = True
                        break

                # Only add as required input if it's not a feature output
                if not is_feature_output:
                    required_inputs.add(input_col)

            # Recursively walk dependencies
            for dep in feature.depends_on:
                walk(dep, path + [feature_name])

        # Walk all requested output features
        for feature_name in output_features:
            walk(feature_name)

        return list(required_features), list(sorted(required_inputs))

    def get_execution_order(self, features: List[str]) -> List[str]:
        """
        Determine execution order for features using topological sort.

        Args:
            features: List of features to order

        Returns:
            List of features in execution order (dependencies first)

        Raises:
            ValueError: If circular dependency detected
        """
        # Build dependency graph
        in_degree = {name: 0 for name in features}
        adj_list = defaultdict(list)

        for name in features:
            feature = self.registry.get_feature(name)
            if feature is None:
                raise ValueError(f"Feature '{name}' not found")

            for dep in feature.depends_on:
                if dep in features:
                    adj_list[dep].append(name)
                    in_degree[name] += 1

        # Kahn's algorithm for topological sort
        queue = [name for name in features if in_degree[name] == 0]
        result = []

        while queue:
            # Sort for deterministic ordering
            queue.sort()
            current = queue.pop(0)
            result.append(current)

            # Update neighbors
            for neighbor in adj_list[current]:
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # Check for circular dependency
        if len(result) != len(features):
            remaining = set(features) - set(result)
            raise ValueError(f"Circular dependency detected among: {remaining}")

        return result

    def get_execution_plan(self, output_features: List[str]) -> Dict:
        """
        Get complete execution plan including features, inputs, and order.

        Args:
            output_features: Desired output features

        Returns:
            Dict with keys:
            - output_features: Requested outputs
            - required_features: All features to execute
            - required_inputs: All input columns needed
            - execution_order: Order to execute features
            - filters: List of filter names to execute
            - attributes: List of attribute names to execute
        """
        # Resolve dependencies
        required_features, required_inputs = self.resolve(output_features)

        # Get execution order
        execution_order = self.get_execution_order(required_features)

        # Separate filters and attributes
        filters = []
        attributes = []

        for name in execution_order:
            feature = self.registry.get_feature(name)
            if feature.category == 'filter':
                filters.append(name)
            else:
                attributes.append(name)

        return {
            'output_features': output_features,
            'required_features': required_features,
            'required_inputs': required_inputs,
            'execution_order': execution_order,
            'filters': filters,
            'attributes': attributes
        }

    def visualize_dependencies(self, output_features: List[str]) -> str:
        """
        Create a text visualization of the dependency tree.

        Args:
            output_features: Features to visualize

        Returns:
            String representation of dependency tree
        """
        lines = []
        lines.append("Dependency Tree:")
        lines.append("=" * 70)

        def visualize_feature(name: str, level: int = 0, visited: Set[str] = None):
            if visited is None:
                visited = set()

            if name in visited:
                lines.append("  " * level + f"- {name} (circular reference)")
                return

            visited.add(name)

            feature = self.registry.get_feature(name)
            if feature is None:
                lines.append("  " * level + f"- {name} (NOT FOUND)")
                return

            lines.append("  " * level + f"- {name} [{feature.category}]")
            lines.append("  " * level + f"  Inputs: {', '.join(feature.inputs)}")
            lines.append("  " * level + f"  Outputs: {', '.join(feature.outputs)}")

            if feature.depends_on:
                lines.append("  " * level + f"  Depends on:")
                for dep in feature.depends_on:
                    visualize_feature(dep, level + 2, visited.copy())

        for feature_name in output_features:
            visualize_feature(feature_name)
            lines.append("")

        return "\n".join(lines)

    def print_execution_plan(self, output_features: List[str]) -> None:
        """
        Print a formatted execution plan.

        Args:
            output_features: Desired output features
        """
        plan = self.get_execution_plan(output_features)

        print("\n" + "=" * 70)
        print("EXECUTION PLAN")
        print("=" * 70)

        print(f"\nOutput Features ({len(plan['output_features'])}):")
        for name in plan['output_features']:
            print(f"  - {name}")

        print(f"\nRequired Features ({len(plan['required_features'])}):")
        for name in plan['required_features']:
            feature = self.registry.get_feature(name)
            print(f"  - {name} [{feature.category}]")

        print(f"\nRequired Inputs ({len(plan['required_inputs'])}):")
        for col in plan['required_inputs']:
            print(f"  - {col}")

        print(f"\nExecution Order:")
        for i, name in enumerate(plan['execution_order'], 1):
            feature = self.registry.get_feature(name)
            deps_str = f" (after: {', '.join(feature.depends_on)})" if feature.depends_on else ""
            print(f"  {i}. {name} [{feature.category}]{deps_str}")

        print("=" * 70 + "\n")


def validate_feature_dependencies(registry: FeatureRegistry) -> Tuple[bool, List[str]]:
    """
    Validate that all feature dependencies exist and there are no circular dependencies.

    Args:
        registry: FeatureRegistry to validate

    Returns:
        (is_valid, list_of_errors)
    """
    errors = []

    # Check all features
    for feature_name in registry.list_all():
        feature = registry.get_feature(feature_name)

        # Check dependencies exist
        for dep in feature.depends_on:
            if dep not in registry:
                errors.append(f"Feature '{feature_name}' depends on '{dep}' which is not registered")

    # Check for circular dependencies
    if not errors:
        resolver = DependencyResolver(registry)
        for feature_name in registry.list_all():
            try:
                resolver.resolve([feature_name])
            except ValueError as e:
                errors.append(str(e))

    return len(errors) == 0, errors
