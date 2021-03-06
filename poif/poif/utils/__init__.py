from abc import ABC, abstractmethod
from collections import defaultdict
from dataclasses import dataclass, field
from enum import Enum
from hashlib import md5
from pathlib import Path
from typing import Any, Dict, Generator, List, Tuple

import cv2
import numpy as np

from poif.config import img_extensions


class ResizeMethod(Enum):
    NORMAL = 0
    PAD = 1


def get_img_size(img: np.ndarray) -> Tuple[int, int]:
    if len(img.shape) == 2:
        h, w = img.shape

        return h, w
    elif len(img.shape) == 3:
        h, w, c = img.shape

        return h, w
    else:
        raise Exception("Can't interpret image where len(shape) is not 2 or 3")


def resize_with_padding(img: np.ndarray, new_width: int, new_height: int, padding_value: int = 0) -> np.ndarray:
    h, w = get_img_size(img)

    original_ratio = w / h
    new_ratio = new_width / new_height

    if len(img.shape) == 3:
        canvas = np.zeros((new_height, new_width, img.shape[2]))
    else:
        canvas = np.zeros((new_height, new_width))

    if new_ratio > original_ratio:
        # new dimensions are proportionally wider than the original dimensions
        # This means that we will have to pad on the sides
        rescaling_width = int(original_ratio * new_height)
        padding_width = (new_width - rescaling_width) // 2

        rescaled_img = cv2.resize(img, (rescaling_width, new_height))

        canvas[:, padding_width : padding_width + rescaling_width] = rescaled_img

    else:
        rescaling_height = int(new_width / original_ratio)
        padding_height = (new_height - rescaling_height) // 2

        rescaled_img = cv2.resize(img, (new_width, rescaling_height))

        canvas[padding_height : padding_height + rescaling_height, :] = rescaled_img

    return canvas


def resize_img(
    img: np.ndarray, new_width: int, new_height: int, resize_method: ResizeMethod = ResizeMethod.PAD
) -> np.ndarray:
    if resize_method == ResizeMethod.NORMAL:
        return cv2.resize(img, (new_width, new_height))
    else:
        return resize_with_padding(img, new_width=new_width, new_height=new_height)


def get_relative_path(base_dir: Path, file: Path) -> str:
    """
    base_dir = Path('/home/user/datasets')
    file_path = Path('/home/user/datasets/name/train/01.jpg')

    => 'name/train/01.jpg'
    """
    return str(file)[len(str(base_dir)) + 1 :]


def hash_object(file: Path) -> str:
    with open(file, "rb") as f:
        hash = md5(f.read()).hexdigest()
    return hash


def hash_string(string: str) -> str:
    return md5(string.encode("utf-8")).hexdigest()


def get_file_name_from_path(file: Path) -> str:
    name_with_extension = file.parts[-1]
    name_without_extension = name_with_extension.split(".")[0]
    return name_without_extension


def get_extension_from_path(file: Path) -> str:
    name_with_extension = file.parts[-1]
    extension = name_with_extension.split(".")[-1]
    return extension


def is_image(path: Path) -> bool:
    return get_extension_from_path(path) in img_extensions


def get_file_depth(base_dir: Path, file: Path) -> int:
    return len(file.parts) - len(base_dir.parts)


def convert_zero_or_more(arg: Any) -> List:
    if arg is None:
        return []
    if isinstance(arg, list):
        return arg
    return [arg]


def has_newline(line: str) -> bool:
    if len(line) == 0:
        return False
    return line[-1] == "\n"


class Iterator(ABC):
    def __iter__(self):
        return self

    @abstractmethod
    def __next__(self):
        pass


class IteratorValidator:
    def is_valid(self, path: Path) -> bool:
        return True


class OnlyDirectory(IteratorValidator):
    def is_valid(self, path: Path) -> bool:
        return path.is_dir()


class OnlyFile(IteratorValidator):
    def is_valid(self, path: Path) -> bool:
        return path.is_file()


class OnlyImage(OnlyFile):
    def is_valid(self, path: Path) -> bool:
        return super().is_valid(path) and is_image(path)


class DirectoryExpander:
    def expand_directory(self, directory: Path):
        return directory.glob("*")


class RecursiveDirectoryExpand(DirectoryExpander):
    def expand_directory(self, directory: Path):
        return directory.rglob("*")


@dataclass
class PathOperator(Iterator, IteratorValidator, DirectoryExpander):
    dir: Path
    dir_contents: Generator[Path, None, None] = field(init=False)

    def __post_init__(self):
        self.dir_contents = self.expand_directory(self.dir)

    def __next__(self) -> Path:
        next_dir_item = next(self.dir_contents)
        while not self.is_valid(next_dir_item):
            next_dir_item = next(self.dir_contents)

        return next_dir_item


class FileIterator(OnlyFile, PathOperator):
    pass


class RecursiveFileIterator(OnlyFile, RecursiveDirectoryExpand, PathOperator):
    pass


class DirectoryIterator(OnlyDirectory, PathOperator):
    pass


class RecursiveDirectoryIterator(OnlyDirectory, RecursiveDirectoryExpand, PathOperator):
    pass


@dataclass
class LimitLength(Iterator):
    iterator: PathOperator
    limit: int

    count: int = 0

    was_stopped_early: bool = False

    def __next__(self):
        if self.count == self.limit:
            next(self.iterator)
            self.was_limited = True
            raise StopIteration

        next_iter_item = next(self.iterator)
        self.count += 1
        return next_iter_item


class CombinedIterator(Iterator):
    iterator_list: List[Iterator]
    current_iterator: Iterator

    def __init__(self):
        self.iterator_list = []
        self.current_iterator = None

    def append(self, iterator: Iterator):
        self.iterator_list.append(iterator)

    def prepend(self, iterator: Iterator):
        self.iterator_list.insert(0, iterator)

    def set_new_iterator(self):
        if len(self.iterator_list) == 0:
            raise StopIteration
        else:
            self.current_iterator = self.iterator_list.pop(0)

    def __next__(self):
        if self.current_iterator is None:
            self.set_new_iterator()

        if not isinstance(self.current_iterator, Iterator):
            value = self.current_iterator
            self.current_iterator = None
            return value

        while True:
            try:
                return next(self.current_iterator)
            except StopIteration:
                self.set_new_iterator()


@dataclass
class InOrderPathIterator(Iterator):
    dir: Path
    stack: List[Path] = field(default_factory=list)

    def __post_init__(self):
        self.add_dir_to_stack(self.dir)

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


def files_by_extension(directory: Path, limit: int = None):
    extension_bins: Dict[str, List[Path]] = defaultdict(list)

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


def is_close(value1: float, value2: float, max_diff: float = 0.0001):
    return abs(value1 - value2) < max_diff
