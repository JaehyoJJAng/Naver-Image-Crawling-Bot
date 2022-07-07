import json
import os.path
from pathlib import Path
from typing import Optional

BASE_DIR = Path(__file__).resolve().parent
JSON_FILE = os.path.join(BASE_DIR,'secret.json')

def get_secret(
        key: str,
        default_value : Optional[str] = None,
        json_path : str = JSON_FILE
):
    with open(json_path,'r',encoding='UTF-8') as f :
        secret_data = json.loads(f.read())

    try :
        return secret_data[key]
    except:
        if default_value :
            return default_value

        raise EnvironmentError(f'Set the {key} environment variable')

