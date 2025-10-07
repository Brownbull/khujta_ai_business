"""
Feature Executor

Executes features with automatic dependency resolution.
"""

import pandas as pd
from typing import Dict, List, Optional, Any, Union
import warnings

from feature_engine.registry import FeatureRegistry
from feature_engine.metadata import FeatureCategory


class FeatureExecutor:
    """
    Executes features with automatic dependency resolution.

    Handles:
    - Dependency resolution and execution ordering
    - Input validation
    - Error handling and reporting
    - Execution tracking and logging
    """

    def __init__(self, registry: FeatureRegistry):
        """
        Initialize executor with feature registry.

        Args:
            registry: FeatureRegistry instance
        """
        self.registry = registry
        self.execution_log = []

    def validate_inputs(
        self,
        feature_names: List[str],
        config: Dict,
        df: Optional[pd.DataFrame] = None
    ) -> tuple[bool, List[str]]:
        """
        Validate that all required inputs are available.

        Args:
            feature_names: List of features to validate
            config: Configuration dictionary
            df: Optional DataFrame (for column validation)

        Returns:
            (is_valid, error_messages)
        """
        errors = []

        # Check all features exist
        for name in feature_names:
            if not self.registry.exists(name):
                errors.append(f"Feature '{name}' not found in registry")

        if errors:
            return False, errors

        # Get execution order (includes dependencies)
        try:
            execution_order = self.registry.get_execution_order(feature_names)
        except ValueError as e:
            errors.append(str(e))
            return False, errors

        # Validate each feature
        for name in execution_order:
            metadata = self.registry.get(name)

            # Check config requirements
            is_compatible, missing = metadata.is_compatible_with_config(config)
            if not is_compatible:
                errors.append(
                    f"Feature '{name}' missing required config keys: {missing}"
                )

            # Check column requirements (if df provided)
            if df is not None:
                for req in metadata.requires:
                    # Check if it's a column name (not a config key)
                    if req in config:
                        col_name = config[req]
                        if col_name not in df.columns:
                            errors.append(
                                f"Feature '{name}' requires column '{col_name}' (from config key '{req}')"
                            )

            # Check dependencies exist
            is_valid, missing_deps = self.registry.validate_dependencies(name)
            if not is_valid:
                errors.append(
                    f"Feature '{name}' has missing dependencies: {missing_deps}"
                )

        return len(errors) == 0, errors

    def execute(
        self,
        df: pd.DataFrame,
        feature_names: List[str],
        config: Dict,
        validate: bool = True,
        verbose: bool = True
    ) -> Union[pd.DataFrame, Dict]:
        """
        Execute a list of features.

        Args:
            df: Input DataFrame
            feature_names: List of features to execute
            config: Configuration dictionary
            validate: Whether to validate inputs before execution
            verbose: Whether to print execution progress

        Returns:
            Modified DataFrame (for filters) or results dict (for attributes/scores)

        Raises:
            ValueError: If validation fails
        """
        # Validate inputs
        if validate:
            is_valid, errors = self.validate_inputs(feature_names, config, df)
            if not is_valid:
                error_msg = "Validation failed:\n" + "\n".join(f"  - {e}" for e in errors)
                raise ValueError(error_msg)

        # Get execution order
        execution_order = self.registry.get_execution_order(feature_names)

        if verbose:
            print(f"\nExecuting {len(execution_order)} features...")
            print(f"Order: {' -> '.join(execution_order)}\n")

        # Execute features
        results = {}
        current_df = df.copy()

        for name in execution_order:
            metadata = self.registry.get(name)

            if verbose:
                print(f"  * Executing: {name} ({metadata.category.value})...", end=" ")

            try:
                # Execute feature function
                result = metadata.function(current_df, config)

                # Handle result based on category
                if metadata.category == FeatureCategory.FILTER:
                    # Filters return modified DataFrame
                    if isinstance(result, pd.DataFrame):
                        current_df = result
                    else:
                        warnings.warn(
                            f"Filter '{name}' should return DataFrame, got {type(result)}"
                        )

                elif metadata.category in [FeatureCategory.ATTRIBUTE, FeatureCategory.SCORE]:
                    # Attributes/Scores return results
                    results[name] = result

                # Log execution
                self.execution_log.append({
                    'feature': name,
                    'category': metadata.category.value,
                    'status': 'success'
                })

                if verbose:
                    print("[OK]")

            except Exception as e:
                error_msg = f"Failed to execute feature '{name}': {str(e)}"
                self.execution_log.append({
                    'feature': name,
                    'category': metadata.category.value,
                    'status': 'error',
                    'error': str(e)
                })

                if verbose:
                    print(f"[FAIL]\n    Error: {str(e)}")

                raise RuntimeError(error_msg) from e

        # Return appropriate result
        if all(self.registry.get(name).category == FeatureCategory.FILTER for name in feature_names):
            # All filters -> return DataFrame
            return current_df
        elif results:
            # Has attributes/scores -> return results dict
            return results
        else:
            # Mixed or only filters
            return current_df

    def execute_single(
        self,
        df: pd.DataFrame,
        feature_name: str,
        config: Dict,
        validate: bool = True,
        verbose: bool = False
    ) -> Union[pd.DataFrame, Any]:
        """Execute a single feature"""
        return self.execute(df, [feature_name], config, validate, verbose)

    def execute_with_dependencies(
        self,
        df: pd.DataFrame,
        feature_name: str,
        config: Dict,
        validate: bool = True,
        verbose: bool = True
    ) -> Union[pd.DataFrame, Any]:
        """
        Execute a feature with all its dependencies automatically resolved.

        Args:
            df: Input DataFrame
            feature_name: Feature to execute
            config: Configuration dictionary
            validate: Whether to validate inputs
            verbose: Whether to print progress

        Returns:
            Execution result (DataFrame or dict)
        """
        if not self.registry.exists(feature_name):
            raise ValueError(f"Feature '{feature_name}' not found in registry")

        # Get all dependencies
        all_deps = self.registry.get_dependencies(feature_name, recursive=True)
        all_features = all_deps + [feature_name]

        if verbose and all_deps:
            print(f"Feature '{feature_name}' requires {len(all_deps)} dependencies:")
            for dep in all_deps:
                print(f"  - {dep}")

        return self.execute(df, all_features, config, validate, verbose)

    def execute_by_category(
        self,
        df: pd.DataFrame,
        category: Union[str, FeatureCategory],
        config: Dict,
        feature_names: Optional[List[str]] = None,
        validate: bool = True,
        verbose: bool = True
    ) -> Union[pd.DataFrame, Dict]:
        """
        Execute all features in a category.

        Args:
            df: Input DataFrame
            category: Category to execute
            config: Configuration dictionary
            feature_names: Optional list to filter features (executes only these)
            validate: Whether to validate inputs
            verbose: Whether to print progress

        Returns:
            Execution result
        """
        if isinstance(category, str):
            category = FeatureCategory(category)

        # Get all features in category
        all_features = self.registry.get_feature_names(category)

        # Filter if specific names provided
        if feature_names:
            all_features = [f for f in all_features if f in feature_names]

        if not all_features:
            warnings.warn(f"No features found in category '{category.value}'")
            return df

        return self.execute(df, all_features, config, validate, verbose)

    def dry_run(
        self,
        feature_names: List[str],
        config: Dict,
        df: Optional[pd.DataFrame] = None
    ) -> Dict:
        """
        Perform a dry run without executing features.

        Returns:
            Dictionary with execution plan and validation results
        """
        # Validate
        is_valid, errors = self.validate_inputs(feature_names, config, df)

        # Get execution order
        try:
            execution_order = self.registry.get_execution_order(feature_names)
        except ValueError as e:
            execution_order = []
            errors.append(str(e))

        # Get details for each feature
        feature_details = []
        for name in feature_names:
            if self.registry.exists(name):
                metadata = self.registry.get(name)
                feature_details.append({
                    'name': name,
                    'category': metadata.category.value,
                    'requires': metadata.requires,
                    'depends_on': metadata.depends_on,
                    'is_aggregation': metadata.is_aggregation
                })

        return {
            'is_valid': is_valid,
            'errors': errors,
            'execution_order': execution_order,
            'total_features': len(execution_order),
            'feature_details': feature_details
        }

    def get_execution_log(self) -> List[Dict]:
        """Get execution log"""
        return self.execution_log.copy()

    def clear_log(self) -> None:
        """Clear execution log"""
        self.execution_log.clear()

    def __repr__(self) -> str:
        return f"<FeatureExecutor: {len(self.registry)} features available>"
