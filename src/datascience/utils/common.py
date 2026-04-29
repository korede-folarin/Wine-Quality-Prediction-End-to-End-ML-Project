import os 
import yaml
from src.datascience import logger 
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
from box.exceptions import BoxValueError    


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"yaml file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e
    

@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    try:
        with open(path) as f:
            content = json.load(f)
            logger.info(f"json file: {path} loaded successfully")
            return ConfigBox(content)
    except Exception as e:
        raise e

@ensure_annotations
def save_model(path: Path, data: Any):
    joblib.dump(value = data, filename =path)
    logger.info(f"model saved at {path}")



@ensure_annotations  

def create_directories(path_to_directories: list, verbose =True):
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"created directory at: {path}")




@ensure_annotations  
def load_model(path: Path) -> Any:
    data = joblib.load(path)
    logger.info(f"model loaded from {path}")
    return data