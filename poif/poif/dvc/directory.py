import json
from dataclasses import dataclass, field
from hashlib import md5
from operator import attrgetter
from pathlib import Path
from typing import Dict, List

from tqdm import tqdm

from poif.dvc.file import VersionedFile
from poif.dvc.utils import FileIterator, file_to_relative_path, hash_object
from poif.typing import FileHash


@dataclass
class VersionedDirectory:
    base_dir: Path
    data_folder: str

    data_path: Path = None

    _tag: FileHash = None
    _versioned_files = None

    @property
    def versioned_files(self):
        if self._versioned_files is None:
            self.set_versioned_files()
        return self._versioned_files

    @property
    def tag(self):
        if self._tag is None:
            self.set_tag()
        return self._tag

    def __post_init__(self):
        self.data_path = self.base_dir / self.data_folder

    def set_versioned_files(self):
        self._versioned_files = []
        for file in tqdm(FileIterator(self.data_path)):
            versioned_file = VersionedFile(base_dir=self.base_dir, file_path=file)
            self._versioned_files.append(versioned_file)

    def get_directory_hash(self):
        # Sort the files (Can't be sure that the file system gives them in order)
        sorted_files = sorted(self.versioned_files, key=attrgetter("relative_path"))
        intermediate_hash = md5()

        for versioned_file in sorted_files:
            intermediate_hash.update(versioned_file.tag.encode('utf-8'))

        return intermediate_hash.hexdigest()

    def set_tag(self):
        self._tag = self.get_directory_hash()

    def write_vdir(self, file: Path):
        with open(file, 'w') as f:
            json.dump({
                'data_folder': self.data_folder,
                'tag': self.tag
            },f)

    def write_mapping(self, file: Path):
        mapping_dict = {file.tag: file.relative_path for file in self.versioned_files}
        with open(file, 'w') as f:
            json.dump(mapping_dict, f)