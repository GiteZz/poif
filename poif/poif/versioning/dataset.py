import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from poif.config.collection import DataCollectionConfig
from poif.config.repo import DataRepoConfig
from poif.git.file import FileCreatorMixin
from poif.git.repo import GitRepo
from poif.repo.base import TaggedRepo
from poif.repo.file_remote import FileRemoteTaggedRepo, get_remote_repo_from_config
from poif.tagged_data.base import TaggedData
from poif.tagged_data.repo import RepoData
from poif.utils import get_file_name_from_path
from poif.versioning.directory import VersionedDirectory
from poif.versioning.file import VersionedFile


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
        self.get_dir_with_filename(filename)
        # TODO

    def get_dir_with_filename(self, filename: str) -> VersionedDirectory:
        for directory in self.directories:
            if directory.get_vdir_name() == filename:
                return directory
        raise Exception("Directory with filename not found")

    def add_vfile(self, file: Path):
        # TODO
        pass


class CollectionFromResourceDir(VersionedCollection):
    _mappings: List[TaggedData] = None
    _files: List[TaggedData] = None
    _tagged_repo: TaggedRepo = field(init=False)
    _resource_dir: Path = field(init=False)

    def __init__(self, resource_dir: Path):
        self._resource_dir = resource_dir
        collection_config = DataCollectionConfig.read(self._resource_dir / "collection_config.json")

        file_remote = collection_config.data_remote.config.get_configured_remote()
        data_folder = collection_config.data_remote.data_folder

        self._tagged_repo = FileRemoteTaggedRepo(remote=file_remote, data_folder=data_folder)

        self.retrieve_mappings()

        self.retrieve_mappings()

    def get_versioned_files(self, resource_dir: Path) -> List[Path]:
        return list(resource_dir.glob("*.vfile"))

    def get_versioned_directories(self, resource_dir: Path) -> List[Path]:
        return list(resource_dir.glob("*.vdir"))

    def retrieve_mappings(self):
        self._mappings = []
        vdirs = self.get_versioned_directories(self._resource_dir)

        for vdir_file in vdirs:
            with open(vdir_file, "r") as f:
                vdir_content = json.load(f)

            mapping = RepoData(
                relative_path=vdir_content["data_folder"] + ".mapping",
                repo=self._tagged_repo,
                tag=vdir_content["tag"],
            )

            self._mappings.append(mapping)

    def retrieve_files(self):
        self._files = []
        vfiles = self.get_versioned_files(self._resource_dir)

        for vfile in vfiles:
            with open(vfile, "r") as f:
                vfile_content = json.load(f)
            file = RepoData(
                relative_path=vfile_content["path"],
                repo=self._tagged_repo,
                tag=vfile_content["tag"],
            )
            self._files.append(file)

    def get_files_from_mappings(self):
        mappings = self.get_mappings()
        files = []

        for mapping in mappings:
            mapping_content = mapping.get_parsed()
            for tag, path in mapping_content.items():
                file = RepoData(relative_path=path, repo=self._tagged_repo, tag=tag)

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


@dataclass
class RepoVersionedCollection(CollectionFromResourceDir):
    _mappings: List[TaggedData] = None
    _files: List[TaggedData] = None
    _tagged_repo: TaggedRepo = field(init=False)
    _resource_dir: Path = field(init=False)

    def __init__(self, git_url: str, git_commit: str):
        repo = GitRepo(git_url=git_url, git_commit=git_commit)

        resource_dir_link = repo.base_dir / ".resource_folder"
        with open(resource_dir_link, "r") as f:
            relative_resource_dir = f.read()

        self._resource_dir = repo.base_dir / relative_resource_dir

        super().__init__(self._resource_dir)

        config = DataRepoConfig.read_from_package(repo.base_dir)
        self._tagged_repo = get_remote_repo_from_config(config.collection.data_remote)

        self.retrieve_mappings()


if __name__ == "__main__":
    repo = RepoVersionedCollection(
        git_url="https://github.ugent.be/gballege/minimal_pneumonia.git",
        git_commit="85d749fd6422af1a178013c45c304576939d3b4c",
    )

    all_files = repo.get_files()
    a = 5
