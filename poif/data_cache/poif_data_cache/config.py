from pathlib import Path
import json
from typing import Dict

base_folder = Path.home() / 'datasets'
config_folder = base_folder / 'config'
git_folder = base_folder / 'git_repos'
data_folder = base_folder / 'datasets'


RepoURL = str
FolderName = str


def load_config() -> Dict[RepoURL, FolderName]:
    base_folder.mkdir(exist_ok=True)
    config_folder.mkdir(exist_ok=True)
    git_folder.mkdir(exist_ok=True)
    data_folder.mkdir(exist_ok=True)

    mapping_dict = config_folder / 'git_mapping.json'
    if mapping_dict.exists():
        with open(mapping_dict, 'r') as f:
            git_mapping = json.load(f)
        return git_mapping
    else:
        return {}

git_mapping = load_config()