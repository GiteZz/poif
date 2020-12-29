from dataclasses import dataclass, field
from hashlib import md5
from pathlib import Path
from typing import Dict

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


def convert_zero_or_more(arg):
    if arg is None:
        return []
    if isinstance(arg, list):
        return arg
    return [arg]

@dataclass
class FileIterator:
    dir: Path
    dir_contents: Path.rglob = field(init=False)

    def __post_init__(self):
        self.dir_contents = self.dir.rglob('*')

    def __iter__(self):
        return self

    def __next__(self):
        next_dir_item = next(self.dir_contents)
        while not next_dir_item.is_file():
            next_dir_item = next(self.dir_contents)

        return next_dir_item