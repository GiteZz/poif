from dataclasses import dataclass, field
from dataclasses_json import dataclass_json
from typing import List, Dict, Set
from pathlib import Path
import json

FileHash = str
RelFilePath = str

poif_base_folder = Path.home() / 'datasets'
poif_config_folder = poif_base_folder / 'config'
poif_ds_info_folder = poif_config_folder / 'ds_info'
poif_git_folder = poif_base_folder / 'git_repos'
poif_data_folder = poif_base_folder / 'data'


def setup_folders():
    poif_base_folder.mkdir(exist_ok=True)
    poif_config_folder.mkdir(exist_ok=True)
    poif_git_folder.mkdir(exist_ok=True)
    poif_data_folder.mkdir(exist_ok=True)
    poif_ds_info_folder.mkdir(exist_ok=True)

setup_folders()


@dataclass_json
@dataclass
class S3Config:
    url: str
    endpointurl: str
    profile: str

    bucket: str = field(init=False)
    folder: str = field(init=False)

    def __post_init__(self):
        url_no_URI = self.url.replace('s3://', '')
        self.bucket, self.folder = url_no_URI.split('/')





@dataclass_json
@dataclass
class DatasetInfo:
    files: Dict[FileHash, RelFilePath]
    s3_config: S3Config
    id: str

    def __post_init__(self):
        self.save()

    def save(self):
        save_file = poif_ds_info_folder / f'{self.id}.json'
        with open(save_file, 'w') as f:
            json.dump(self.to_dict(), f)

    @staticmethod
    def load(file: Path) -> 'DatasetInfo':
        with open(file, 'r') as f:
            ds_info_dict = json.load(f)
        return DatasetInfo.from_dict(ds_info_dict)


poif_ds_info_dict = {}
for file in poif_ds_info_folder.glob('*.json'):
    ds_info = DatasetInfo.load(file)
    poif_ds_info_dict[ds_info.id] = ds_info