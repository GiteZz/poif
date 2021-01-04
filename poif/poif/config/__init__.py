from enum import Enum
from pathlib import Path
from dataclasses import dataclass

from poif.data.remote.s3 import S3Config
from typing import Union, List

poif_config_folder = Path.home() / '.poif'
poif_config_folder.mkdir(exist_ok=True)

datasets_default_config_file = poif_config_folder / 'config.json'

img_extensions = ['bmp', 'pbm', 'pgm', 'ppm', 'sr', 'ras', 'jpeg', 'jpg', 'jpe', 'jp2', 'tiff', 'tif', 'png']


class RemoteType(Enum):
    S3: 1


@dataclass
class CacheConfig:
    enable: bool
    data_storage_location: Path
    git_storage_location: Path
    cache_uploads: bool


@dataclass
class RemoteConfig:
    remote: RemoteType
    config: Union[S3Config]


@dataclass
class ReadmeConfig:
    enable: bool
    enable_filetree: bool
    enable_image_gallery: bool
    image_remote: RemoteConfig


@dataclass
class PythonPackageConfig:
    enable: bool


@dataclass
class DataCollectionConfig:
    dataset_name: str
    folders: List[str]
    files: List[str]
    data_remote: RemoteConfig


@dataclass
class DataRepoConfig:
    collection: DataCollectionConfig
    readme: ReadmeConfig
    python_package: PythonPackageConfig
