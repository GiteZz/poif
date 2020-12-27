from hashlib import md5
from pathlib import Path
from typing import Dict

from dataclasses import dataclass, field

from poif.typing import FileHash


def file_to_relative_path(base_dir: Path, file: Path):
    return str(file)[len(str(base_dir)):]


def get_md5_hash(file: Path):
    with open(file, 'rb') as f:
        hash = md5(f.read()).hexdigest()
    return hash


def get_directory_hash(tag_to_file: Dict[FileHash, str]):

    intermediate_hash = md5()

    for key in sorted(tag_to_file.keys()):
        intermediate_hash.update(tag_to_file[key].encode('utf-8'))

    return intermediate_hash.hexdigest()


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