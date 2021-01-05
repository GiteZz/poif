from copy import deepcopy
from pydantic import BaseModel
from pathlib import Path
from typing import List, Union

from poif.cli.datasets.tools.cli import (answer_from_list, simple_input,
                                         yes_with_question)
from poif.config.remotes import S3Config, remote_types

poif_config_folder = Path.home() / '.poif'
poif_config_folder.mkdir(exist_ok=True)

datasets_default_config_file = poif_config_folder / 'config.json'

img_extensions = ['bmp', 'pbm', 'pgm', 'ppm', 'sr', 'ras', 'jpeg', 'jpg', 'jpe', 'jp2', 'tiff', 'tif', 'png']


class CacheConfig(BaseModel):
    enable: bool
    data_storage_location: Path
    git_storage_location: Path
    cache_uploads: bool


class RemoteConfig(BaseModel):
    remote_type: str = None
    data_folder: str = None
    config: Union[S3Config] = None

    @staticmethod
    def prompt(default: 'RemoteConfig' = None) -> 'RemoteConfig':
        new_config = RemoteConfig()
        new_config.remote_type = answer_from_list('Remote type?', list(remote_types.keys()))

        if default is not None and isinstance(default.config, remote_types[new_config.remote_type]):
            new_config.config = remote_types[new_config.remote_type].prompt(default=default.config)
        else:
            new_config.config = remote_types[new_config.remote_type].prompt()

        new_config.data_folder = simple_input('Data folder on remote?', default=new_config.data_folder)

        return new_config


class ReadmeConfig(BaseModel):
    enable: bool = True
    enable_filetree: bool = True
    enable_image_gallery: bool = True
    image_remote: RemoteConfig = None

    @staticmethod
    def prompt(default: 'ReadmeConfig' = None) -> 'ReadmeConfig':
        if default is None:
            new_config = ReadmeConfig()
        else:
            new_config = deepcopy(default)

        new_config.enable = yes_with_question("Create readme?", default=new_config.enable)
        if not new_config.enable:
            return new_config

        new_config.enable_filetree = yes_with_question('Add filetree?', default=new_config.enable_filetree)
        new_config.enable_image_gallery = yes_with_question('Add image galley?', default=new_config.enable_image_gallery)
        if new_config.enable_image_gallery:
            new_config.image_remote = RemoteConfig.prompt(new_config.image_remote)

        return new_config


class PythonPackageConfig(BaseModel):
    enable: bool = True


class DataCollectionConfig(BaseModel):
    dataset_name: str
    folders: List[str]
    files: List[str]
    data_remote: RemoteConfig


class DataRepoConfig(BaseModel):
    collection: DataCollectionConfig
    readme: ReadmeConfig
    python_package: PythonPackageConfig
