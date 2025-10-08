from typing import Callable, Dict, List, Any
import pandas as pd
from functools import reduce

class Pipeline:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.steps: List[Callable] = []
    
    def add_step(self, step_name: str, processor: Callable):
        self.steps.append((step_name, processor))
        return self
    
    def run(self, initial_data: pd.DataFrame = None) -> pd.DataFrame:
        data = initial_data if initial_data is not None else self._load_initial_data()
        
        for step_name, processor in self.steps:
            print(f"Executing: {step_name}")
            data = processor(data, self.config)
        
        return data
    
    def _load_initial_data(self) -> pd.DataFrame:
        return pd.read_csv(self.config['input_file'])

# Define processing functions
def preprocess_data(data: pd.DataFrame, config: Dict) -> pd.DataFrame:
    return data.dropna().reset_index(drop=True)

def calculate_filters(data: pd.DataFrame, config: Dict) -> pd.DataFrame:
    data['custom_filter'] = data['value'] > config.get('filter_threshold', 100)
    return data

def aggregate_data(data: pd.DataFrame, config: Dict) -> pd.DataFrame:
    return data.groupby('category').agg({
        'value': ['mean', 'sum', 'count']
    })

# Usage
config = {'input_file': 'data.csv', 'filter_threshold': 100}

pipeline = (Pipeline(config)
    .add_step("preprocessing", preprocess_data)
    .add_step("filter_calculation", calculate_filters)
    .add_step("aggregation", aggregate_data))

result = pipeline.run()