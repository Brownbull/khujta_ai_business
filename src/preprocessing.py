import pandas as pd
import os
from typing import Dict
from src.logger import get_logger

logger = get_logger(__name__)

def dtype_cols(data: pd.DataFrame, config: Dict) -> pd.DataFrame:
    for col, dtype in config['column_types'].items():
        if col in data.columns:
            if dtype == 'date':
                data[col] = pd.to_datetime(data[col], errors='coerce')
            elif dtype == 'int':
                data[col] = pd.to_numeric(data[col], errors='coerce', downcast='integer')
            elif dtype == 'float':
                data[col] = pd.to_numeric(data[col], errors='coerce', downcast='float')
            elif dtype == 'str':
                data[col] = data[col].astype(str)
            logger.info(f"Converted column '{col}' to type '{dtype}'")
        else:
            logger.warning(f"Column '{col}' not found in data for type conversion")
    return data


def map_cols(data: pd.DataFrame, config: Dict) -> pd.DataFrame:
    missing_cols = []
    
    for key, value in config['column_mappings'].items():
        if value in data.columns:
            data = data.rename(columns={value: key})
            logger.info(f"Mapped column '{value}' to '{key}'")
        else:
            missing_cols.append(value)
            logger.debug(f"Column '{value}' not found in data")
            
    return data, missing_cols

def check_dt_range(min_dt, max_dt, analysis_dt):
    logger.info(f"Data date range: {min_dt.date()} to {max_dt.date()}")
    logger.info(f"Recommended analysis_dt: {max_dt.date() + pd.Timedelta(days=1)} or later")
    
    if analysis_dt < min_dt:
        logger.warning(f"⚠️⚠️⚠️ Warning: Analysis date {analysis_dt.date()} is before data range. ⚠️⚠️⚠️")
    if analysis_dt > max_dt + pd.Timedelta(days=30):
        logger.warning(f"⚠️⚠️⚠️ Warning: Analysis date {analysis_dt.date()} is significantly after data range. ⚠️⚠️⚠️")
        
def load_data(data_source: str):
    logger.info(f"Loading data from: {data_source}")
    """Load data from file or DataFrame"""
    if isinstance(data_source, pd.DataFrame):
        data = data_source
    elif data_source.endswith('.csv'):
        data = pd.read_csv(data_source)
    elif data_source.endswith(('.xlsx', '.xls')):
        data = pd.read_excel(data_source)
    else:
        raise ValueError(f"Unsupported data source type: {data_source}")

    logger.info(f"Data loaded with shape: {data.shape if data is not None else ''}")

    return data

def preprocess_data(data: pd.DataFrame, config: Dict) -> pd.DataFrame:
    data, missing_cols = map_cols(data, config)
    if 'in_dt' in missing_cols:
        logger.error(f"Missing columns in data: {missing_cols}")
        raise ValueError(f"Missing columns in data: {missing_cols}")
    
    # Date conversion
    data['in_dt'] = pd.to_datetime( data['in_dt'], errors='coerce')
        
    # Get range of dates
    config['min_dt'] = data['in_dt'].min()
    config['max_dt'] = data['in_dt'].max()
    
    # Check analysis date
    analysis_dt = pd.Timestamp(config['analysis_dt'])
    
    # Validate analysis date against data range
    check_dt_range(config['min_dt'], config['max_dt'], analysis_dt)
    
    # Convert column types
    data = dtype_cols(data, config)
    
    # Drop rows with NaT in date column
    return data.dropna(subset=['in_dt']).reset_index(drop=True)


