from typing import Callable, Dict, List, Any
import pandas as pd
from datetime import datetime
from typing import Dict
import os
import warnings
warnings.filterwarnings('ignore')

from src.logger import get_logger

# Initialize logger for this module
logger = get_logger(__name__)

class Khujta:
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize Khujta with optional data source and configuration"""
        self.config = config or self._default_config()
        self.steps: List[Callable] = []
        
        # Add runtime variables
        self.now = datetime.now()
        self.config['run_dt'] = self.now.strftime('%Y%m%d')  # YYYYMMDD
        self.config['run_time'] = self.now.strftime('%H%M')   # HHMM
        self.config['run_id'] = f"{self.config['run_dt']}_{self.config['run_time']}"  # YYYYMMDD_HHMM
        
    def add_step(self, step_name: str, processor: Callable):
        self.steps.append((step_name, processor))
        return self
    
    def run(self, initial_data: pd.DataFrame = None) -> pd.DataFrame:
        data = initial_data if initial_data is not None else self._load_initial_data()
        
        logger.info(f"Starting pipeline run: {self.config['run_id']}")
        logger.info(f"Initial config keys: {list(self.config.keys())}")
        
        for step_name, processor in self.steps:
            logger.info(f"Executing: {step_name}")
            data = processor(data, self.config)
            logger.info(f"Config after {step_name}: {self.config.get('step_metrics', {})}")
        
        return data
    
    def _load_initial_data(self) -> pd.DataFrame:
        self.load_data(self.config['input_file'])
        logger.info(f"Business initialized with data from: {self.config['input_file']} {self.data.shape if self.data is not None else ''}")
        return self.data
        
    def _default_config(self) -> Dict:
        """Default configuration settings"""
        return {
            # Project settings
            'client': 'test_client',
            'out_dir': 'data',
            
            # Column Mappings
            'column_mappings': {
                'in_dt': 'fecha',
                'in_trans_id': 'trans_id',
                'in_product': 'producto',
                'in_description': 'glosa',
                'in_cost': 'costo',
                'in_price': 'precio',
                'in_quantity': 'cantidad',
                'in_total': 'total',
                'in_customer_id': 'customer_id',
                'in_customer_name': 'customer_name',
                'in_customer_location': 'customer_location',
            },

            # Analysis settings
            'analysis_dt': self.now.strftime('%Y-%m-%d'),
            'language': 'EN',
            
            # Logging and performance
            'log_level': 'DEBUG',               # 'DEBUG', 'INFO', 'WARNING','ERROR', 'CRITICAL'
        }
            
    def load_data(self, data_source: str):
        self.file_name = os.path.basename(data_source).split('.')[0]
        logger.info(f"Loading data from: {data_source}")
        """Load data from file or DataFrame"""
        if isinstance(data_source, pd.DataFrame):
            self.data = data_source
        elif data_source.endswith('.csv'):
            self.data = pd.read_csv(data_source)
        elif data_source.endswith(('.xlsx', '.xls')):
            self.data = pd.read_excel(data_source)
        else:
            raise ValueError(f"Unsupported data source type: {data_source}")

        logger.info(f"Data loaded with shape: {self.data.shape if self.data is not None else ''}")
        
    def __repr__(self):
        """String representation of Khujta instance"""
        data_info = f"{len(self.data)} rows" if self.data is not None else "No data"
        return f"Khujta(client='{self.config['client']}', model='{self.config['model']}', data={data_info})"
