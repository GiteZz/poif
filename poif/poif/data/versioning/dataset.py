import json
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Union

from dataclasses_json import dataclass_json

from poif.data.remote.base import Remote
from poif.data.remote.s3 import S3Config
from poif.data.versioning.directory import VersionedDirectory
from poif.data.versioning.file import VersionedFile
from poif.typing import ZeroOrMorePaths
from poif.utils import convert_zero_or_more, get_file_name_from_path

@dataclass
class ReadmeConfig:
    enabled: bool = True
    enable_filetree: bool = True
    enable_image_gallery: bool = True
    s3_config: S3Config = None

@dataclass
class CachingConfig:
    enabled: bool = True
    folder: Path = field(default_factory=lambda : Path.cwd() / '.data_versioning_cache')


@dataclass_json
@dataclass
class VersionedDataCollectionConfig:
    data_s3: S3Config
    dataset_name: str
    folders: List[str]
    files: List[str]
    git_url: str

    readme_s3: S3Config = None

    def write(self, file: Path):
        with open(file, 'w') as f:
            json.dump(self.to_dict(), f, indent=4)

    @staticmethod
    def load(config_path: Path) -> Optional['VersionedDatasetConfig']:
        with open(config_path, 'r') as f:
            return VersionedDatasetConfig.from_dict(json.load(f))


@dataclass
class VersionedDataset:
    base_dir: Path
    config: VersionedDatasetConfig

    directories: List[VersionedDirectory] = field(default_factory=list)
    files: List[VersionedFile] = field(default_factory=list)

    _created_files: List[str] = field(default_factory=list)

    def __post_init__(self):
        for directory in self.config.folders:
            actual_directory = self.base_dir / directory
            self.directories.append(VersionedDirectory(base_dir=self.base_dir, data_dir=actual_directory))

        for file in self.config.files:
            actual_file = self.base_dir / file
            self.files.append(VersionedFile(base_dir=self.base_dir, file_path=actual_file))

    def upload(self, remote: Remote):
        self.upload_directories(remote)
        self.upload_files(remote)

    def upload_directories(self, remote: Remote):
        for directory in self.directories:
            self.upload_directory_mapping(remote, directory)
            for file in directory.files:
                self.upload_file(remote, file)

    def upload_files(self, remote: Remote):
        for file in self.files:
            self.upload_file(remote, file)

    def upload_file(self, remote: Remote, file: VersionedFile):
        remote.upload_file(file.file_path, self.get_remote_name(file))

    def upload_directory_mapping(self, remote: Remote, directory: VersionedDirectory):
        mapping_file = Path(tempfile.mkstemp())
        directory.write_mapping_to_file(mapping_file)

        remote.upload_file(mapping_file, self.get_remote_name(directory))

    def get_remote_name(self, tag_object: Union[VersionedFile, VersionedDirectory]):
        return f'{self.name}/{tag_object.remote_file_name()}'

    def write_directories(self, save_directory: Path):
        for directory in self.directories:
            created_file = directory.write_vdir_to_folder(save_directory)

            self._created_files.append(created_file)

    def write_files(self, save_directory: Path):
        for directory in self.files:
            created_file = directory.write_vfile_to_folder(save_directory)

            self._created_files.append(created_file)

    def write_versioning_files(self, save_directory: Path):
        self.write_directories(save_directory)
        self.write_files(save_directory)

    def write_mappings(self, save_directory: Path):
        for directory in self.directories:
            directory.write_mapping_to_folder(save_directory)

    def get_created_files(self):
        return self._created_files

    def add_vdir_file(self, file: Path):
        filename = get_file_name_from_path(file)
        directory = self.get_dir_with_filename(filename)
        # TODO


    def get_dir_with_filename(self, filename: str) -> VersionedDirectory:
        for directory in self.directories:
            if directory.get_vdir_name() == filename:
                return directory
        raise Exception('Directory with filename not found')


    def add_vfile(self, file: Path):
        # TODO


