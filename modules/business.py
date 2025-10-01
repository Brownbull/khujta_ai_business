"""
Business Core Module
Central class to manage business data, configuration, and calculated metrics
"""

import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict
import os
import warnings
warnings.filterwarnings('ignore')


class Business:
    """
    Central business class that holds all data, configuration, and calculated metrics.
    This class is responsible for data storage and state management, not calculations.
    """

    def __init__(self, data_source: str = None, config: Dict = None):
        """Initialize business with data and configuration"""
        # Configuration
        self.config = config or self._default_config()

        # Raw data
        self.data = None

        # Calculated metrics (populated by BusinessAnalyzer)
        self.product_analysis = None
        self.revenue_metrics = None
        self.inventory = None
        self.kpis = None
        self.alerts = None
        self.pareto = None

        # Run timestamp for unique file names
        now = datetime.now()
        self.min_dt = None
        self.max_dt = None
        self.run_dt = now.strftime('%Y%m%d')  # YYYYMMDD
        self.run_time = now.strftime('%H%M')  # HHMM

        # Output directory
        self.out_dir = self._set_out_dir()

        # Load data if provided
        if data_source:
            self.load_data(data_source)
            print(f"Business initialized with data from: {data_source} {self.data.shape if self.data is not None else ''}")

        print(f"Output directory: {self.out_dir}")

    def _default_config(self) -> Dict:
        """Default configuration settings"""
        return {
            'project_name': 'Buenacarne',
            'analysis_date': datetime.now(),
            'top_products_threshold': 0.2,
            'dead_stock_days': 30,
            'currency_format': 'CLP',
            'language': 'EN',
            'date_col': 'fecha',
            'product_col': 'producto',
            'description_col': 'glosa',
            'revenue_col': 'total',
            'quantity_col': 'cantidad',
            'transaction_col': 'trans_id',
            'cost_col': 'costo',
            'out_dir': 'outputs'
        }

    def _set_out_dir(self) -> str:
        """Set output directory based on config and timestamp"""
        output_dir = os.path.join(
            self.config['out_dir'],
            self.config['project_name'],
            f"{self.run_dt}_{self.run_time}"
        )
        return output_dir

    def load_data(self, data_source: str):
        """Load data from file or DataFrame"""
        if isinstance(data_source, pd.DataFrame):
            self.data = data_source
        elif data_source.endswith('.csv'):
            self.data = pd.read_csv(data_source)
        elif data_source.endswith(('.xlsx', '.xls')):
            self.data = pd.read_excel(data_source)
        else:
            raise ValueError(f"Unsupported data source type: {data_source}")

        self._prepare_data()

    def _prepare_data(self):
        """Prepare and clean data for analysis"""
        if self.data is None:
            return

        # Convert date column
        if self.config['date_col'] in self.data.columns:
            self.data[self.config['date_col']] = pd.to_datetime(
                self.data[self.config['date_col']],
                errors='coerce'
            )
        
        # Get range of dates
        self.min_dt = self.data[self.config['date_col']].min()
        self.max_dt = self.data[self.config['date_col']].max()
        print(f"Data date range: {self.min_dt.date()} to {self.max_dt.date()}")
        
        analysis_date = pd.Timestamp(self.config['analysis_date'])
        if analysis_date < self.min_dt:
            print(f"⚠️⚠️⚠️ Warning: Analysis date {analysis_date.date()} is before data range. ⚠️⚠️⚠️")
        if analysis_date > self.max_dt + pd.Timedelta(days=30):
            print(f"⚠️⚠️⚠️ Warning: Analysis date {analysis_date.date()} is significantly after data range. ⚠️⚠️⚠️")
        
        # Add time-based columns if they don't exist
        if 'hour' not in self.data.columns and 'inith' in self.data.columns:
            self.data['hour'] = self.data['inith']

        if 'weekday' not in self.data.columns and self.config['date_col'] in self.data.columns:
            self.data['weekday'] = self.data[self.config['date_col']].dt.day_name()
            self.data['weekday_num'] = self.data[self.config['date_col']].dt.dayofweek

    def format_currency(self, value: float) -> str:
        """Format value as currency based on config"""
        if self.config['currency_format'] == 'CLP':
            return f"$ {value:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
        else:
            return f"${value:,.2f}"

    def get_date_range(self) -> Dict:
        """Get date range from data"""
        if self.data is None or self.config['date_col'] not in self.data.columns:
            return {'start': None, 'end': None}

        return {
            'start': self.data[self.config['date_col']].min(),
            'end': self.data[self.config['date_col']].max()
        }

    def __repr__(self):
        """String representation of Business instance"""
        data_info = f"{len(self.data)} rows" if self.data is not None else "No data"
        return f"Business(project='{self.config['project_name']}', data={data_info})"
