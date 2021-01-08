import json
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Union

from tqdm import tqdm

from poif.config.collection import DataCollectionConfig
from poif.config.repo import DataRepoConfig
from poif.data.datapoint.base import TaggedData
from poif.data.datapoint.repo import RepoData
from poif.data.git.file import FileCreatorMixin
from poif.data.git.repo import GitRepo
from poif.data.packaging.base import packages
from poif.data.repo.base import TaggedRepo
from poif.data.repo.file_remote import get_remote_repo_from_config
from poif.data.versioning.directory import VersionedDirectory
from poif.data.versioning.file import VersionedFile
from poif.utils import get_file_name_from_path
from abc import ABC, abstractmethod


class VersionedCollection(ABC):
    @abstractmethod
    def get_files(self) -> List[TaggedData]:
        pass

    @abstractmethod
    def get_mappings(self) -> List[TaggedData]:
        pass

    def get_tagged_data(self) -> List[TaggedData]:
        return self.get_mappings() + self.get_files()


@dataclass
class FromDiskVersionedCollection(VersionedCollection, FileCreatorMixin):
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

    def get_files(self) -> List[TaggedData]:
        return self.files + self.files_from_directory()

    def files_from_directory(self) -> List[TaggedData]:
        file_list = []
        for directory in self.directories:
            file_list.extend(directory.files)
        return file_list

    def get_mappings(self) -> List[TaggedData]:
        return self.directories

    def write_versioning_files(self, save_directory: Path):
        self.write_directories_versioning_files(save_directory)
        self.write_files_versioning_files(save_directory)

    def write_directories_versioning_files(self, save_directory: Path):
        for directory in self.directories:
            created_file = directory.write_vdir_to_folder(save_directory)

            self.add_created_file(created_file)

    def write_files_versioning_files(self, save_directory: Path):
        for file in self.files:
            created_file = file.write_vfile_to_folder(save_directory)

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


@dataclass
class RepoVersionedCollection(VersionedCollection):
    _mappings: List[TaggedData] = None
    _files: List[TaggedData] = None
    _tagged_repo: TaggedRepo = field(init=False)
    _resource_dir: Path = field(init=False)

    def __init__(self, git_url: str, git_commit: str):

        repo = GitRepo(git_url=git_url, git_commit=git_commit)
        config = DataRepoConfig.read_from_package(repo.base_dir)
        tagged_repo = get_remote_repo_from_config(config.collection.data_remote)
        self._tagged_repo = tagged_repo

        self._resource_dir = packages[config.package.type].get_resource_directory(base_dir=repo.base_dir)

        self.retrieve_mappings()

    def get_versioned_files(self, resource_dir: Path) -> List[Path]:
        return list(resource_dir.glob('*.vfile'))

    def get_versioned_directories(self, resource_dir: Path) -> List[Path]:
        return list(resource_dir.glob('*.vdir'))

    def retrieve_mappings(self):
        self._mappings = []
        vdirs = self.get_versioned_directories(self._resource_dir)

        for vdir_file in vdirs:
            with open(vdir_file, 'r') as f:
                vdir_content = json.load(f)

            mapping = RepoData(relative_path=vdir_content['data_folder'] + '.mapping',
                               repo=self._tagged_repo,
                               tag=vdir_content['tag']
                               )

            self._mappings.append(mapping)

    def retrieve_files(self):
        self._files = []
        vfiles = self.get_versioned_files(self._resource_dir)

        for vfile in vfiles:
            with open(vfile, 'r') as f:
                vfile_content = json.load(f)
            file = RepoData(relative_path=vfile_content['path'],
                               repo=self._tagged_repo,
                               tag=vfile_content['tag']
                               )
            self._files.append(file)

    def get_files_from_mappings(self):
        mappings = self.get_mappings()
        files = []

        for mapping in mappings:
            mapping_content = mapping.get_parsed()
            for tag, path in mapping_content.items():
                file = RepoData(relative_path=path,
                                repo=self._tagged_repo,
                                tag=tag
                                )

                files.append(file)
        return files

    def get_files(self) -> List[TaggedData]:
        if self._files is None:
            self.retrieve_files()

        return self._files + self.get_files_from_mappings()

    def get_mappings(self) -> List[TaggedData]:
        if self._mappings is None:
            self.retrieve_mappings()
        return self._mappings


if __name__ == "__main__":
    repo = RepoVersionedCollection(git_url='http://localhost:360/root/datasets-5729607b-372d-4422-bd2b-1db968099ef9.git', git_commit='fa2aa394f3a69654ecdf2e6e2c8b6a244ff482cb')

    all_files = repo.get_files()
    a = 5

