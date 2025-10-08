"""
Model Executor for GabeDA Analytics

This module provides the ModelExecutor class that executes individual models
within the GabedaContext framework. It handles dynamic configuration resolution,
dependency management, and multi-output handling.

The executor integrates with:
- src.fidx.get_dependencies: For resolving feature dependencies
- src.modeling.calc_datasets: For calculating filters and attributes
"""

import pandas as pd
from typing import Dict, Any, Optional, List
from src.logger import get_logger
from src.gabeda_context import GabedaContext
from src.fidx import get_dependencies
from src.model_ops import calc_datasets

logger = get_logger(__name__)


class ModelExecutor:
    """
    Executes a single GabeDA model within a GabedaContext.

    Handles:
    - Dynamic configuration with get_dependencies()
    - Dual output (filters + attributes) from calc_datasets()
    - Integration with GabedaContext for state management

    Attributes:
        model_config (Dict): Base model configuration
        model_name (str): Model identifier
    """

    def __init__(self, model_config: Dict[str, Any]):
        """
        Initialize ModelExecutor with model configuration.

        Args:
            model_config: Dictionary containing:
                - model_name: Model identifier (required)
                - group_by: List of grouping columns (required for aggregations)
                - features: Dict of feature definitions (optional if in feature store)
                - output_cols: List of desired output columns (optional)
                - Any other model-specific configuration
        """
        if 'model_name' not in model_config:
            raise ValueError("model_config must contain 'model_name'")

        self.model_config = model_config.copy()
        self.model_name = self.model_config['model_name']

        logger.info(f"ModelExecutor initialized: {self.model_name}")

    def execute(
        self,
        ctx: GabedaContext,
        input_dataset_name: str = 'preprocessed',
        resolve_dependencies: bool = True
    ) -> Dict[str, pd.DataFrame]:
        """
        Execute model using GabedaContext.

        Args:
            ctx: GabedaContext instance
            input_dataset_name: Name of input dataset in context
            resolve_dependencies: Whether to call get_dependencies()

        Returns:
            Dictionary with 'filters' and 'attrs' DataFrames

        Raises:
            ValueError: If input dataset not found in context
        """
        logger.info(f"Executing model: {self.model_name}")

        # Get input data from context
        input_df = ctx.get_dataset(input_dataset_name)
        if input_df is None:
            raise ValueError(
                f"Input dataset '{input_dataset_name}' not found in context. "
                f"Available: {ctx.list_datasets()}"
            )

        logger.debug(f"Input dataset: {input_dataset_name} with shape {input_df.shape}")

        # Prepare configuration
        cfg_model = self._prepare_config(ctx, resolve_dependencies)

        # Execute calculation
        try:
            filters_df, attrs_df = calc_datasets(input_df, cfg_model)

            logger.info(
                f"Model {self.model_name} completed: "
                f"filters={filters_df.shape if filters_df is not None else 'None'}, "
                f"attrs={attrs_df.shape if attrs_df is not None else 'None'}"
            )

            # Package results
            results = {
                'filters': filters_df,
                'attrs': attrs_df,
                'config': cfg_model
            }

            # Store in context
            ctx.set_model_output(self.model_name, results)

            return results

        except Exception as e:
            logger.error(f"Error executing model {self.model_name}: {e}", exc_info=True)
            raise

    def _prepare_config(self, ctx: GabedaContext, resolve_dependencies: bool) -> Dict:
        """
        Prepare model configuration, optionally resolving dependencies.

        Args:
            ctx: GabedaContext instance
            resolve_dependencies: Whether to call get_dependencies()

        Returns:
            Enhanced configuration dictionary
        """
        cfg_model = self.model_config.copy()

        # Resolve dependencies if requested
        if resolve_dependencies:
            # Determine output columns
            output_cols = cfg_model.get('output_cols')
            if output_cols is None:
                # If not specified, use all features as output
                if 'features' in cfg_model:
                    output_cols = list(cfg_model['features'].keys())
                else:
                    raise ValueError(
                        f"Model {self.model_name}: must specify 'output_cols' or 'features'"
                    )

            # Get fidx configuration from user config
            fidx_config = ctx.user_config.get('fidx_config')
            if fidx_config is None:
                # Default to local feature store
                fidx_config = {'type': 'local', 'path': 'feature_index'}
                logger.warning(
                    f"No fidx_config in user_config, using default: {fidx_config}"
                )

            # Pass available_cols from preprocessing to cfg_model
            if 'available_cols' in ctx.user_config:
                cfg_model['available_cols'] = ctx.user_config['available_cols']
                logger.debug(f"Available columns: {cfg_model['available_cols']}")

            if 'missing_cols' in ctx.user_config:
                cfg_model['missing_cols'] = ctx.user_config['missing_cols']
                logger.debug(f"Missing columns: {cfg_model['missing_cols']}")

            # Resolve dependencies
            logger.debug(f"Resolving dependencies for {self.model_name}")
            cfg_model = get_dependencies(
                fidx_config,
                self.model_name,
                cfg_model,
                output_cols
            )

            logger.info(
                f"Dependencies resolved for {self.model_name}: "
                f"in_cols={cfg_model.get('in_cols')}, "
                f"exec_seq={cfg_model.get('exec_seq')}"
            )

        return cfg_model

    def execute_and_return_filters(
        self,
        ctx: GabedaContext,
        input_dataset_name: str = 'preprocessed'
    ) -> pd.DataFrame:
        """
        Convenience method: Execute and return only filters DataFrame.

        Args:
            ctx: GabedaContext instance
            input_dataset_name: Name of input dataset in context

        Returns:
            Filters DataFrame
        """
        results = self.execute(ctx, input_dataset_name)
        return results['filters']

    def execute_and_return_attrs(
        self,
        ctx: GabedaContext,
        input_dataset_name: str = 'preprocessed'
    ) -> Optional[pd.DataFrame]:
        """
        Convenience method: Execute and return only attributes DataFrame.

        Args:
            ctx: GabedaContext instance
            input_dataset_name: Name of input dataset in context

        Returns:
            Attributes DataFrame or None
        """
        results = self.execute(ctx, input_dataset_name)
        return results['attrs']

    def __repr__(self):
        """String representation."""
        return f"ModelExecutor(model='{self.model_name}')"


class ModelOrchestrator:
    """
    Orchestrates multiple model executions in sequence or parallel.

    This class manages the execution of the 6 GabeDA models:
    1. Transaction Enrichment (filters only)
    2. Product-Level Analysis
    3. Customer-Level Analysis
    4. Time-Period Analysis
    5. Basket Analysis
    6. Business Overview

    Attributes:
        ctx (GabedaContext): Shared execution context
        executors (Dict[str, ModelExecutor]): Registered model executors
    """

    def __init__(self, ctx: GabedaContext):
        """
        Initialize orchestrator with context.

        Args:
            ctx: GabedaContext instance
        """
        self.ctx = ctx
        self.executors: Dict[str, ModelExecutor] = {}
        logger.info("ModelOrchestrator initialized")

    def register_model(self, executor: ModelExecutor) -> 'ModelOrchestrator':
        """
        Register a model executor.

        Args:
            executor: ModelExecutor instance

        Returns:
            Self for chaining
        """
        self.executors[executor.model_name] = executor
        logger.info(f"Model registered: {executor.model_name}")
        return self

    def execute_model(
        self,
        model_name: str,
        input_dataset_name: str = 'preprocessed'
    ) -> Dict[str, pd.DataFrame]:
        """
        Execute a specific registered model.

        Args:
            model_name: Model identifier
            input_dataset_name: Input dataset name

        Returns:
            Dictionary with filters and attrs DataFrames

        Raises:
            KeyError: If model not registered
        """
        if model_name not in self.executors:
            raise KeyError(
                f"Model '{model_name}' not registered. "
                f"Available: {list(self.executors.keys())}"
            )

        executor = self.executors[model_name]
        return executor.execute(self.ctx, input_dataset_name)

    def execute_all(
        self,
        input_dataset_name: str = 'preprocessed',
        model_sequence: Optional[List[str]] = None
    ):
        """
        Execute all registered models in sequence.

        Args:
            input_dataset_name: Input dataset name
            model_sequence: Optional custom execution order (defaults to registration order)
        """
        if model_sequence is None:
            model_sequence = list(self.executors.keys())

        logger.info(f"Executing {len(model_sequence)} models in sequence")

        for model_name in model_sequence:
            try:
                self.execute_model(model_name, input_dataset_name)
            except Exception as e:
                logger.error(f"Failed to execute model {model_name}: {e}")
                # Continue with other models or raise?
                raise

        logger.info("All models executed successfully")

    def get_results_summary(self) -> Dict:
        """
        Get summary of all executed models.

        Returns:
            Dictionary with execution summary
        """
        return self.ctx.get_execution_summary()

    def __repr__(self):
        """String representation."""
        return f"ModelOrchestrator(models={list(self.executors.keys())})"
