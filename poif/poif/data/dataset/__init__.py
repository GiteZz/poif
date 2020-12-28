from typing import List, Optional
from pathlib import Path

from poif.data.directory import VersionedDirectory
from poif.data.file import VersionedFile
from poif.typing import ZeroOrMorePaths


def convert_zero_or_more(arg):
    if arg is None:
        return []
    if isinstance(arg, list):
        return arg
    return [arg]


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