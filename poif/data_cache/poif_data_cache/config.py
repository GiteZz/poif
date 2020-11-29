from pathlib import Path
import json
from typing import Dict
from poif_data_cache.data_handling.config import DatasetInfo

base_folder = Path.home() / 'datasets'
config_folder = base_folder / 'config'
git_folder = base_folder / 'git_repos'
data_folder = base_folder / 'data'


RepoURL = str
FolderName = str


def setup_folders():
    base_folder.mkdir(exist_ok=True)
    config_folder.mkdir(exist_ok=True)
    git_folder.mkdir(exist_ok=True)
    data_folder.mkdir(exist_ok=True)


def get_dvc_mapping() -> Dict[RepoURL, DvcConfig]:
    dvc_config = config_folder / 'config.json'
    if dvc_config.exists():
        with open(dvc_config, 'r') as f:
            dvc_config = json.load(f)
        return dvc_config
    else:
        return {}

dvc_config = get_dvc_mapping()