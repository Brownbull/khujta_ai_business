"""
ModelDriver - Main Orchestrator

Unified orchestrator for the entire feature pipeline.
Manages configuration, registration, dependency resolution, and execution.

Example:
    driver = ModelDriver({
        'client_name': 'auto_partes',
        'model_name': 'sales_analysis',
        'output_base': 'data_management/'
    })

    driver.register_filter('profit_margin', profit_margin_func,
                          inputs=['revenue', 'cost'],
                          outputs=['profit_margin'])

    driver.set_output_attributes(['total_revenue', 'profit_margin'])
    required = driver.get_required_inputs()  # ['revenue', 'cost', 'product']

    result = driver.execute(df, save_intermediates=True)
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Callable, Optional, Any, Tuple
from pathlib import Path
from datetime import datetime
import json
import warnings
warnings.filterwarnings('ignore')

from model_driver.feature_simple import FeatureRegistry
from model_driver.resolver import DependencyResolver, validate_feature_dependencies


class ModelDriver:
    """
    Main orchestrator for feature pipeline execution.

    Manages the complete workflow:
    1. Feature registration (filters and attributes)
    2. Output attribute selection
    3. Dependency resolution (determines required inputs automatically)
    4. Staged execution (preprocess → filters → attributes → output)
    5. Intermediate output management
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initialize ModelDriver with configuration.

        Args:
            config: Configuration dictionary with keys:
                - client_name: Name of client/project
                - model_name: Name of model/analysis
                - output_base: Base directory for outputs (default: 'data_management/')
                - date_col: Name of date column (optional)
                - save_intermediates: Whether to save intermediate outputs (default: True)
        """
        self.config = config
        self.client_name = config['client_name']
        self.model_name = config['model_name']
        self.output_base = config.get('output_base', 'data_management/')
        self.date_col = config.get('date_col', 'fecha')
        self.save_intermediates = config.get('save_intermediates', True)

        # Initialize registry and resolver
        self.registry = FeatureRegistry()
        self.resolver = DependencyResolver(self.registry)

        # Output attributes (what user wants as final output)
        self.output_attributes = []

        # Execution metadata
        self.execution_plan = None
        self.execution_metadata = {}

        # Results cache
        self._preprocessed_df = None
        self._filtered_df = None
        self._attributes_df = None

        # Create timestamped run directory
        self.run_timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        self.run_dir = Path(self.output_base) / self.client_name / self.model_name / self.run_timestamp

        print(f"[OK] ModelDriver initialized: {self.client_name}/{self.model_name}")
        print(f"  Run directory: {self.run_dir}")

    # =========================================================================
    # REGISTRATION METHODS
    # =========================================================================

    def register_filter(self, name: str, function: Callable,
                       inputs: List[str], outputs: List[str],
                       depends_on: List[str] = None,
                       dtype: str = 'float',
                       description: str = '') -> None:
        """
        Register a filter (row-level calculation).

        Args:
            name: Feature name
            function: Function that takes DataFrame and returns DataFrame with new columns
            inputs: List of required input column names
            outputs: List of output column names this feature creates
            depends_on: List of feature names this depends on (optional)
            dtype: Data type of output columns
            description: Human-readable description
        """
        self.registry.register_filter(name, function, inputs, outputs,
                                     depends_on or [], dtype, description)
        print(f"[OK] Registered filter: {name}")

    def register_attribute(self, name: str, function: Callable,
                          inputs: List[str], outputs: List[str],
                          depends_on: List[str] = None,
                          dtype: str = 'float',
                          description: str = '') -> None:
        """
        Register an attribute (aggregation/computed metric).

        Args:
            name: Feature name
            function: Function that takes DataFrame and returns DataFrame with new columns
            inputs: List of required input column names
            outputs: List of output column names this feature creates
            depends_on: List of feature names this depends on (optional)
            dtype: Data type of output columns
            description: Human-readable description
        """
        self.registry.register_attribute(name, function, inputs, outputs,
                                        depends_on or [], dtype, description)
        print(f"[OK] Registered attribute: {name}")

    def register_filters_batch(self, features_dict: Dict[str, Dict]) -> None:
        """
        Register multiple filters from dictionary.

        Args:
            features_dict: Dictionary with feature definitions
                {
                    'feature_name': {
                        'function': callable,
                        'inputs': ['col1', 'col2'],
                        'outputs': ['new_col'],
                        'depends_on': ['other_feature'],  # optional
                        'dtype': 'float',  # optional
                        'description': 'What it does'  # optional
                    }
                }
        """
        self.registry.register_filters_from_dict(features_dict)
        print(f"[OK] Registered {len(features_dict)} filters in batch")

    def register_attributes_batch(self, features_dict: Dict[str, Dict]) -> None:
        """
        Register multiple attributes from dictionary.

        Args:
            features_dict: Dictionary with feature definitions (same format as filters)
        """
        self.registry.register_attributes_from_dict(features_dict)
        print(f"[OK] Registered {len(features_dict)} attributes in batch")

    # =========================================================================
    # OUTPUT CONFIGURATION
    # =========================================================================

    def set_output_attributes(self, attribute_names: List[str]) -> None:
        """
        Define which attributes should be in the final output.
        This triggers automatic dependency resolution.

        Args:
            attribute_names: List of attribute names to include in output

        Raises:
            ValueError: If attribute not found or dependencies cannot be resolved
        """
        # Validate all attributes exist
        for name in attribute_names:
            if name not in self.registry:
                raise ValueError(f"Attribute '{name}' not found in registry")

        self.output_attributes = attribute_names

        # Create execution plan
        self.execution_plan = self.resolver.get_execution_plan(attribute_names)

        print(f"\n[OK] Output attributes set: {len(attribute_names)} features")
        print(f"  Required features: {len(self.execution_plan['required_features'])}")
        print(f"  Required inputs: {len(self.execution_plan['required_inputs'])}")
        print(f"  Filters to execute: {len(self.execution_plan['filters'])}")
        print(f"  Attributes to execute: {len(self.execution_plan['attributes'])}")

    def get_required_inputs(self) -> List[str]:
        """
        Get list of required input columns based on selected output attributes.

        Returns:
            List of required input column names

        Raises:
            ValueError: If output attributes not set yet
        """
        if not self.execution_plan:
            raise ValueError("Output attributes not set. Call set_output_attributes() first.")

        return self.execution_plan['required_inputs']

    def print_execution_plan(self) -> None:
        """Print detailed execution plan."""
        if not self.execution_plan:
            print("[WARN] No execution plan. Call set_output_attributes() first.")
            return

        self.resolver.print_execution_plan(self.output_attributes)

    def visualize_dependencies(self) -> None:
        """Print dependency tree visualization."""
        if not self.output_attributes:
            print("[WARN] No output attributes set. Call set_output_attributes() first.")
            return

        print(self.resolver.visualize_dependencies(self.output_attributes))

    # =========================================================================
    # VALIDATION
    # =========================================================================

    def validate_registry(self) -> Tuple[bool, List[str]]:
        """
        Validate that all feature dependencies are valid.

        Returns:
            (is_valid, list_of_errors)
        """
        return validate_feature_dependencies(self.registry)

    def validate_input_data(self, df: pd.DataFrame) -> Tuple[bool, List[str]]:
        """
        Validate that input DataFrame has all required columns.

        Args:
            df: Input DataFrame

        Returns:
            (is_valid, list_of_missing_columns)
        """
        if not self.execution_plan:
            raise ValueError("Output attributes not set. Call set_output_attributes() first.")

        required = set(self.execution_plan['required_inputs'])
        available = set(df.columns)
        missing = required - available

        if missing:
            return False, list(missing)
        return True, []

    # =========================================================================
    # EXECUTION
    # =========================================================================

    def execute(self, df: pd.DataFrame,
                save_intermediates: Optional[bool] = None) -> Dict[str, pd.DataFrame]:
        """
        Execute complete pipeline with staged outputs.

        Pipeline stages:
        1. Preprocessing (validation, type conversion)
        2. Filters (row-level calculations)
        3. Attributes (aggregations)
        4. Output (final selected attributes)

        Args:
            df: Input DataFrame
            save_intermediates: Override config setting for saving intermediate files

        Returns:
            Dictionary with DataFrames from each stage:
            {
                'preprocessed': DataFrame,
                'filtered': DataFrame,
                'attributes': DataFrame,
                'output': DataFrame
            }

        Raises:
            ValueError: If validation fails or execution plan not ready
        """
        if not self.execution_plan:
            raise ValueError("Output attributes not set. Call set_output_attributes() first.")

        # Override save setting if provided
        save = save_intermediates if save_intermediates is not None else self.save_intermediates

        # Create output directories if saving
        if save:
            self._create_stage_directories()

        print("\n" + "="*70)
        print("EXECUTING PIPELINE")
        print("="*70)

        # Stage 1: Preprocessing
        print("\n[1/4] Preprocessing...")
        df_preprocessed = self._stage_preprocess(df)
        self._preprocessed_df = df_preprocessed

        if save:
            self._save_stage_output('01_preprocess', df_preprocessed, 'preprocessed.csv')
        print(f"  [OK] Preprocessed: {df_preprocessed.shape[0]} rows, {df_preprocessed.shape[1]} columns")

        # Stage 2: Filters (row-level)
        print("\n[2/4] Applying filters...")
        df_filtered = self._stage_filters(df_preprocessed)
        self._filtered_df = df_filtered

        if save:
            self._save_stage_output('02_features', df_filtered, 'filtered.csv')
        print(f"  [OK] Filters applied: {len(self.execution_plan['filters'])} filters")
        print(f"  [OK] Result: {df_filtered.shape[0]} rows, {df_filtered.shape[1]} columns")

        # Stage 3: Attributes (aggregations)
        print("\n[3/4] Computing attributes...")
        df_attributes = self._stage_attributes(df_filtered)
        self._attributes_df = df_attributes

        if save:
            self._save_stage_output('03_attributes', df_attributes, 'attributes.csv')
        print(f"  [OK] Attributes computed: {len(self.execution_plan['attributes'])} attributes")
        print(f"  [OK] Result: {df_attributes.shape[0]} rows, {df_attributes.shape[1]} columns")

        # Stage 4: Output (select requested attributes only)
        print("\n[4/4] Creating output...")
        df_output = self._stage_output(df_attributes)

        if save:
            self._save_stage_output('04_output', df_output, 'final_output.csv')
            self._save_execution_metadata()
        print(f"  [OK] Output created: {len(self.output_attributes)} attributes")
        print(f"  [OK] Final shape: {df_output.shape[0]} rows, {df_output.shape[1]} columns")

        print("\n" + "="*70)
        print("PIPELINE COMPLETE")
        print("="*70)

        if save:
            print(f"\nOutputs saved to: {self.run_dir}")

        return {
            'preprocessed': df_preprocessed,
            'filtered': df_filtered,
            'attributes': df_attributes,
            'output': df_output
        }

    def _stage_preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Stage 1: Preprocessing
        - Validate required inputs
        - Type conversion
        - Date parsing
        """
        df_prep = df.copy()

        # Validate required inputs
        is_valid, missing = self.validate_input_data(df_prep)
        if not is_valid:
            raise ValueError(f"Missing required input columns: {missing}")

        # Parse date column if exists
        if self.date_col in df_prep.columns:
            if not pd.api.types.is_datetime64_any_dtype(df_prep[self.date_col]):
                df_prep[self.date_col] = pd.to_datetime(df_prep[self.date_col], errors='coerce')

        return df_prep

    def _stage_filters(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Stage 2: Apply filters in execution order
        """
        df_filtered = df.copy()

        filter_names = self.execution_plan['filters']

        for filter_name in filter_names:
            feature = self.registry.get_feature(filter_name)
            if feature is None:
                raise ValueError(f"Filter '{filter_name}' not found")

            # Execute filter function
            df_filtered = feature.function(df_filtered)

        return df_filtered

    def _stage_attributes(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Stage 3: Compute attributes in execution order
        """
        df_attrs = df.copy()

        attribute_names = self.execution_plan['attributes']

        for attr_name in attribute_names:
            feature = self.registry.get_feature(attr_name)
            if feature is None:
                raise ValueError(f"Attribute '{attr_name}' not found")

            # Execute attribute function
            df_attrs = feature.function(df_attrs)

        return df_attrs

    def _stage_output(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Stage 4: Select only requested output attributes
        """
        # Get all output columns from requested attributes
        output_cols = []
        for attr_name in self.output_attributes:
            feature = self.registry.get_feature(attr_name)
            output_cols.extend(feature.outputs)

        # Also include key columns if they exist
        key_cols = []
        for potential_key in ['pin', 'id', 'transaction_id', self.date_col]:
            if potential_key in df.columns and potential_key not in output_cols:
                key_cols.append(potential_key)

        final_cols = key_cols + output_cols

        # Select only available columns
        available_cols = [col for col in final_cols if col in df.columns]

        return df[available_cols].copy()

    # =========================================================================
    # OUTPUT MANAGEMENT
    # =========================================================================

    def _create_stage_directories(self) -> None:
        """Create directory structure for staged outputs."""
        stages = ['01_preprocess', '02_features', '03_attributes', '04_output']

        for stage in stages:
            stage_dir = self.run_dir / stage
            stage_dir.mkdir(parents=True, exist_ok=True)

    def _save_stage_output(self, stage: str, df: pd.DataFrame, filename: str) -> None:
        """Save DataFrame to stage directory."""
        output_path = self.run_dir / stage / filename

        if filename.endswith('.csv'):
            df.to_csv(output_path, index=False)
        elif filename.endswith('.parquet'):
            try:
                df.to_parquet(output_path, index=False)
            except ImportError:
                # Fall back to CSV if parquet not available
                csv_path = output_path.with_suffix('.csv')
                df.to_csv(csv_path, index=False)
                print(f"  [INFO] Parquet not available, saved as CSV: {csv_path.name}")
        else:
            raise ValueError(f"Unsupported file format: {filename}")

    def _save_execution_metadata(self) -> None:
        """Save execution metadata as JSON."""
        metadata = {
            'client_name': self.client_name,
            'model_name': self.model_name,
            'run_timestamp': self.run_timestamp,
            'output_attributes': self.output_attributes,
            'execution_plan': {
                'required_features': self.execution_plan['required_features'],
                'required_inputs': self.execution_plan['required_inputs'],
                'execution_order': self.execution_plan['execution_order'],
                'filters': self.execution_plan['filters'],
                'attributes': self.execution_plan['attributes']
            },
            'config': self.config
        }

        metadata_path = self.run_dir / 'execution_metadata.json'
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)

    # =========================================================================
    # UTILITY METHODS
    # =========================================================================

    def list_registered_features(self, category: Optional[str] = None) -> List[str]:
        """
        List all registered features.

        Args:
            category: Filter by category ('filter' or 'attribute'), or None for all

        Returns:
            List of feature names
        """
        if category == 'filter':
            return list(self.registry.filters.keys())
        elif category == 'attribute':
            return list(self.registry.attributes.keys())
        else:
            return self.registry.list_all()

    def get_feature_info(self, name: str) -> Optional[Dict]:
        """
        Get detailed information about a feature.

        Args:
            name: Feature name

        Returns:
            Dictionary with feature metadata or None if not found
        """
        feature = self.registry.get_feature(name)
        if feature is None:
            return None

        return {
            'name': feature.name,
            'category': feature.category,
            'inputs': feature.inputs,
            'outputs': feature.outputs,
            'depends_on': feature.depends_on,
            'dtype': feature.dtype,
            'description': feature.description
        }

    def print_summary(self) -> None:
        """Print summary of driver configuration and state."""
        print("\n" + "="*70)
        print("MODEL DRIVER SUMMARY")
        print("="*70)
        print(f"\nClient: {self.client_name}")
        print(f"Model: {self.model_name}")
        print(f"Output base: {self.output_base}")
        print(f"Run timestamp: {self.run_timestamp}")

        print(f"\nRegistered Features:")
        print(f"  Filters: {len(self.registry.filters)}")
        print(f"  Attributes: {len(self.registry.attributes)}")
        print(f"  Total: {len(self.registry.list_all())}")

        if self.output_attributes:
            print(f"\nOutput Configuration:")
            print(f"  Output attributes: {len(self.output_attributes)}")
            print(f"  Required inputs: {len(self.execution_plan['required_inputs'])}")
            print(f"  Filters to execute: {len(self.execution_plan['filters'])}")
            print(f"  Attributes to execute: {len(self.execution_plan['attributes'])}")
        else:
            print("\n[WARN] Output attributes not configured yet")

        print("="*70 + "\n")
