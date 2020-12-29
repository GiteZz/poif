import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from dataclasses_json import dataclass_json

from poif.data.remote.s3 import S3Config, S3Remote

logger = logging.getLogger(__name__)


class PoifConfig:
    @property
    def config_path(self) -> Path:
        config_folder = Path.home() / '.poif'
        config_folder.mkdir(exist_ok=True)

        return config_folder


def get_default_config() -> 'DefaultConfig':
    config_file = DefaultConfig.config_file

    # Fix the try/except block
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                return DefaultConfig.from_dict(json.load(f))
        except:
            logging.warning('Default config could not be parsed')

    return DefaultConfig()


@dataclass_json
@dataclass
class VersionedDatasetConfig:
    data_s3: S3Config
    readme_s3: S3Config
    dataset_name: str
    data_folders: List[str]
    git_url: str

    @staticmethod
    def get_config_file():
        config_path = Path.cwd() / '.dataset'
        config_path.mkdir(exist_ok=True)
        return config_path / 'config.json'

    def save(self):
        dataset_config_file = DatasetConfig.get_config_file()
        dataset_config_file.parent.mkdir(exist_ok=True)

        with open(dataset_config_file, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)

        return dataset_config_file

    @staticmethod
    def load() -> Optional['DatasetConfig']:
        dataset_config_file = DatasetConfig.get_config_file()
        with open(dataset_config_file, 'r') as f:
            return DatasetConfig.from_dict(json.load(f))


@dataclass_json
@dataclass
class DefaultConfig:
    data_s3: S3Config = None
    readme_s3: S3Config = None

    @property
    def config_file(self) -> Path:

        return PoifConfig.config_path / 'config.json'

    # TODO change this? config file definition is kind of ugly and the save/load is not pretty either
    def save(self):
        with open(self.config_file, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)
