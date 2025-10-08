from src.logger import get_logger

logger = get_logger(__name__)


def fetch_feature(model, feature, cfg_model):
    import json

    # Load feature definition from local filesystem
    local_fs = 'feature_store'
    feat_path = '{}/{}/{}'.format(local_fs, model, feature)
    feature_path = '{}/{}.py'.format(feat_path, feature)
    feat_meta = '{}/metadata.json'.format(feat_path, feature)

    # Read the feature function and metadata
    with open(feature_path, "rb") as f1:
        func =  f1.read().decode('utf-8') 
        
    # Read the feature metadata
    with open(feat_meta, "rb") as f2:
        meta_data =  json.load(f2)

    return {'udf':func,'args':meta_data['args']}   

def get_feat_in_cols(rec_cnt, cfg_model, feat_idx, model, feature, input, exec_seq):
    logger.debug("{} feature: {}".format(feature, rec_cnt))
    
    # Base case: if feature is not defined, fetch or add to input
    if feature not in cfg_model['features']:
        if feature in feat_idx:
            cfg_model['features'][feature] = fetch_feature(model, feature, cfg_model) # Fetch and store the feature definition
            logger.info("Fetched feature: {} from model: {}".format(feature, model))
        else:
            if feature not in input:
                input.append(feature) # Add feature to input list if not found
                logger.info("Added feature: {} to input list".format(feature))
                
            return input, exec_seq # Add feature to execution sequence if not found

    # Recursive case: resolve dependencies
    if callable(cfg_model['features'][feature]):
        f = cfg_model['features'][feature]
        arg_list = list(f.__code__.co_varnames)[0:f.__code__.co_argcount] # get function argument names
    else:
        arg_list = cfg_model['features'][feature]['args'] # get argument names from metadata

    # Process each argument recursively
    for arg in arg_list:
        if arg not in cfg_model['group_by']:
            input, exec_seq = get_feat_in_cols(rec_cnt + 1, cfg_model, feat_idx, model, arg, input, exec_seq)

    # Finally, add the current feature to execution sequence if not already present
    if feature not in exec_seq:
        exec_seq.append(feature)

    return input, exec_seq

def get_feature_index(cfg_fidx, model):
    import os
    from pathlib import Path
    fs_path = ''
    if cfg_fidx['type'] == 'local':
        fs_path = cfg_fidx['path']

    look_path = '{}/{}'.format(fs_path, model)
    if not Path(look_path).exists():
        return []
    model_features = next(os.walk(look_path))[1]
    return model_features

def get_dependencies(cfg_fidx, model, cfg_model, output_cols):
    in_cols = list()
    exec_seq = list()
    feat_idx = get_feature_index(cfg_fidx, model)
    logger.info("feat_idx: {}".format(feat_idx))

    if 'features' not in cfg_model.keys():
        cfg_model['features'] = {}

    for feature in output_cols:
        in_cols, exec_seq = get_feat_in_cols(0, cfg_model, feat_idx, model, feature, in_cols, exec_seq)

    cfg_model['in_cols'] = in_cols
    cfg_model['exec_seq'] = exec_seq
    cfg_model['out_cols'] = output_cols

    return cfg_model