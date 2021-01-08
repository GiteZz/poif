import json
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Union

from tqdm import tqdm

from poif.config.collection import DataCollectionConfig
from poif.data.git.file import FileCreatorMixin
from poif.data.repo.base import TaggedRepo
from poif.data.versioning.directory import VersionedDirectory
from poif.data.versioning.file import VersionedFile
from poif.utils import get_file_name_from_path


@dataclass
class VersionedDataset(FileCreatorMixin):
    base_dir: Path
    config: DataCollectionConfig

    directories: List[VersionedDirectory] = field(default_factory=list)
    files: List[VersionedFile] = field(default_factory=list)

    def __post_init__(self):
        for directory in self.config.folders:
            actual_directory = self.base_dir / directory
            self.directories.append(VersionedDirectory(base_dir=self.base_dir, data_dir=actual_directory))

        for file in self.config.files:
            actual_file = self.base_dir / file
            self.files.append(VersionedFile(base_dir=self.base_dir, file_path=actual_file))

    def upload(self, remote: TaggedRepo):
        self.upload_directories(remote)
        self.upload_files(remote)

    def upload_directories(self, remote: TaggedRepo):
        for directory in self.directories:
            remote.upload(directory)
            for file in tqdm(directory.files, desc=f'Uploading directory {directory.relative_path}'):
                self.upload_file(remote, file)

    def upload_files(self, remote: TaggedRepo):
        for file in self.files:
            self.upload_file(remote, file)

    def upload_file(self, remote: TaggedRepo, file: VersionedFile):
        remote.upload(file)

    def write_versioning_files(self, save_directory: Path):
        self.write_directories(save_directory)
        self.write_files(save_directory)

    def write_directories(self, save_directory: Path):
        for directory in self.directories:
            created_file = directory.write_vdir_to_folder(save_directory)

            self.add_created_file(created_file)

    def write_files(self, save_directory: Path):
        for directory in self.files:
            created_file = directory.write_vfile_to_folder(save_directory)

            self.add_created_file(created_file)

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
        pass


