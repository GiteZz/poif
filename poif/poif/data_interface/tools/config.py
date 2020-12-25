import json
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

import yaml
from dataclasses_json import dataclass_json

config_folder = Path.home() / '.daif'
config_folder.mkdir(exist_ok=True)

daif_config_file = config_folder / 'config.json'


@dataclass_json
@dataclass
class DatasetConfig:
    dvc_s3: 'S3Config'
    dataset_name: str
    data_folders: List[str]
    git_remote_url: str
    readme_s3: Optional['S3Config'] = None

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
class S3Config:
    bucket: str
    endpoint: str
    profile: str

    def to_dict(self):
        return vars(self)


@dataclass_json
@dataclass
class DaifConfig:
    current_origin: Optional['OriginConfig'] = None
    origins: Optional[List['OriginConfig']] = field(default_factory=list)

    def save(self):
        with open(daif_config_file, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)

        return daif_config_file

    @staticmethod
    def load() -> Optional['DaifConfig']:
        if daif_config_file.exists():
            with open(daif_config_file, 'r') as f:
                return DaifConfig.from_dict(json.load(f))
        else:
            return DaifConfig()


@dataclass_json
@dataclass
class OriginConfig:
    name: str
    git_url: Optional[str] = None
    git_api_key: Optional[str] = None
    default_s3: Optional[S3Config] = None
