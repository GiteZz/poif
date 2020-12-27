import json
from pathlib import Path
from typing import Dict

from dataclasses import dataclass, field
from tqdm import tqdm

from poif.dvc.utils import get_md5_hash, file_to_relative_path, get_directory_hash, FileIterator
from poif.typing import FileHash


@dataclass
class VersionedDirectory:
    base_dir: Path
    data_folder: str

    data_path: Path = field(init=False)

    directory_hash: str = field(init=False)
    tag_to_file: Dict[FileHash, str] = field(default_factory=dict)

    def __post_init__(self):
        self.data_path = self.base_dir / self.data_folder

    def set_file_hashes(self):
        for file in tqdm(FileIterator(self.data_path)):
            file_hash = get_md5_hash(file)
            rel_file = file_to_relative_path(self.data_path, file)

            self.tag_to_file[file_hash] = rel_file

    def set_base_directory_hash(self):
        self.directory_hash = get_directory_hash(self.tag_to_file)

    def init(self):
        self.set_file_hashes()
        self.set_base_directory_hash()

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