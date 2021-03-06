from dataclasses import dataclass
from pathlib import Path
from typing import List

from dataclasses_json import dataclass_json

from poif.cli.tools.cli import multi_input, simple_input
from poif.config.base import Config
from poif.config.remote.base import RemoteConfig


@dataclass_json
@dataclass
class DataCollectionConfig(Config):
    name: str
    folders: List[str]
    files: List[str]
    data_remote: RemoteConfig

    @classmethod
    def get_default_name(cls) -> str:
        return "collection_config.json"

    @staticmethod
    def prompt(data_default: RemoteConfig = None):
        if data_default is None:
            data_default = RemoteConfig.get_default()

        cwd_dir_name = Path.cwd().parts[-1]
        collection_name = simple_input("Name of data collection?", default=cwd_dir_name)

        folders = multi_input("Folder to track?", empty_allowed=True)
        files = multi_input("Files to track?", empty_allowed=True)

        print("Configuration for the data remote.")
        remote_config = RemoteConfig.prompt(data_default)

        return DataCollectionConfig(
            name=collection_name,
            folders=folders,
            files=files,
            data_remote=remote_config,
        )
