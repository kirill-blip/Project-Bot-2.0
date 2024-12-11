import json
import os

from service_collection import ServiceCollection


def load_psql_settings(app_type: str) -> str:
    if app_type == "development":
        file_name = 'psql_settings_develop.json'
    elif app_type == "production":
        file_name = 'psql_settings.json'
    else:
        ServiceCollection.LoggerService.error("Invalid app type")
    
    psql_settings:str = {}
    
    data_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'data')
    json_file_path = os.path.join(data_dir, file_name)

    with open(json_file_path, 'r') as f:
        data = json.load(f)
        psql_settings.update(data)
        
    ServiceCollection.LoggerService.info(f"Loaded psql settings from {json_file_path}")
        
    return psql_settings