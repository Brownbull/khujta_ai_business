# ModelDriver Enhancement Plan

## Current State Analysis

### What We Have (model_driver/)
✓ **FeatureRegistry**: Simple feature registration with metadata
✓ **DependencyResolver**: Backward dependency resolution from outputs to inputs
✓ **ModelDriver**: Pipeline orchestrator with staged execution
✓ **Dynamic Input Resolution**: Automatically determines required inputs based on selected outputs

### What's Missing vs. model_class.md Requirements

Based on analysis of the reference notebooks (prpf1_pp, prpf1_cp, etc.) and model_class.py:

#### 1. **Function Signature Pattern** ⚠️ CRITICAL MISMATCH
   - **Reference Pattern**: Functions receive **named arguments** matching column names
     ```python
     def prpf1_pp2001(year_built, building_area):
         return np.where(year_built > 1950, 1, 0)
     ```
   - **Current ModelDriver**: Functions receive entire DataFrame
     ```python
     def calc_feature(df):
         df['feature'] = ...
         return df
     ```
   - **Issue**: Our signature is **incompatible** with the reference approach
   - **Why Reference Pattern is Better**:
     - Self-documenting (function signature shows exactly what inputs it needs)
     - Easier to test (just call function with values)
     - No need to specify `inputs=` separately (extracted from function signature)
     - More portable (can be used outside DataFrame context)

#### 2. **Filter vs Attribute Execution in Same Loop** ⚠️ IMPORTANT
   - **Reference Pattern**: Both filters and attributes execute in the **same groupby.apply()** loop
   - **Current ModelDriver**: Separate stages (filters first, then attributes)
   - **Issue**: Some filters may depend on attribute values from aggregation
   - **Requirement from model_class.md line 26**:
     > "some filter calculation could depend on an attribute value, so the calling of these following the execution order should be in the same loop in which 2 dataframes are being updates, one on input level where filters can be added, and the second on aggregation by groupby key where attribute columns are being added."

#### 3. **Registry Storage Pattern** 📝 MISSING
   - **Requirement**: Features should be stored in **plain code** files (like model_attributes.py)
   - **Current**: Features only registered programmatically
   - **Need**: Ability to save/load feature registry from Python files

#### 4. **Model Chaining** 📝 MISSING
   - **Requirement (line 8)**: "model seq in case other model will use the output as input"
   - **Reference (model_class.py:486)**: `attr_set_arr[1].calc_attributes(attr_set_arr[0].calc_attributes(payload))`
   - **Need**: Support for multi-model pipelines where one model's output feeds another

#### 5. **Group-by Support** ⚠️ PARTIAL
   - **Reference Pattern**: Explicit group_by key (typically 'pin' or similar)
   - **Current**: group_by support exists but not fully tested
   - **Need**: Better integration with row-level vs group-level calculations

#### 6. **Automatic Dependency Extraction** ⚠️ MISSING
   - **Reference Pattern**: Dependencies inferred from function signatures
   - **Current**: Must explicitly specify `inputs=['col1', 'col2']`
   - **Need**: Auto-extract from function signature inspection

---

## Enhancement Plan

### Phase 1: Signature Pattern Refactor 🔴 CRITICAL

**Goal**: Change from DataFrame-based to argument-based function signatures

**Before**:
```python
def profit_margin(df):
    df['profit_margin'] = (df['revenue'] - df['cost']) / df['revenue']
    return df

driver.register_filter('profit_margin', profit_margin,
                      inputs=['revenue', 'cost'],  # ← Manual
                      outputs=['profit_margin'])
```

**After**:
```python
def profit_margin(revenue, cost):
    return (revenue - cost) / revenue * 100

driver.register_filter('profit_margin', profit_margin)
# ← inputs auto-extracted from signature!
# ← outputs defaults to ['profit_margin']
```

**Implementation**:
1. Update `FeatureMetadata` to support vectorized functions (receive arrays, return array/value)
2. Add signature inspection to auto-extract inputs from function `__code__.co_varnames`
3. Update execution engine to call features with `np.vectorize(f)(*[df[col].values for col in inputs])`
4. Add output name defaulting (if not specified, use function name)

**Files to Modify**:
- `model_driver/feature_simple.py`: Add signature inspection in `register_filter()`/`register_attribute()`
- `model_driver/driver.py`: Update `_stage_filters()` and `_stage_attributes()` to use vectorized calls

---

### Phase 2: Unified Execution Loop 🟡 IMPORTANT

**Goal**: Execute filters and attributes in same loop (two-DataFrame pattern)

**Current Pattern**:
```
dfI (input) → [Filters] → dfF (filtered) → [GroupBy] → [Attributes] → dfC (output)
```

**Target Pattern** (from reference):
```
dfI (input) → [GroupBy.apply()] → {
    dfI_group ← row-level (filters)
    dfC_group ← aggregation-level (attributes)
    execute in dependency order using BOTH dataframes
}
```

**Why**: Some features might need:
- Filter that uses an attribute: `def filter_x(col_a, aggregated_avg):`
- Multiple passes through data with intermediate aggregations

**Implementation**:
1. Create `_execute_feature_in_context()` method that:
   - Checks if feature is filter (output = row-level) or attribute (output = aggregation)
   - If filter: executes and adds to dfI_group
   - If attribute: executes and adds to dfC_group
2. Update groupby execution to use single loop with dual DataFrame updates
3. Maintain dependency ordering but allow mixing of filters/attributes

**Files to Modify**:
- `model_driver/driver.py`: Refactor `execute()` to use single-loop pattern
- `model_driver/resolver.py`: Update to handle filter→attribute and attribute→filter dependencies

---

### Phase 3: Registry Persistence 🟢 ENHANCEMENT

**Goal**: Save/load features from Python files (like model_attributes.py)

**Target**:
```python
# features/my_features.py
def profit_margin(revenue, cost):
    return (revenue - cost) / revenue * 100

def total_revenue(revenue):  #agg
    return revenue.sum()

# In notebook:
driver.load_features_from_module('features.my_features')
# OR
driver.save_features_to_module('features.my_generated_features')
```

**Implementation**:
1. Add `save_to_python_file(path)` method that generates Python code with all registered features
2. Add `load_from_python_file(path)` or `load_from_module(module)` that:
   - Imports the module
   - Inspects functions
   - Auto-registers based on naming convention or decorators
3. Use `inspect.getsource()` to preserve original function code

**Files to Create**:
- `model_driver/registry_io.py`: Module for save/load operations

---

### Phase 4: Model Chaining 🟢 ENHANCEMENT

**Goal**: Support multi-model pipelines

**Target**:
```python
model_pp = ModelDriver(config_pp)
model_cp = ModelDriver(config_cp)

# Chain models
result = model_cp.execute(model_pp.execute(df)['output'])

# OR automatic chaining
pipeline = ModelPipeline([model_pp, model_cp])
result = pipeline.execute(df)
```

**Implementation**:
1. Add `seq` field to config (sequence number for chaining)
2. Create `ModelPipeline` class that:
   - Accepts list of ModelDriver instances
   - Executes in sequence
   - Passes output of one as input to next
3. Add validation to ensure output columns match next model's required inputs

**Files to Create**:
- `model_driver/pipeline.py`: ModelPipeline class

---

### Phase 5: Enhanced Group-by Integration 🟡 IMPORTANT

**Goal**: Better support for group-by operations

**Current Issues**:
- Row-level vs aggregation-level not clearly separated
- group_by configuration not fully integrated

**Target**:
```python
driver = ModelDriver({
    'client_name': 'auto_partes',
    'model_name': 'sales_v1',
    'group_by': 'pin',  # ← Key for aggregations
})

# Filters operate on dfI (row-level)
def age(year_built):  # Executed per row
    return 2025 - year_built

# Attributes operate on groups
def avg_age(age):  #agg  # Executed per pin
    return age.mean()
```

**Implementation**:
1. Add explicit `is_aggregation` detection:
   - Check for keywords in source: `.sum`, `.mean`, `.max`, etc.
   - Check function name patterns: `agg_*`, `total_*`, `avg_*`, `count_*`
   - Allow manual override: `register_attribute(..., is_aggregation=True)`
2. Use detection to route execution correctly
3. Add `#agg` comment convention (like reference code)

**Files to Modify**:
- `model_driver/feature_simple.py`: Add `is_aggregation` detection (port from model_class.py:38-46)
- `model_driver/driver.py`: Use detection in execution logic

---

### Phase 6: Auto-Dependency Extraction 🟢 ENHANCEMENT

**Goal**: Remove need for manual `inputs=` specification

**Before**:
```python
driver.register_filter('profit_margin', profit_margin,
                      inputs=['revenue', 'cost'],  # ← Manual!
                      outputs=['profit_margin'])
```

**After**:
```python
driver.register_filter('profit_margin', profit_margin)
# Auto-extracts:
#   inputs = ['revenue', 'cost'] from signature
#   outputs = ['profit_margin'] from function name
```

**Implementation**:
1. Use `inspect.signature()` or `func.__code__.co_varnames[:func.__code__.co_argcount]`
2. Make `inputs` and `outputs` parameters optional
3. If not provided, extract from signature
4. Output defaults to `[function_name]`

**Files to Modify**:
- `model_driver/feature_simple.py`: Add auto-extraction in registration methods

---

## Implementation Priority

### CRITICAL (Must Have)
1. **Phase 1**: Signature Pattern Refactor
   - **Why**: Foundation for everything else, reference compatibility
   - **Impact**: Changes execution engine fundamentally
   - **Effort**: Medium (2-3 hours)

2. **Phase 2**: Unified Execution Loop
   - **Why**: Required for filter↔attribute dependencies
   - **Impact**: Core execution model
   - **Effort**: High (4-5 hours)

### IMPORTANT (Should Have)
3. **Phase 5**: Enhanced Group-by Integration
   - **Why**: Core to reference implementation pattern
   - **Impact**: Makes aggregations work correctly
   - **Effort**: Low-Medium (1-2 hours)

4. **Phase 6**: Auto-Dependency Extraction
   - **Why**: Reduces boilerplate, less error-prone
   - **Impact**: Better DX (developer experience)
   - **Effort**: Low (1 hour)

### ENHANCEMENT (Nice to Have)
5. **Phase 3**: Registry Persistence
   - **Why**: Enables feature reuse across projects
   - **Impact**: Workflow improvement
   - **Effort**: Medium (2-3 hours)

6. **Phase 4**: Model Chaining
   - **Why**: Advanced use case
   - **Impact**: Enables complex pipelines
   - **Effort**: Medium (2-3 hours)

---

## Breaking Changes

⚠️ **Phase 1 will break existing code**

All feature functions must be rewritten from:
```python
def my_filter(df):
    df['output'] = df['col1'] + df['col2']
    return df
```

To:
```python
def my_filter(col1, col2):
    return col1 + col2
```

**Migration Path**:
1. Keep current implementation in `model_driver_v1/`
2. Create new implementation in `model_driver/` (refactored)
3. Provide migration guide
4. Support both patterns temporarily with `legacy_mode=True`

---

## Questions for User

1. **Signature Pattern**: Confirm we should switch to `def feature(col1, col2):` pattern?
2. **Breaking Changes**: OK to break current examples for better reference compatibility?
3. **Group-by**: Should group_by key always be included in output, or only when specified?
4. **Output Naming**: OK to default output name to function name (can override)?
5. **Aggregation Detection**: Trust automatic detection via keywords, or require explicit flag?
6. **Implementation Order**: Start with Phase 1 (signatures) then Phase 2 (unified loop)?

---

## Success Criteria

✅ Feature functions match reference notebook signature style
✅ No manual `inputs=` specification needed
✅ Filters and attributes can depend on each other
✅ Group-by aggregations work correctly
✅ Can save/load feature registry from Python files
✅ Supports multi-model chaining
✅ All current demo examples work (after migration)
✅ Compatible with reference implementation patterns

---

## Timeline Estimate

- **Phase 1**: 3 hours
- **Phase 2**: 5 hours
- **Phase 5**: 2 hours
- **Phase 6**: 1 hour
- **Testing & Migration**: 3 hours
- **Documentation**: 2 hours

**Total**: ~16 hours (2 days)

For Phases 3-4: Additional ~5 hours (optional enhancements)
