from copy import deepcopy
from pydantic import BaseModel
from pathlib import Path
from typing import List, Union, Optional

from poif.cli.datasets.tools.cli import (answer_from_list, simple_input,
                                         yes_with_question, multi_input, path_input)
from poif.config.remotes import S3Config, remote_types

poif_config_folder = Path.home() / '.poif'
poif_config_folder.mkdir(exist_ok=True)

datasets_default_config_file = poif_config_folder / 'config.json'

img_extensions = ['bmp', 'pbm', 'pgm', 'ppm', 'sr', 'ras', 'jpeg', 'jpg', 'jpe', 'jp2', 'tiff', 'tif', 'png']


class Config(BaseModel):
    @classmethod
    def read(cls, file: Path):
        with open(file, 'r') as f:
            json_content = f.read()
        return cls.parse_raw(json_content)

    def write(self, file: Path):
        with open(file, 'w') as f:
            f.write(self.json(exclude={'default_location'}))

    @classmethod
    def get_default(cls):
        if cls.default_location is not None and cls.default_location().is_file():
            return cls.read(cls.default_location())

        return None

    @staticmethod
    def default_location() -> Optional[Path]:
        return None


class CacheConfig(Config):
    enable: bool
    data_storage_location: Path = None
    git_storage_location: Path = None
    cache_uploads: bool = None

    @staticmethod
    def default_location() -> Optional[Path]:
        return poif_config_folder / 'cache_config.json'

    @staticmethod
    def prompt():
        enable = yes_with_question('Enable caching on disk?')
        data_storage = path_input('Data storage location?', default=Path.cwd() / 'data_cache' / 'data')
        git_storage = path_input('Git storage location? Used to avoid duplicated cloning.',
                                 default=Path.cwd() / 'data_cache' / 'git'
                                 )
        cache_upload = yes_with_question('Cache on upload?', default=True)

        return CacheConfig(enable=enable,
                           data_storage_location=data_storage,
                           git_storage_location=git_storage,
                           cache_uploads=cache_upload
                           )


class RemoteConfig(Config):
    remote_type: str = None
    data_folder: str = None
    config: Union[S3Config] = None

    @staticmethod
    def default_location() -> Optional[Path]:
        return poif_config_folder / 'remote_config.json'

    @staticmethod
    def prompt(default_remote: 'RemoteConfig' = None) -> 'RemoteConfig':
        # Given remote has priority
        if default_remote is None:
            default_remote = RemoteConfig.get_default()

        new_config = RemoteConfig()
        new_config.remote_type = answer_from_list('Remote type?', list(remote_types.keys()), default=None if default_remote is None else default_remote.remote_type)

        if default_remote is not None and isinstance(default_remote.config, remote_types[new_config.remote_type]):
            new_config.config = remote_types[new_config.remote_type].prompt(default=default_remote.config)
        else:
            new_config.config = remote_types[new_config.remote_type].prompt()

        new_config.data_folder = simple_input('Data folder on remote?', default=new_config.data_folder)

        return new_config


class ReadmeConfig(Config):
    enable: bool
    enable_filetree: bool
    enable_image_gallery: bool
    image_remote: RemoteConfig = None

    @staticmethod
    def default_location() -> Optional[Path]:
        return poif_config_folder / 'readme_config.json'

    @classmethod
    def prompt(cls, default_readme: 'ReadmeConfig' = None) -> 'ReadmeConfig':
        # given readme config has priority
        if default_readme is None:
            default_readme = cls.get_default()

        # If the version loaded from disk is still not loaded
        if default_readme is None:
            default_remote = RemoteConfig.get_default()
        else:
            default_remote = default_readme.image_remote

        default_enable = None if default_readme is None else default_readme.enable
        default_enable_filetree = None if default_readme is None else default_readme.enable_filetree
        default_enable_gallery = None if default_readme is None else default_readme.enable_image_gallery

        enable = yes_with_question("Create readme?", default=default_enable)
        if not enable:
            return ReadmeConfig(enable=False, enable_filetree=False, enable_image_gallery=False)

        enable_filetree = yes_with_question('Add filetree?', default=default_enable_filetree)
        enable_image_gallery = yes_with_question('Add image galley?', default=default_enable_gallery)

        if enable_image_gallery:
            image_remote = RemoteConfig.prompt(default_remote)
        else:
            image_remote = None

        return ReadmeConfig(enable=enable,
                            enable_filetree=enable_filetree,
                            enable_image_gallery=enable_image_gallery,
                            image_remote=image_remote
                            )


class PythonPackageConfig(Config):
    enable: bool = True

    @staticmethod
    def default_location() -> Optional[Path]:
        return poif_config_folder / 'package_config.json'

    @staticmethod
    def prompt():
        enable = yes_with_question("Pack as python package?", default=True)

        return PythonPackageConfig(enable=enable)


class DataCollectionConfig(Config):
    collection_name: str
    folders: List[str]
    files: List[str]
    data_remote: RemoteConfig

    @staticmethod
    def prompt(data_default: RemoteConfig = None):
        if data_default is None:
            data_default = RemoteConfig.get_default()
        collection_name = simple_input('Name of data collection?')

        folders = multi_input('Folder to track?', empty_allowed=True)
        files = multi_input('Files to track?', empty_allowed=True)

        remote_config = ReadmeConfig.prompt(data_default)

        return DataCollectionConfig(collection_name=collection_name, folders=folders, files=files, data_remote=remote_config)


class DataRepoConfig(Config):
    collection: DataCollectionConfig
    readme: ReadmeConfig
    python_package: PythonPackageConfig

    @staticmethod
    def prompt():
        collection = DataCollectionConfig.prompt()
        readme = ReadmeConfig.prompt()
        package = PythonPackageConfig.prompt()

        return DataRepoConfig(collection=collection, readme=readme, python_package=package)
