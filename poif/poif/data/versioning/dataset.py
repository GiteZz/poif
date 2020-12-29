import tempfile
from pathlib import Path
from typing import Union

from poif.data.remote.base import Remote
from poif.data.versioning.directory import VersionedDirectory
from poif.data.versioning.file import VersionedFile
from poif.typing import ZeroOrMorePaths
from poif.utils import convert_zero_or_more


class VersionedDataset:
    def __init__(self, name: str, base_dir: Path, directories: ZeroOrMorePaths, files: ZeroOrMorePaths):
        self.name = name
        self.base_dir = base_dir

        self.directories = []
        for directory in convert_zero_or_more(directories):
            self.directories.append(VersionedDirectory(base_dir=self.base_dir, data_dir=directory))

        self.files = []
        for file in convert_zero_or_more(files):
            self.files.append(VersionedFile(base_dir=self.base_dir, file_path=file))

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