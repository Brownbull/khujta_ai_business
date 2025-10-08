from typing import Callable, List, Dict
import pandas as pd
from datetime import datetime

class Pipeline:
    def __init__(self, config: Dict[str, any]):
        self.config = config
        self.steps: List[Callable] = []
        
        # Initialize runtime variables and add to config
        self.now = datetime.now()
        self.config['run_dt'] = self.now.strftime('%Y%m%d')  # YYYYMMDD
        self.config['run_time'] = self.now.strftime('%H%M')   # HHMM
        self.config['run_id'] = f"{self.config['run_dt']}_{self.config['run_time']}"
        
        # Initialize shared variables in config
        self.config['step_metrics'] = {}  # Store metrics from each step
        self.config['intermediate_results'] = {}  # Store data between steps
        self.config['flags'] = {}  # Store flags and decisions
    
    def add_step(self, step_name: str, processor: Callable):
        self.steps.append((step_name, processor))
        return self
    
    def run(self, initial_data: pd.DataFrame = None) -> pd.DataFrame:
        data = initial_data if initial_data is not None else self._load_initial_data()
        
        print(f"Starting pipeline run: {self.config['run_id']}")
        print(f"Initial config keys: {list(self.config.keys())}")
        
        for step_name, processor in self.steps:
            print(f"Executing: {step_name}")
            print(f"Config before {step_name}: {self.config.get('step_metrics', {})}")
            
            data = processor(data, self.config)
            
            print(f"Config after {step_name}: {self.config.get('step_metrics', {})}")
        
        return data
    
    def _load_initial_data(self) -> pd.DataFrame:
        return pd.read_csv(self.config['input_file'])

# Processing functions that read and write to config
def preprocess_data(data: pd.DataFrame, config: Dict) -> pd.DataFrame:
    """Preprocessing step that calculates stats and stores in config"""
    
    # Read from config
    run_id = config['run_id']
    print(f"Preprocessing for run: {run_id}")
    
    # Preprocessing logic
    data = data.dropna().reset_index(drop=True)
    
    # Calculate and store metrics in config for later steps
    config['step_metrics']['preprocessing'] = {
        'original_rows': len(data) + data.isna().sum().sum(),  # Estimate original
        'final_rows': len(data),
        'columns_processed': len(data.columns),
        'completion_time': datetime.now().strftime('%H:%M:%S')
    }
    
    # Store intermediate data in config
    config['intermediate_results']['preprocessed_columns'] = list(data.columns)
    config['intermediate_results']['data_shape_before_filters'] = data.shape
    
    # Add a flag based on data characteristics
    config['flags']['has_missing_data'] = data.isna().sum().sum() > 0
    
    return data

def calculate_filters(data: pd.DataFrame, config: Dict) -> pd.DataFrame:
    """Filter calculation that uses previous step's results"""
    
    # Read metrics from previous step
    preprocess_metrics = config['step_metrics'].get('preprocessing', {})
    original_rows = preprocess_metrics.get('original_rows', 0)
    final_rows = preprocess_metrics.get('final_rows', len(data))
    
    print(f"Data reduced from {original_rows} to {final_rows} rows in preprocessing")
    
    # Use flags from previous step
    if config['flags'].get('has_missing_data', False):
        print("Warning: Data had missing values that were dropped")
    
    # Filter calculation logic
    threshold = config.get('filter_threshold', 100)
    data['value_filter'] = data['value'] > threshold
    
    # Calculate filter statistics
    filter_stats = {
        'threshold_used': threshold,
        'rows_above_threshold': data['value_filter'].sum(),
        'percentage_above_threshold': (data['value_filter'].mean() * 100),
        'filter_applied_at': datetime.now().strftime('%H:%M:%S')
    }
    
    # Store filter results in config
    config['step_metrics']['filter_calculation'] = filter_stats
    config['intermediate_results']['filter_threshold'] = threshold
    config['intermediate_results']['filtered_data_shape'] = data.shape
    
    # Set flag for next step
    config['flags']['high_filter_rate'] = filter_stats['percentage_above_threshold'] > 50
    
    return data

def aggregate_data(data: pd.DataFrame, config: Dict) -> pd.DataFrame:
    """Aggregation that uses information from all previous steps"""
    
    # Access information from ALL previous steps
    preprocess_metrics = config['step_metrics'].get('preprocessing', {})
    filter_metrics = config['step_metrics'].get('filter_calculation', {})
    
    print(f"Aggregating data that was preprocessed at {preprocess_metrics.get('completion_time')}")
    print(f"Using filter threshold: {filter_metrics.get('threshold_used', 'unknown')}")
    
    # Use flags to decide aggregation strategy
    if config['flags'].get('high_filter_rate', False):
        print("High filter rate detected - using conservative aggregation")
        aggregation_method = 'mean'
    else:
        aggregation_method = 'sum'
    
    # Aggregation logic
    if 'category' in data.columns:
        aggregated = data.groupby('category').agg({
            'value': [aggregation_method, 'count']
        })
    else:
        aggregated = data.agg({
            'value': [aggregation_method, 'count']
        })
    
    # Store aggregation results in config
    config['step_metrics']['aggregation'] = {
        'method_used': aggregation_method,
        'final_row_count': len(aggregated),
        'completion_time': datetime.now().strftime('%H:%M:%S'),
        'decision_based_on_filter_rate': config['flags'].get('high_filter_rate', False)
    }
    
    # Add pipeline summary to config
    config['pipeline_summary'] = {
        'total_steps': len([k for k in config['step_metrics'].keys()]),
        'final_data_shape': aggregated.shape,
        'run_id': config['run_id'],
        'run_completion_time': datetime.now().strftime('%Y%m%d %H:%M:%S')
    }
    
    return aggregated

# Usage
config = {
    'input_file': 'data.csv',
    'filter_threshold': 100
}

pipeline = (Pipeline(config)
    .add_step("preprocessing", preprocess_data)
    .add_step("filter_calculation", calculate_filters)
    .add_step("aggregation", aggregate_data))

result = pipeline.run()

# Access the final config with all accumulated data
print("\n=== FINAL CONFIG SUMMARY ===")
print(f"Run ID: {pipeline.config['run_id']}")
print(f"Steps executed: {list(pipeline.config['step_metrics'].keys())}")
print(f"Pipeline summary: {pipeline.config.get('pipeline_summary', {})}")
print(f"All step metrics: {pipeline.config['step_metrics']}")