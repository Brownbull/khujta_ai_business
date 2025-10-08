# GabeDA Context-Based Architecture - Implementation Summary

## What Was Built

Implemented **Option 1: Context-Based Execution Manager** to replace the linear pipeline approach.

### Core Components

1. **GabedaContext** ([src/gabeda_context.py](src/gabeda_context.py))
   - Manages execution state across the 6-model pipeline
   - Separates user config from runtime metadata
   - Stores multiple named DataFrames (raw, preprocessed, filters, attrs)
   - Tracks execution history and provides summaries
   - Supports saving datasets in multiple formats (csv, parquet, excel)

2. **ModelExecutor** ([src/model_executor.py](src/model_executor.py))
   - Executes individual models within a GabedaContext
   - Handles dynamic config resolution via `get_dependencies()`
   - Manages dual outputs (filters + attributes) from `calc_datasets()`
   - Stores results back into context with proper naming conventions

3. **ModelOrchestrator** ([src/model_executor.py](src/model_executor.py))
   - Registry pattern for managing multiple models
   - Executes models in sequence or individually
   - Provides centralized execution summary

---

## Problem Solved

### Before (Linear Pipeline)
```python
pipeline = Pipeline(config)
    .add_step("preprocessing", preprocess_data)
    .add_step("calculation", calc_datasets)

result = pipeline.run()  # ❌ Only ONE dataframe
```

**Issues**:
- ❌ Can't handle dual outputs (filters + attrs)
- ❌ Config becomes bloated with runtime metadata
- ❌ Can't access intermediate results
- ❌ Hard to inspect/debug/save at each stage

### After (Context-Based)
```python
ctx = GabedaContext(user_config)
ctx.set_dataset('preprocessed', preprocessed_df)

executor = ModelExecutor(model_config)
results = executor.execute(ctx)

# ✅ Access both outputs
filters = ctx.get_model_filters('product_stats')
attrs = ctx.get_model_attrs('product_stats')

# ✅ Save intermediate results
ctx.save_dataset('product_stats_filters', 'output/filters')
ctx.print_summary()  # ✅ View execution state
```

**Benefits**:
- ✅ Multiple DataFrames managed explicitly
- ✅ User config separated from runtime config
- ✅ All intermediate results accessible
- ✅ Easy to inspect, debug, and save at any stage
- ✅ Scales to 6-model architecture naturally

---

## Quick Start

### 1. Basic Usage

```python
from src.gabeda_context import GabedaContext
from src.model_executor import ModelExecutor

# Initialize context
ctx = GabedaContext(khujta_cfg)
ctx.set_dataset('preprocessed', preprocessed_df)

# Configure model
cfg_product = {
    'model_name': 'product_stats',
    'group_by': ['in_product'],
    'features': {
        'hour': hour_func,
        'total_sales': total_sales_func,
    },
    'output_cols': ['hour', 'total_sales']
}

# Execute
executor = ModelExecutor(cfg_product)
results = executor.execute(ctx)

# Access results (3 ways)
filters = results['filters']                          # From results dict
filters = ctx.get_dataset('product_stats_filters')    # By name
filters = ctx.get_model_filters('product_stats')      # Convenience method
```

### 2. Multiple Models

```python
from src.model_executor import ModelOrchestrator

# Initialize orchestrator
orchestrator = ModelOrchestrator(ctx)

# Register models
orchestrator.register_model(ModelExecutor(cfg_product))
orchestrator.register_model(ModelExecutor(cfg_customer))
orchestrator.register_model(ModelExecutor(cfg_time))

# Execute all
orchestrator.execute_all(input_dataset_name='preprocessed')

# View summary
ctx.print_summary()
```

---

## Key Advantages for Your Use Case

### 1. Handles Dynamic Configs

`get_dependencies()` can dynamically enhance configs without polluting `khujta_cfg`:

```python
# User config stays clean
khujta_cfg = {
    'client': 'test_client',
    'fidx_config': {'type': 'local', 'path': 'feature_store'}
}

# Runtime config stored separately
executor.execute(ctx)  # Internally calls get_dependencies()
runtime_cfg = ctx.get_runtime_config('product_stats')
# Contains: in_cols, exec_seq, feature_funcs, etc.
```

### 2. Dual Output Handling

`calc_datasets()` returns both filters and attrs - both are stored:

```python
filters_df, attrs_df = calc_datasets(input_df, cfg_model)

# Context stores both
ctx.set_dataset('product_stats_filters', filters_df)
ctx.set_dataset('product_stats_attrs', attrs_df)

# Access either anytime
if need_row_level:
    df = ctx.get_model_filters('product_stats')
if need_aggregated:
    df = ctx.get_model_attrs('product_stats')
```

### 3. Flexible Data Flow

Use output from one model as input to another:

```python
# Model 2: Product analysis
executor_product.execute(ctx, input_dataset_name='preprocessed')

# Model 6: Business overview uses product attrs
product_attrs = ctx.get_model_attrs('product_stats')
customer_attrs = ctx.get_model_attrs('customer_stats')

# Combine and analyze
business_input = pd.merge(product_attrs, customer_attrs, ...)
ctx.set_dataset('business_input', business_input)
executor_business.execute(ctx, input_dataset_name='business_input')
```

---

## Files Created

| File | Description |
|------|-------------|
| [src/gabeda_context.py](src/gabeda_context.py) | GabedaContext class - state management |
| [src/model_executor.py](src/model_executor.py) | ModelExecutor and ModelOrchestrator classes |
| [docs/context_architecture_guide.md](docs/context_architecture_guide.md) | Comprehensive usage guide |
| [play.ipynb](play.ipynb) | Updated with working examples |
| [ARCHITECTURE_SUMMARY.md](ARCHITECTURE_SUMMARY.md) | This file |

---

## Testing

Tested successfully with `product_stats` model:

```bash
jupyter nbconvert --to notebook --execute play.ipynb --output play_test.ipynb
```

Results:
- ✅ Context initialized correctly
- ✅ Datasets stored and retrieved
- ✅ ModelExecutor executed successfully
- ✅ Filters (8x11) and Attrs (6x3) both generated
- ✅ Multiple access methods work
- ✅ Save functionality works
- ✅ Execution summary displays correctly

---

## Next Steps

### Immediate (Phase 1)
1. ✅ Context and Executor implemented
2. ✅ Working example with product_stats
3. ⏳ Migrate customer model to new architecture
4. ⏳ Migrate time-period model
5. ⏳ Migrate basket model

### Short-term (Phase 2)
6. ⏳ Create business overview model (consolidates 2-5)
7. ⏳ Add parallel execution support for models 2-5
8. ⏳ Create template configs for all 6 models
9. ⏳ Add validation layer for model outputs

### Long-term (Phase 3)
10. ⏳ Implement caching for expensive computations
11. ⏳ Add incremental update support
12. ⏳ Create web dashboard using context outputs
13. ⏳ Integrate AI layers (C1-C8) from architecture doc

---

## Migration Path

### For Existing Code

**Old approach** (conf_step_pipeline.py, src/khujta.py):
- Still works for backwards compatibility
- Gradually migrate to new architecture
- Start with new models, migrate old ones over time

**New approach** (recommended for all new code):
- Use GabedaContext + ModelExecutor for everything
- Clean separation of concerns
- Better debugging and introspection
- Scales to full 6-model pipeline

---

## Design Decisions

### Why Context Over Pipeline?

1. **Multiple Outputs**: Pipeline assumes single output per step
2. **State Visibility**: Context makes all state explicit and accessible
3. **Config Separation**: User vs runtime configs don't mix
4. **Debugging**: Easy to inspect at any point
5. **Flexibility**: Non-linear flows supported naturally

### Why Not Classes/OOP per Model?

- Option 3 (Model Registry) considered but more boilerplate
- Current approach: functional with state management
- Balance between OOP and functional paradigms
- Can evolve to class-based if needed later

### Why Executor Pattern?

- Clean separation: config → execution → results
- Handles integration with existing functions (get_dependencies, calc_datasets)
- Easy to test and mock
- Supports both individual and batch execution

---

## Performance Considerations

- Context stores DataFrames in memory
- For large datasets (>1M rows), consider:
  - Saving intermediate results to disk
  - Using parquet format (compressed)
  - Clearing datasets no longer needed
- Parallel execution possible for models 2-5 (they only depend on model 1)

---

## Documentation

- **Architecture Guide**: [docs/context_architecture_guide.md](docs/context_architecture_guide.md)
- **Complete 6-Model Spec**: [docs/specs/99_architecture.md](docs/specs/99_architecture.md)
- **Working Examples**: [play.ipynb](play.ipynb)
- **Original Project README**: [CLAUDE.md](CLAUDE.md)

---

## Contact & Support

For questions about the architecture:
- Review the complete guide in [docs/context_architecture_guide.md](docs/context_architecture_guide.md)
- Check working examples in [play.ipynb](play.ipynb)
- See execution logs in `logs/` directory

---

## Summary

✅ **Problem Solved**: Can now handle multiple outputs, dynamic configs, and explicit state management

✅ **Architecture**: Context-based approach with ModelExecutor pattern

✅ **Tested**: Working example with product_stats model in play.ipynb

✅ **Scalable**: Ready for all 6 models in the GabeDA pipeline

✅ **Documented**: Comprehensive guide and working examples

**Next**: Migrate remaining models (customer, time, basket, business) to the new architecture.
