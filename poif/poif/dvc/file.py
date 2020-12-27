import json
from pathlib import Path
from typing import Dict

from dataclasses import dataclass, field
from tqdm import tqdm

from poif.dvc.utils import get_md5_hash, file_to_relative_path, get_directory_hash, FileIterator
from poif.typing import FileHash


@dataclass
class VersionedFile:
    base_dir: Path
    file_path: Path

    tag: str = field(init=False)
    rel_path: str = field(init=False)

    def set_file_hash(self):
        self.tag = get_md5_hash(self.file_path)

    def set_rel_file_path(self):


    def init(self):
        self.set_file_hash()
        self.set_rel_file_path()

    def write_vdir(self, file: Path):
        if self.directory_hash is not None:
            self.init()

        with open(file, 'w') as f:
            json.dump({
                'data_folder': self.data_folder,
                'tag': self.directory_hash
            },f)

    def write_mapping(self, file: Path):
        if self.directory_hash is not None:
            self.init()
        with open(file, 'w') as f:
            json.dump(self.tag_to_file,f)