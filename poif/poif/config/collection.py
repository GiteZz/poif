from typing import List

from poif.cli.datasets.tools.cli import simple_input, multi_input
from poif.config.base import Config
from poif.config.remote.base import RemoteConfig


class DataCollectionConfig(Config):
    name: str
    folders: List[str]
    files: List[str]
    data_remote: RemoteConfig

    @classmethod
    def get_default_name(cls) -> str:
        return 'collection_config.json'

    @staticmethod
    def prompt(data_default: RemoteConfig = None):
        if data_default is None:
            data_default = RemoteConfig.get_default()
        collection_name = simple_input('Name of data collection?')

        folders = multi_input('Folder to track?', empty_allowed=True)
        files = multi_input('Files to track?', empty_allowed=True)

        print('Configuration for the data remote.')
        remote_config = RemoteConfig.prompt(data_default)

        return DataCollectionConfig(name=collection_name, folders=folders, files=files, data_remote=remote_config)