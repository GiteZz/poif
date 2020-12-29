import json
import logging
from dataclasses import dataclass

from dataclasses_json import dataclass_json

from poif.config import datasets_default_config_file
from poif.data.remote.s3 import S3Config

logger = logging.getLogger(__name__)


# TODO Fix this ugliness
def get_default_config() -> 'DefaultConfig':
    # Fix the try/except block
    if datasets_default_config_file.exists():
        try:
            with open(datasets_default_config_file, 'r') as f:
                return DefaultConfig.from_dict(json.load(f))
        except:
            logging.warning('Default config could not be parsed')

    return DefaultConfig()


@dataclass_json
@dataclass
class DefaultConfig:
    data_s3: S3Config = None
    readme_s3: S3Config = None

    # TODO change this? config file definition is kind of ugly and the save/load is not pretty either
    def save(self):
        with open(datasets_default_config_file, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)
