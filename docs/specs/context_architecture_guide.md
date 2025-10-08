# GabeDA Context-Based Architecture Guide

## Overview

This document describes the new **Context-Based Execution Architecture** for GabeDA, replacing the previous linear pipeline approach. This architecture solves key limitations:

1. ✅ **Multiple outputs per step**: Handle both filters and attributes DataFrames
2. ✅ **Dynamic configuration management**: Separate user config from runtime metadata
3. ✅ **Explicit state management**: Named datasets accessible throughout execution
4. ✅ **Scalable to 6 models**: Clean orchestration of the complete analytics pipeline

---

## Architecture Components

### 1. GabedaContext (`src/gabeda_context.py`)

**Purpose**: Stateful execution context managing the entire analytics workflow.

**Key Features**:
- **User Config**: Immutable user-provided configuration
- **Runtime Config**: Dynamic metadata per model (from `get_dependencies()`)
- **Datasets**: Named DataFrames at different pipeline stages
- **Models**: Model outputs with metadata
- **History**: Execution log for debugging and auditing

**Usage**:
```python
from src.gabeda_context import GabedaContext

# Initialize with user configuration
ctx = GabedaContext(khujta_cfg)

# Store datasets
ctx.set_dataset('preprocessed', preprocessed_df)

# Retrieve datasets
filters_df = ctx.get_dataset('product_stats_filters')
attrs_df = ctx.get_model_attrs('product_stats')

# Save to disk
ctx.save_dataset('product_stats_filters', 'output/filters', format='csv')

# View execution summary
ctx.print_summary()
```

---

### 2. ModelExecutor (`src/model_executor.py`)

**Purpose**: Executes individual models within a GabedaContext.

**Key Features**:
- Handles `get_dependencies()` for dynamic configuration
- Executes `calc_datasets()` for filters + attributes calculation
- Stores results back into context with proper naming
- Manages runtime config separately from user config

**Usage**:
```python
from src.model_executor import ModelExecutor

# Define model configuration
cfg_product = {
    'model_name': 'product_stats',
    'group_by': ['in_product'],
    'features': {
        'hour': hour,
        'total_transacciones': total_transacciones,
        'total_unidades_vendidas': total_unidades_vendidas,
    },
    'output_cols': ['hour', 'total_transacciones', 'total_unidades_vendidas']
}

# Execute model
executor = ModelExecutor(cfg_product)
results = executor.execute(ctx, input_dataset_name='preprocessed')

# Access results
filters_df = results['filters']  # Row-level calculations
attrs_df = results['attrs']      # Aggregated metrics
runtime_cfg = results['config']  # Enhanced configuration
```

---

### 3. ModelOrchestrator (`src/model_executor.py`)

**Purpose**: Orchestrates multiple models in sequence or parallel.

**Key Features**:
- Registry pattern for model management
- Execute specific models or all registered models
- Shared context across all executions
- Centralized execution summary

**Usage**:
```python
from src.model_executor import ModelOrchestrator

# Initialize orchestrator
orchestrator = ModelOrchestrator(ctx)

# Register models (6-model pipeline)
orchestrator.register_model(ModelExecutor(cfg_product))
orchestrator.register_model(ModelExecutor(cfg_customer))
orchestrator.register_model(ModelExecutor(cfg_time))
orchestrator.register_model(ModelExecutor(cfg_basket))
orchestrator.register_model(ModelExecutor(cfg_business))

# Execute all
orchestrator.execute_all(input_dataset_name='preprocessed')

# Or execute individually
orchestrator.execute_model('product_stats', input_dataset_name='preprocessed')
```

---

## Complete Workflow Example

### Step 1: Configuration

```python
khujta_cfg = {
    # Project settings
    'input_file': 'data/test_client/transactions.csv',
    'out_dir': 'data',
    'client': 'test_client',

    # Feature store config
    'fidx_config': {'type': 'local', 'path': 'feature_store'},

    # Column mappings
    'column_mappings': {
        'in_dt': 'fecha',
        'in_trans_id': 'trans_id',
        'in_product': 'producto',
        # ... more mappings
    },

    # Other settings
    'analysis_dt': '2024-12-02',
    'language': 'EN',
    'log_level': 'DEBUG',
}
```

### Step 2: Initialize Context

```python
from src.gabeda_context import GabedaContext
from src.preprocessing import preprocess_data

# Create context
ctx = GabedaContext(khujta_cfg)

# Load and preprocess data
raw_data = pd.read_csv(khujta_cfg['input_file'])
preprocessed_df = preprocess_data(raw_data, khujta_cfg)

# Store in context
ctx.set_dataset('raw', raw_data)
ctx.set_dataset('preprocessed', preprocessed_df)
```

### Step 3: Define Feature Functions

```python
import numpy as np
import pandas as pd

# Filter function (row-level)
def hour(in_dt):
    return pd.Timestamp(in_dt).hour

# Aggregate functions (group-level)
def total_transacciones(in_trans_id):
    return np.count_nonzero(in_trans_id)

def total_unidades_vendidas(in_quantity):
    return np.sum(in_quantity)
```

### Step 4: Execute Model

```python
from src.model_executor import ModelExecutor

# Configure model
cfg_product = {
    'model_name': 'product_stats',
    'group_by': ['in_product'],
    'features': {
        'hour': hour,
        'total_transacciones': total_transacciones,
        'total_unidades_vendidas': total_unidades_vendidas,
    },
    'output_cols': ['hour', 'total_transacciones', 'total_unidades_vendidas']
}

# Execute
executor = ModelExecutor(cfg_product)
results = executor.execute(ctx, input_dataset_name='preprocessed')

print(f"Filters shape: {results['filters'].shape}")
print(f"Attrs shape: {results['attrs'].shape}")
```

### Step 5: Access Results

```python
# Method 1: From results dict
filters_df = results['filters']
attrs_df = results['attrs']

# Method 2: From context by name
filters_df = ctx.get_dataset('product_stats_filters')
attrs_df = ctx.get_dataset('product_stats_attrs')

# Method 3: Convenience methods
filters_df = ctx.get_model_filters('product_stats')
attrs_df = ctx.get_model_attrs('product_stats')
```

### Step 6: Save and Inspect

```python
# Save datasets
ctx.save_dataset('product_stats_filters', 'output/product_filters', format='csv')
ctx.save_dataset('product_stats_attrs', 'output/product_attrs', format='parquet')

# View execution summary
ctx.print_summary()
# Output:
# ================================================================================
# GabeDA Execution Summary - Run ID: test_client_20251008_115624
# ================================================================================
#
# Datasets (4):
#   - raw: (100, 10)
#   - preprocessed: (100, 11)
#   - product_stats_filters: (100, 12)
#   - product_stats_attrs: (15, 3)
#
# Models Executed (1):
#   - product_stats: ['product_stats_filters', 'product_stats_attrs']
#
# Total Steps: 5
# ================================================================================
```

---

## Comparison: Old vs New Architecture

### Old Pipeline Approach

**Limitations**:
```python
# Single DataFrame flow
pipeline = (Pipeline(config)
    .add_step("preprocessing", preprocess_data)
    .add_step("filter_calculation", calculate_filters)
    .add_step("aggregation", aggregate_data))

result = pipeline.run()  # Only returns ONE dataframe
```

❌ Only one DataFrame passed between steps
❌ Config becomes bloated with runtime metadata
❌ Can't access intermediate results
❌ Hard to handle dual outputs (filters + attrs)

### New Context-Based Approach

**Advantages**:
```python
# Multiple outputs, explicit state
ctx = GabedaContext(user_config)
ctx.set_dataset('preprocessed', preprocessed_df)

executor = ModelExecutor(model_config)
results = executor.execute(ctx)  # Returns dict with filters + attrs

# Access both outputs
filters = ctx.get_model_filters('product_stats')
attrs = ctx.get_model_attrs('product_stats')
```

✅ Multiple DataFrames managed explicitly
✅ User config separated from runtime config
✅ All intermediate results accessible
✅ Dual outputs (filters + attrs) handled naturally
✅ Easy to inspect, debug, and save at any stage

---

## 6-Model Pipeline Integration

The architecture aligns perfectly with the 6-model GabeDA pipeline:

```python
# Initialize context
ctx = GabedaContext(khujta_cfg)
ctx.set_dataset('preprocessed', preprocessed_df)

# Model 1: Transaction Enrichment (filters only)
executor1 = ModelExecutor(cfg_transaction_enrichment)
executor1.execute(ctx)

# Model 2: Product-Level Analysis
executor2 = ModelExecutor(cfg_product)
executor2.execute(ctx)

# Model 3: Customer-Level Analysis
executor3 = ModelExecutor(cfg_customer)
executor3.execute(ctx)

# Model 4: Time-Period Analysis
executor4 = ModelExecutor(cfg_time)
executor4.execute(ctx)

# Model 5: Basket Analysis
executor5 = ModelExecutor(cfg_basket)
executor5.execute(ctx)

# Model 6: Business Overview (uses outputs from 2-5)
product_attrs = ctx.get_model_attrs('product_stats')
customer_attrs = ctx.get_model_attrs('customer_stats')
time_attrs = ctx.get_model_attrs('time_stats')

executor6 = ModelExecutor(cfg_business)
# ... consolidate insights from previous models
```

---

## Advanced Features

### 1. Metadata Tracking

```python
# Store dataset with metadata
ctx.set_dataset('product_stats_filters', filters_df, metadata={
    'rows_added': 8,
    'columns_added': ['hour'],
    'execution_time': 0.5
})

# Access execution history
history = ctx.get_execution_summary()
print(history['history'])
```

### 2. Custom Input Datasets

```python
# Use output from one model as input to another
executor_product.execute(ctx, input_dataset_name='preprocessed')
executor_business.execute(ctx, input_dataset_name='product_stats_attrs')
```

### 3. Configuration Access

```python
# Get runtime config generated by get_dependencies()
runtime_cfg = ctx.get_runtime_config('product_stats')
print(runtime_cfg['exec_seq'])  # Execution sequence
print(runtime_cfg['in_cols'])   # Input columns resolved
```

### 4. Bulk Save

```python
# Save all model outputs
for model_name in ctx.models.keys():
    ctx.save_dataset(f'{model_name}_filters', f'output/{model_name}_filters')
    ctx.save_dataset(f'{model_name}_attrs', f'output/{model_name}_attrs')
```

---

## Migration Guide

### From Old Pipeline Code

**Before** (conf_step_pipeline.py):
```python
pipeline = Pipeline(config)
pipeline.add_step("preprocessing", preprocess_data)
pipeline.add_step("filter_calculation", calculate_filters)
result = pipeline.run()
```

**After** (New Architecture):
```python
ctx = GabedaContext(config)
ctx.set_dataset('preprocessed', preprocess_data(raw_data, config))

executor = ModelExecutor(model_config)
results = executor.execute(ctx)

filters = results['filters']
attrs = results['attrs']
```

### From Legacy Khujta Class

**Before**:
```python
khujta = Khujta(config)
khujta.add_step("preprocessing", preprocess_data)
result = khujta.run()
```

**After**:
```python
ctx = GabedaContext(config)
ctx.set_dataset('preprocessed', preprocessed_df)

# Use ModelExecutor for each analytical model
executor = ModelExecutor(model_config)
executor.execute(ctx)
```

---

## Best Practices

1. **Naming Convention**: Use `{model_name}_{output_type}` for datasets
   - `product_stats_filters`
   - `product_stats_attrs`
   - `customer_rfm_attrs`

2. **Config Management**:
   - Keep user config minimal and immutable
   - Let runtime config be generated dynamically
   - Don't pollute user config with execution metadata

3. **Dataset Lifecycle**:
   - Store raw data first
   - Store preprocessed data
   - Each model creates filters and/or attrs datasets
   - Business model consumes attrs from other models

4. **Error Handling**:
   ```python
   try:
       executor.execute(ctx)
   except Exception as e:
       logger.error(f"Model failed: {e}")
       # Context preserves partial results
       ctx.print_summary()  # See what completed
   ```

5. **Memory Management**:
   - Save and clear large datasets when no longer needed
   - Use parquet format for large DataFrames
   - Monitor context state with `ctx.print_summary()`

---

## Testing

See [play.ipynb](../play.ipynb) for complete working examples.

Run tests:
```bash
jupyter nbconvert --to notebook --execute play.ipynb --output play_test.ipynb
```

---

## Files Created

- **src/gabeda_context.py**: GabedaContext class
- **src/model_executor.py**: ModelExecutor and ModelOrchestrator classes
- **play.ipynb**: Updated with working examples
- **docs/context_architecture_guide.md**: This document

---

## Next Steps

1. ✅ Context and Executor classes created
2. ✅ Working example in play.ipynb
3. ⏳ Migrate remaining 5 models to new architecture
4. ⏳ Add model-specific configurations
5. ⏳ Implement parallel execution for models 2-5
6. ⏳ Create business overview model that consumes attrs

---

## FAQ

**Q: Can I still use the old pipeline approach?**
A: Yes, `src/khujta.py` still exists for backwards compatibility, but the new architecture is recommended.

**Q: How do I handle dependencies between models?**
A: Use `ctx.get_model_attrs()` to get aggregated output from one model and pass it as input to another.

**Q: What if a model only produces filters (no aggregations)?**
A: The executor handles this - `attrs` will be None. Access with `ctx.get_model_filters()`.

**Q: Can I execute models in parallel?**
A: Yes, models 2-5 can run in parallel since they all depend only on model 1. Use threading/multiprocessing with separate executors sharing the same context.

**Q: How do I debug configuration issues?**
A: Check `ctx.get_runtime_config(model_name)` to see resolved dependencies, execution sequence, and input columns.

---

## Support

For questions or issues:
- Check [99_architecture.md](specs/99_architecture.md) for the 6-model architecture
- See [play.ipynb](../play.ipynb) for working examples
- Review logs in `logs/` directory for execution details
