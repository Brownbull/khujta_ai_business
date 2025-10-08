"""
GabeDA Context-Based Execution Architecture

This module implements the context-based approach for managing the 6-model
analytics pipeline. It separates user configuration from runtime metadata
and allows handling multiple DataFrames throughout the execution flow.

Architecture:
    GabedaContext: Stateful execution context managing datasets and configs
    ModelExecutor: Executes individual models using the context
"""

import pandas as pd
from typing import Dict, Any, Tuple, Optional
from datetime import datetime
from src.logger import get_logger

logger = get_logger(__name__)


class GabedaContext:
    """
    Manages execution state across the 6-model GabeDA pipeline.

    Separates concerns:
    - user_config: Immutable configuration provided by user
    - runtime_config: Dynamic metadata generated during execution
    - datasets: Named DataFrames at different stages
    - models: Model outputs with metadata
    - history: Execution log for debugging

    Attributes:
        user_config (Dict): User-provided configuration (immutable)
        runtime_config (Dict): Runtime metadata per model
        datasets (Dict[str, pd.DataFrame]): Named DataFrames
        models (Dict[str, Dict]): Model outputs with metadata
        history (List[Tuple]): Execution history log
    """

    def __init__(self, user_config: Dict[str, Any]):
        """
        Initialize GabedaContext with user configuration.

        Args:
            user_config: User-provided configuration dictionary
        """
        self.user_config = user_config.copy()  # Immutable copy
        self.runtime_config: Dict[str, Dict] = {}  # Model-specific runtime configs
        self.datasets: Dict[str, pd.DataFrame] = {}  # Named DataFrames
        self.models: Dict[str, Dict] = {}  # Model outputs
        self.history: list = []  # Execution log

        # Add runtime variables
        self.now = datetime.now()
        self.run_id = f"{user_config.get('client', 'unknown')}_{self.now.strftime('%Y%m%d_%H%M%S')}"

        logger.info(f"GabedaContext initialized - run_id: {self.run_id}")

    def set_dataset(self, name: str, df: pd.DataFrame, metadata: Optional[Dict] = None):
        """
        Store a named DataFrame in the context.

        Args:
            name: Dataset identifier (e.g., 'preprocessed', 'product_filters')
            df: DataFrame to store
            metadata: Optional metadata about the dataset
        """
        if df is None:
            logger.warning(f"Attempting to set None dataset: {name}")
            return

        self.datasets[name] = df
        log_entry = {
            'action': 'set_dataset',
            'name': name,
            'shape': df.shape,
            'columns': len(df.columns),
            'timestamp': datetime.now().isoformat()
        }
        if metadata:
            log_entry['metadata'] = metadata

        self.history.append(log_entry)
        logger.debug(f"Dataset stored: {name} with shape {df.shape}")

    def get_dataset(self, name: str) -> Optional[pd.DataFrame]:
        """
        Retrieve a named DataFrame from the context.

        Args:
            name: Dataset identifier

        Returns:
            DataFrame if found, None otherwise
        """
        df = self.datasets.get(name)
        if df is None:
            logger.warning(f"Dataset not found: {name}. Available: {list(self.datasets.keys())}")
        return df

    def list_datasets(self) -> list:
        """
        List all available datasets.

        Returns:
            List of dataset names
        """
        return list(self.datasets.keys())

    def set_model_output(self, model_name: str, outputs: Dict[str, Any]):
        """
        Store model execution output with metadata.

        Args:
            model_name: Model identifier (e.g., 'product_stats', 'customer_rfm')
            outputs: Dictionary containing:
                - 'filters': DataFrame with row-level calculations (optional)
                - 'attrs': DataFrame with aggregated metrics (optional)
                - 'config': Runtime configuration used
                - 'metadata': Additional metadata (optional)
        """
        self.models[model_name] = {
            'outputs': outputs,
            'timestamp': datetime.now().isoformat(),
            'datasets_generated': []
        }

        # Store datasets with model namespace
        if 'filters' in outputs and outputs['filters'] is not None:
            dataset_name = f"{model_name}_filters"
            self.set_dataset(dataset_name, outputs['filters'])
            self.models[model_name]['datasets_generated'].append(dataset_name)

        if 'attrs' in outputs and outputs['attrs'] is not None:
            dataset_name = f"{model_name}_attrs"
            self.set_dataset(dataset_name, outputs['attrs'])
            self.models[model_name]['datasets_generated'].append(dataset_name)

        # Store runtime config if provided
        if 'config' in outputs:
            self.runtime_config[model_name] = outputs['config']

        self.history.append({
            'action': 'model_executed',
            'model': model_name,
            'datasets': self.models[model_name]['datasets_generated'],
            'timestamp': datetime.now().isoformat()
        })

        logger.info(f"Model output stored: {model_name} -> {self.models[model_name]['datasets_generated']}")

    def get_model_output(self, model_name: str) -> Optional[Dict]:
        """
        Retrieve model execution output.

        Args:
            model_name: Model identifier

        Returns:
            Dictionary with model outputs or None
        """
        return self.models.get(model_name)

    def get_model_filters(self, model_name: str) -> Optional[pd.DataFrame]:
        """
        Convenience method to get filters DataFrame from a model.

        Args:
            model_name: Model identifier

        Returns:
            Filters DataFrame or None
        """
        return self.get_dataset(f"{model_name}_filters")

    def get_model_attrs(self, model_name: str) -> Optional[pd.DataFrame]:
        """
        Convenience method to get attributes DataFrame from a model.

        Args:
            model_name: Model identifier

        Returns:
            Attributes DataFrame or None
        """
        return self.get_dataset(f"{model_name}_attrs")

    def merge_runtime_config(self, model_name: str, config_updates: Dict):
        """
        Add or update runtime configuration for a specific model.

        Args:
            model_name: Model identifier
            config_updates: Configuration dictionary to merge
        """
        if model_name not in self.runtime_config:
            self.runtime_config[model_name] = {}

        self.runtime_config[model_name].update(config_updates)
        logger.debug(f"Runtime config updated for {model_name}")

    def get_runtime_config(self, model_name: str) -> Optional[Dict]:
        """
        Get runtime configuration for a specific model.

        Args:
            model_name: Model identifier

        Returns:
            Runtime config dictionary or None
        """
        return self.runtime_config.get(model_name)

    def save_dataset(self, name: str, output_path: str, format: str = 'csv'):
        """
        Save a dataset to disk.

        Args:
            name: Dataset name to save
            output_path: Output file path (without extension)
            format: File format ('csv', 'parquet', 'excel')
        """
        df = self.get_dataset(name)
        if df is None:
            logger.error(f"Cannot save dataset {name}: not found")
            return

        try:
            if format == 'csv':
                df.to_csv(f"{output_path}.csv", index=False)
            elif format == 'parquet':
                df.to_parquet(f"{output_path}.parquet", index=False)
            elif format == 'excel':
                df.to_excel(f"{output_path}.xlsx", index=False)
            else:
                raise ValueError(f"Unsupported format: {format}")

            logger.info(f"Dataset {name} saved to {output_path}.{format}")
        except Exception as e:
            logger.error(f"Error saving dataset {name}: {e}")

    def get_execution_summary(self) -> Dict:
        """
        Get summary of execution history.

        Returns:
            Dictionary with execution statistics
        """
        return {
            'run_id': self.run_id,
            'total_datasets': len(self.datasets),
            'datasets': list(self.datasets.keys()),
            'total_models': len(self.models),
            'models_executed': list(self.models.keys()),
            'execution_steps': len(self.history),
            'history': self.history
        }

    def print_summary(self):
        """Print execution summary to console."""
        summary = self.get_execution_summary()
        print("\n" + "="*80)
        print(f"GabeDA Execution Summary - Run ID: {summary['run_id']}")
        print("="*80)
        print(f"\nDatasets ({summary['total_datasets']}):")
        for ds_name in summary['datasets']:
            df = self.datasets[ds_name]
            print(f"  - {ds_name}: {df.shape}")

        print(f"\nModels Executed ({summary['total_models']}):")
        for model_name in summary['models_executed']:
            model_info = self.models[model_name]
            print(f"  - {model_name}: {model_info['datasets_generated']}")

        print(f"\nTotal Steps: {summary['execution_steps']}")
        print("="*80 + "\n")

    def __repr__(self):
        """String representation of context."""
        return (f"GabedaContext(run_id='{self.run_id}', "
                f"datasets={len(self.datasets)}, "
                f"models={len(self.models)})")
