from abc import ABC, abstractmethod

from dataclasses import dataclass, field
from hashlib import md5
from pathlib import Path
from typing import Dict, List
from itertools import islice
from poif.typing import FileHash


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
    name_without_extension = name_with_extension.split('.')[-1]
    return name_without_extension


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

    def __next__(self):
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


class FolderIterator(PathOperator):
    def is_valid(self, path: Path):
        return path.is_dir()


class RecursiveFolderIterator(RecursivePathOperator):
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
    file_per_directory_amount: int
    limit_reached_str: str = '...'
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

    def add_dir_to_stack(self, dir: Path):
        dirs_in_dir = sorted(list(FolderIterator(dir)))
        files_in_dir = sorted(list(LimitLength(FileIterator(dir), limit=self.file_per_directory_amount)))
        self.stack = dirs_in_dir + files_in_dir + self.stack
