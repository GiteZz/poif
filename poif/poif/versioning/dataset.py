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
from poif.typing import FileHash, RelFilePath
from poif.versioning.directory import VersionedDirectory
from poif.versioning.file import VersionedFile


class VersionedCollection(ABC):
    """
    This class is used to contain a collection of TaggedData. The get_files() is the most important function
    since this retrieves the TaggedData that can be use to construct a Dataset.
    """

    def __init__(self):
        super().__init__()

    @abstractmethod
    def get_files(self) -> List[TaggedData]:
        """
        This function retrieves the TaggedData for all the files present in the original dataset. This includes
        the versioned files and the files in the versioned directories.
        Returns:

        """

    @abstractmethod
    def _get_mappings(self) -> List[TaggedData]:
        pass

    def get_tagged_data(self) -> List[TaggedData]:
        """
        This function is used to retrieve all tagged data. This means that the mappings for the versioned
        directories are included too. The get_files functions only returns the TaggedData for the actual
        data files in the original dataset.
        Returns:

        """
        return self._get_mappings() + self.get_files()


@dataclass
class FromDiskVersionedCollection(VersionedCollection, FileCreatorMixin):
    base_dir: Path
    config: DataCollectionConfig

    directories: List[VersionedDirectory] = field(default_factory=list)
    files: List[VersionedFile] = field(default_factory=list)

    def __post_init__(self):
        super().__init__()
        for directory in self.config.folders:
            actual_directory = self.base_dir / directory
            self.directories.append(VersionedDirectory(base_dir=self.base_dir, data_dir=actual_directory))

        for file in self.config.files:
            actual_file = self.base_dir / file
            self.files.append(VersionedFile(base_dir=self.base_dir, file_path=actual_file))

    def get_files(self) -> List[TaggedData]:
        return self.files + self._files_from_directory()

    def _files_from_directory(self) -> List[TaggedData]:
        file_list = []
        for directory in self.directories:
            file_list.extend(directory.files)
        return file_list

    def _get_mappings(self) -> List[TaggedData]:
        return self.directories

    def write_versioning_files(self, save_directory: Path):
        self._write_directories_versioning_files(save_directory)
        self._write_files_versioning_files(save_directory)

    def _write_directories_versioning_files(self, save_directory: Path):
        for directory in self.directories:
            created_file = directory.write_vdir_to_folder(save_directory)

            self.add_created_file(created_file)

    def _write_files_versioning_files(self, save_directory: Path):
        for file in self.files:
            created_file = file.write_vfile_to_folder(save_directory)

            self.add_created_file(created_file)

    def _get_dir_with_filename(self, filename: str) -> VersionedDirectory:
        for directory in self.directories:
            if directory.get_vdir_name() == filename:
                return directory
        raise Exception("Directory with filename not found")


class ResourceDirCollection(VersionedCollection):
    _mappings: List[TaggedData] = None
    _files: List[TaggedData] = None
    _tagged_repo: TaggedRepo = field(init=False)
    _resource_dir: Path = field(init=False)

    def __init__(self, resource_dir: Path):
        super().__init__()
        self._resource_dir = resource_dir
        collection_config = DataCollectionConfig.read(self._resource_dir / "collection_config.json")

        file_remote = collection_config.data_remote.config.get_configured_remote()
        data_folder = collection_config.data_remote.data_folder

        self._tagged_repo = FileRemoteTaggedRepo(remote=file_remote, data_folder=data_folder)

        self._retrieve_mappings()

    def _get_versioned_files(self) -> List[Path]:
        return list(self._resource_dir.glob("*.vfile"))

    def _get_versioned_directories(self) -> List[Path]:
        return list(self._resource_dir.glob("*.vdir"))

    def _retrieve_mappings(self):
        self._mappings = []
        vdirs = self._get_versioned_directories()

        for vdir_file in vdirs:
            with open(vdir_file, "r") as f:
                vdir_content = json.load(f)

            mapping = self._create_repo_file(vdir_content["data_folder"] + ".mapping", vdir_content["tag"])

            self._mappings.append(mapping)

    def _create_repo_file(self, relative_path: RelFilePath, tag: FileHash) -> RepoData:
        return RepoData(
            relative_path=relative_path,
            repo=self._tagged_repo,
            tag=tag,
        )

    def _retrieve_files(self):
        self._files = []
        vfiles = self._get_versioned_files()

        for vfile in vfiles:
            with open(vfile, "r") as f:
                vfile_content = json.load(f)

            file = self._create_repo_file(vfile_content["path"], vfile_content["tag"])
            self._files.append(file)

    def _get_files_from_mappings(self):
        mappings = self._get_mappings()
        files = []

        for mapping in mappings:
            mapping_content = mapping.get_parsed()
            for tag, path in mapping_content.items():
                file = RepoData(relative_path=path, repo=self._tagged_repo, tag=tag)

                files.append(file)
        return files

    def get_files(self) -> List[TaggedData]:
        if self._files is None:
            self._retrieve_files()

        return self._files + self._get_files_from_mappings()

    def _get_mappings(self) -> List[TaggedData]:
        if self._mappings is None:
            self._retrieve_mappings()
        return self._mappings


@dataclass
class GitRepoCollection(ResourceDirCollection):
    """
    VersionedCollection that is initialized from a git repository and commit. With these two variables
    all references from the original collection can be retrieved.
    """

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

        self._retrieve_mappings()
