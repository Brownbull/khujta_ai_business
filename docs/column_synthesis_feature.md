# Automatic Column Synthesis Feature

## Overview

The system now automatically calculates missing input columns when they can be derived from existing columns using available filter functions. This eliminates the need to manually preprocess data when columns are missing but calculable.

## How It Works

### 1. Detection Phase
When `calc_datasets()` is called, the new `synthesize_missing_columns()` function:
- Checks which columns from `in_cols` are missing in the input DataFrame
- Searches for filter functions that match the missing column names
- Verifies that the filter function is row-level (not an aggregation)

### 2. Synthesis Phase
For each missing column:
- Extracts the function signature to determine required arguments
- Checks if all required arguments are available in the DataFrame
- If yes: calculates the missing column using `np.vectorize()`
- If no: logs a warning about missing dependencies

### 3. Execution Phase
The synthesized columns are added to the DataFrame **before** the main `exec_seq` execution, ensuring they're available when needed by other features.

## Example Use Case

### Dataset Missing `in_unit_price`
```
CSV columns: trans_id, fecha, producto, glosa, costo, total, cantidad, ...
Missing: precio (mapped to in_unit_price)
```

### Filter Function Available
```python
def in_unit_price(in_quantity, in_total_price):
    return in_total_price / in_quantity if in_quantity != 0 else 0.0
```

### Result
The system automatically:
1. Detects `in_unit_price` is missing but required
2. Finds the `in_unit_price()` filter function
3. Verifies `in_quantity` and `in_total_price` exist
4. Calculates: `in_unit_price = total / cantidad`
5. Adds the column to the DataFrame

## Implementation Details

### Location
- **File**: [src/model_ops.py](../src/model_ops.py)
- **Function**: `synthesize_missing_columns(data_in, cfg_model)`
- **Called by**: `calc_datasets()` (lines 117-121)

### Key Logic
```python
def calc_datasets(data_in: pd.DataFrame, cfg_model: Dict):
    # 1. Check if in_cols exists and has missing columns (optimization)
    if 'in_cols' in cfg_model:
        missing_cols = [col for col in cfg_model['in_cols'] if col not in data_in.columns]
        if missing_cols:
            # 2. Only call synthesis when needed
            data_in = synthesize_missing_columns(data_in, cfg_model)

def synthesize_missing_columns(data_in: pd.DataFrame, cfg_model: Dict) -> pd.DataFrame:
    # Assumes caller has verified in_cols exists and has missing columns
    missing_cols = [col for col in cfg_model['in_cols'] if col not in data_in.columns]

    # For each missing column, check if it's in features
    for missing_col in missing_cols:
        if missing_col in cfg_model['features']:
            # Extract function and arguments
            # Check if it's a row-level filter (not groupby)
            # Verify all args are available
            # Calculate and add to DataFrame
```

### Requirements
For a column to be synthesizable:
1. ✅ Must be listed in `cfg_model['in_cols']`
2. ✅ Must have a matching function in `cfg_model['features']`
3. ✅ Function must be a row-level filter (not contain aggregation keywords)
4. ✅ All function arguments must exist in the DataFrame

## Supported Scenarios

### ✅ Supported
- **Simple calculations**: `in_unit_price = total / quantity`
- **Derived metrics**: `margin = price - cost`
- **Chained synthesis**: Column A → Column B → Column C (if executed in order)
- **Multiple columns**: Synthesize several columns in one pass

### ❌ Not Supported (by design)
- **Aggregated columns**: Functions containing `.sum()`, `.mean()`, etc.
- **Columns not in in_cols**: Only synthesizes explicitly required inputs
- **Complex dependencies**: Circular or unresolvable dependency chains

## Testing

Run the test script to see the feature in action:
```bash
python test_column_synthesis.py
```

### Expected Output
```
[!] Notice: 'precio' (in_unit_price) is NOT in the dataset
...
@synthesize_missing_columns - Detected missing input columns: ['in_unit_price']
  ✓ Synthesizing in_unit_price from ['in_quantity', 'in_total_price']
@synthesize_missing_columns - Successfully synthesized 1 columns: ['in_unit_price']
...
[OK] in_unit_price: exists (mean=8008.78)
[OK] margin: exists (mean=2233.78)
```

## Configuration Requirements

### Column Mappings
Define expected columns in `column_mappings`:
```python
'column_mappings': {
    'in_unit_price': 'precio',  # Maps to 'precio' in CSV
    'in_quantity': 'cantidad',
    'in_total_price': 'total',
}
```

### Feature Functions
Provide filter functions that can calculate missing columns:
```python
'features': {
    'in_unit_price': in_unit_price,  # Function to calculate if missing
    'margin': margin,
    # ... other features
}
```

### Dependency Resolution
Ensure `get_dependencies()` includes synthesizable columns in `in_cols`:
```python
# After get_dependencies() runs:
cfg_model['in_cols'] = ['in_quantity', 'in_total_price', 'in_unit_price', ...]
```

## Benefits

1. **Data Flexibility**: Accept datasets with varying column structures
2. **Reduced Preprocessing**: No need to manually add calculated columns
3. **Reusable Logic**: Filter functions serve dual purpose (synthesis + feature engineering)
4. **Automatic Dependencies**: System handles calculation order automatically
5. **Fail-Safe**: Logs warnings but doesn't crash if synthesis fails

## Logging

The system provides detailed logs:
```
INFO - @synthesize_missing_columns - Detected 1 missing input columns: ['in_unit_price']
INFO - ✓ Synthesizing in_unit_price from ['in_quantity', 'in_total_price']
INFO - @synthesize_missing_columns - Successfully synthesized 1 columns: ['in_unit_price']
```

Or when synthesis isn't possible:
```
WARNING - ✗ Cannot synthesize in_unit_price: missing args ['in_quantity']
```

## Future Enhancements

Potential improvements:
- **Multi-pass synthesis**: Iterate until no more columns can be synthesized
- **Dependency ordering**: Automatically order synthesis to handle chains
- **Cost-aware synthesis**: Skip expensive calculations unless needed
- **User override**: Allow explicit opt-out of synthesis for specific columns
- **Synthesis cache**: Store synthesized columns for reuse across models
