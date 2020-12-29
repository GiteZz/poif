from abc import ABC, abstractmethod

from dataclasses import dataclass, field
from hashlib import md5
from pathlib import Path
from typing import Dict, List
from itertools import islice
from poif.typing import FileHash
from collections import defaultdict

def get_relative_path(base_dir: Path, file: Path):
    """
    base_dir = Path('/home/user/datasets')
    file_path = Path('/home/user/datasets/name/train/01.jpg')

    => 'name/train/01.jpg'
    """
    return str(file)[len(str(base_dir)) + 1:]


def hash_object(file: Path):
    with open(file, 'rb') as f:
        hash = md5(f.read()).hexdigest()
    return hash


def hash_string(string: str):
    return md5(string.encode('utf-8')).hexdigest()


def get_file_name_from_path(file: Path):
    name_with_extension = file.parts[-1]
    name_without_extension = name_with_extension.split('.')[0]
    return name_without_extension

def get_extension_from_path(file: Path):
    name_with_extension = file.parts[-1]
    extension = name_with_extension.split('.')[-1]
    return extension


def get_file_depth(base_dir: Path, file: Path):
    return len(file.parts) - len(base_dir.parts)


def convert_zero_or_more(arg):
    if arg is None:
        return []
    if isinstance(arg, list):
        return arg
    return [arg]


@dataclass
class PathOperator(ABC):
    dir: Path
    dir_contents: Path.rglob = field(init=False)

    def __post_init__(self):
        self.dir_contents = self.dir.glob('*')

    def __iter__(self):
        return self

    def __next__(self) -> Path:
        next_dir_item = next(self.dir_contents)
        while not self.is_valid(next_dir_item):
            next_dir_item = next(self.dir_contents)

        return next_dir_item

    @abstractmethod
    def is_valid(self, path: Path):
        pass

# TODO remove duplication
class RecursivePathOperator(PathOperator, ABC):
    def __post_init__(self):
        self.dir_contents = self.dir.rglob('*')


class FileIterator(PathOperator):
    def is_valid(self, path: Path):
        return path.is_file()


class RecursiveFileIterator(RecursivePathOperator):
    def is_valid(self, path: Path):
        return path.is_file()


class DirectoryIterator(PathOperator):
    def is_valid(self, path: Path):
        return path.is_dir()


class RecursiveDirectoryIterator(RecursivePathOperator):
    def is_valid(self, path: Path):
        return path.is_dir()

@dataclass
class LimitLength:
    iterator: PathOperator
    limit: int

    count: int = 0

    was_stopped_early: bool = False

    def __iter__(self):
        return self

    def __next__(self):
        if self.count == self.limit:
            next(self.iterator)
            self.was_limited = True
            raise StopIteration

        next_iter_item = next(self.iterator)
        self.count += 1
        return next_iter_item


@dataclass
class InOrderPathIterator:
    dir: Path
    stack: List[Path] = None

    def __post_init__(self):
        self.stack = []
        self.add_dir_to_stack(self.dir)

    def __iter__(self):
        return self

    def __next__(self):
        if len(self.stack) > 0:
            first_item = self.stack.pop(0)
            if first_item.is_dir():
                self.add_dir_to_stack(first_item)
            return first_item

        else:
            raise StopIteration

    def add_dir_to_stack(self, directory: Path):
        dirs_in_dir = self.select_directories_from_directory(directory)
        files_in_dir = self.select_files_from_directory(directory)
        self.stack = dirs_in_dir + files_in_dir + self.stack

    def select_files_from_directory(self, directory: Path):
        return sorted_files_from_directory(directory)

    def select_directories_from_directory(self, directory: Path):
        return sorted_directories_from_directory(directory)


def sorted_files_from_directory(directory: Path):
    return sorted(list(FileIterator(directory)))


def sorted_directories_from_directory(directory: Path):
    return sorted(list(DirectoryIterator(directory)))


def files_by_extension(directory: Path, limit=None):
    extension_bins = defaultdict(list)

    for file in FileIterator(directory):
        extension = get_extension_from_path(file)

        if limit is not None and len(extension_bins[extension]) >= limit:
            continue

        extension_bins[extension].append(file)

    return extension_bins


def sorted_files_by_extension(directory: Path, limit=None):
    extension_bins = files_by_extension(directory, limit=None)

    for extension, files in extension_bins.items():
        extension_bins[extension] = sorted(files)[:limit]

    return extension_bins


def is_more_populated(directory: Path, value: int) -> bool:
    """
    Efficient way to check if a directory contains more files the value
    """
    remaining = value
    for _ in FileIterator(directory):
        remaining -= 1
        if remaining < 0:
            break

    return remaining < 0
