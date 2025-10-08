import pandas as pd
import numpy as np
from typing import Dict, Tuple
from src.logger import get_logger

logger = get_logger(__name__)

def is_groupby(f):
    if callable(f):
        from inspect import getsource
        f = getsource(f)
    f_txt = f.lower()
    gby_keywords = ['np.vectorize(','np.where(','#gby',
        '.sum(','.max(','.min(','.unique(','.nunique(','.mean(','.median(','.percentile(',
        '.nansum(','np.nanmax(','np.nanmin(','flag1','rows_out','agg_out','#agg','.count_nonzero(']
    return True if any(word in f_txt for word in gby_keywords) else False

def load_feature_funcs(data_in: pd.DataFrame, cfg_model: Dict) -> pd.DataFrame:
    df_in_columns = data_in.columns.tolist()
    cfg_model['feature_funcs'] = {}
    cfg_model['feature_args'] = {}
    cfg_model['feature_groupby_flg'] = {}
    
    for feature in cfg_model['exec_seq']:
        if feature not in df_in_columns:

            if callable(cfg_model['features'][feature]):
                f = cfg_model['features'][feature]
                groupby_flg = is_groupby(f)
                args = list(f.__code__.co_varnames)[0:f.__code__.co_argcount]
            else:
                f = cfg_model['features'][feature]['udf']
                groupby_flg = is_groupby(f)
                exec(f) # Collect aggregated features here
                f = locals()[feature]
                args = cfg_model['features'][feature]['args']
        
            cfg_model['feature_funcs'][feature] = f
            cfg_model['feature_args'][feature] = args
            cfg_model['feature_groupby_flg'][feature] = groupby_flg
            
    return cfg_model
                    
def calc_datasets(data_in: pd.DataFrame, cfg_model: Dict) -> Tuple[pd.DataFrame, pd.DataFrame]:
    if cfg_model['missing_cols']:
        cfg_model['exec_seq'] = cfg_model['missing_cols'] + cfg_model['exec_seq'] # Ensure all missing cols are included
        logger.warning(f"calc_datasets - missing_cols added to exec_seq: {cfg_model['missing_cols']}")
    
    cfg_model = load_feature_funcs(data_in, cfg_model) # Ensure feature functions are loaded
    cfg_model['exec_fltrs'] = []
    cfg_model['exec_attrs'] = []
    data_out = {} # Collect aggregated features here
    agg_results = {}
    
    for feature in cfg_model['exec_seq']: # Follow execution sequence
        if feature not in data_in.columns: # Skip if feature already in input data
            logger.info("@calc_datasets - feature: {}".format(feature))
            
            # Prepare function inputs
            args_data = []
            in_flg = False
            out_flg = False
            func = cfg_model['feature_funcs'][feature]
            arg_list = cfg_model['feature_args'][feature]
            groupby_flg = cfg_model['feature_groupby_flg'][feature]

            # Process each argument
            for arg in arg_list:
                if arg in data_in.columns: # input from data_in only
                    in_flg = True
                    args_data.append(data_in[arg].values)
                    logger.debug("{}@data_in ".format(arg))

                elif arg in agg_results.keys(): # input from agg_results only
                    out_flg = True
                    args_data.append(agg_results[arg])
                    logger.debug("{}@agg_results ".format(arg))
                
                else:
                    # Argument not found in either data_in or agg_results
                    logger.error(f"Feature '{feature}': argument '{arg}' not found in data_in or agg_results")
                    continue  # or raise an exception
            # Validate all required arguments were found
            if len(args_data) != len(arg_list):
                logger.error(f"Feature '{feature}': expected {len(arg_list)} arguments, found {len(args_data)}")
                logger.error(f"  Expected: {arg_list}")
                logger.error(f"  Available in data_in: {list(data_in.columns)}")
                logger.error(f"  Available in agg_results: {list(agg_results.keys())}")
                continue  # Skip this feature
            
            # Determine processing type and execute
            if in_flg and not out_flg and not groupby_flg: # input from data only and no Agg present -> output on data level
                # Row-level filter
                logger.info("@calc_datasets - call FLTR {} with args({}) - flags {} {} {}".format(feature, len(arg_list), in_flg, out_flg, groupby_flg))
                cfg_model['exec_fltrs'].append(feature)
                data_in[feature] = np.vectorize(func)(*args_data)
                
            else:
                # Aggregated attribute
                logger.info("@calc_datasets - call ATTR args({})".format(len(arg_list)))
                logger.debug("@calc_datasets - *args_data: {}".format(args_data))
                cfg_model['exec_attrs'].append(feature)
                
                # Apply function to grouped data
                if in_flg and not out_flg:
                    # Arguments from data_in only - use groupby aggregation
                    grouped = data_in.groupby(cfg_model['group_by'])
                    agg_results[feature] = grouped.apply(lambda g: func(*[g[arg] for arg in arg_list]), include_groups=False)

                elif out_flg:
                    # Arguments include data_out - use already computed aggregates
                    agg_results[feature] = func(*args_data)
                
    # At the end, combine all aggregated results:
    if agg_results:
        data_out = pd.DataFrame(agg_results).reset_index()
        return data_in, data_out
    else:
        return data_in, None