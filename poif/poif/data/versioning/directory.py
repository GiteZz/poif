import json
from dataclasses import dataclass
from hashlib import md5
from operator import attrgetter
from pathlib import Path
from typing import Dict, List, Tuple

from tqdm import tqdm

from poif.data.datapoint.base import (LazyLoadedTaggedData, LazyTagged,
                                      TaggedData)
from poif.data.versioning.file import VersionedFile
from poif.typing import FileHash
from poif.utils import RecursiveFileIterator, get_relative_path


class Mapping(LazyLoadedTaggedData):
    mapping: Dict[FileHash, TaggedData]

    def __init__(self):
        super().__init__(relative_path="")

    @property
    def size(self) -> int:
        return len(self.get())

    @property
    def extension(self) -> str:
        return 'mapping'

    def get(self) -> bytes:
        return json.dumps(self.mapping).encode('utf-8')

    def set_tag(self):
        self._tag = self.get_mapping_hash()

    def get_mapping_hash(self):
        # Sort the files (Can't be sure that the file system gives them in order)
        sorted_tags = self.get_sorted_mapping()
        intermediate_hash = md5()

        for tag in sorted_tags:
            intermediate_hash.update(tag.encode('utf-8'))

        return intermediate_hash.hexdigest()

    def get_sorted_mapping(self) -> List[FileHash, TaggedData]:
        tags = list(self.mapping.keys())
        relative_files = [data.relative_path for data in self.mapping.values()]

        return [tag for _, tag in sorted(zip(relative_files, tags), key=lambda pair: pair[0])]


class VersionedDirectory(Mapping):
    base_dir: Path
    data_dir: Path = None

    _files: List[VersionedFile] = None

    def __init__(self, base_dir: Path, data_dir: Path, tag=None):
        super().__init__()

        self.base_dir = base_dir
        self.data_dir = data_dir

    @property
    def files(self):
        if self._files is None:
            self.set_files()
        return self._files

    def set_files(self):
        self._files = []
        for file in tqdm(RecursiveFileIterator(self.data_dir)):
            versioned_file = VersionedFile(base_dir=self.base_dir, file_path=file)
            self._files.append(versioned_file)

    def write_vdir_to_folder(self, directory: Path) -> Path:
        vdir_file= directory /self.get_vdir_name()
        with open(vdir_file, 'w') as f:
            json.dump({
                'data_folder': get_relative_path(self.base_dir, self.data_dir),
                'tag': self.tag
            }, f, indent=4)

        return vdir_file

    def write_mapping_to_folder(self, directory: Path) -> Path:
        mapping_dict = {file.tag: file.relative_path for file in self.files}
        mapping_file = directory / self.get_mapping_name()
        with open(mapping_file, 'w') as f:
            json.dump(mapping_dict, f)

        return mapping_file

    def get_vdir_name(self):
        file_name = self._get_file_name()

        return f'{file_name}.vdir'

    def get_mapping_name(self):
        file_name = self._get_file_name()

        return f'{file_name}.mapping'

    def _get_file_name(self):
        relative_path = get_relative_path(self.base_dir, self.data_dir)
        path_snake_case = relative_path.replace('/', '_')

        return path_snake_case

    def from_vdir_file(self, vdir_file: Path, base_dir: Path) -> 'VersionedDirectory':
        with open(vdir_file, 'r') as f:
            vdir_contents = json.load(f)

        self._tag = vdir_contents['tag']
        self.data_dir = self.base_dir / vdir_contents['data_folder']

    def load_mapping_file(self, file: Path):
        with open(file, 'r') as f:
            mapping = json.load(f)

        for tag, relative_file in mapping.items():
            versioned_file_path = self.base_dir / relative_file
            VersionedFile(base_dir=self.base_dir, file_path=versioned_file_path, _tag=tag)

    @property
    def size(self) -> int:
        return 0

    def get(self) -> bytes:
        self.m
