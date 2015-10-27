import json
import os

from Logging import Logging


def load_params():
    params = json.loads(os.environ['Params'])
    Logging.get_logger(__name__).debug('Config File Loaded')
    return params
