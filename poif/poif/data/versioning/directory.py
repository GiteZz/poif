import json
from typing import List

from dataclasses import dataclass
from hashlib import md5
from operator import attrgetter
from pathlib import Path

from tqdm import tqdm

from poif.data.versioning.base import LazyLoadingTagged
from poif.data.versioning.file import VersionedFile
from poif.typing import FileHash
from poif.utils import RecursiveFileIterator, get_relative_path


@dataclass
class VersionedDirectory(LazyLoadingTagged):
    base_dir: Path
    data_dir: Path = None

    _files: List[VersionedFile] = None

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

    def set_tag(self):
        self._tag = self.get_directory_hash()

    def get_directory_hash(self):
        # Sort the files (Can't be sure that the file system gives them in order)
        sorted_files = sorted(self.files, key=attrgetter("relative_path"))
        intermediate_hash = md5()

        for versioned_file in sorted_files:
            intermediate_hash.update(versioned_file.tag.encode('utf-8'))

        return intermediate_hash.hexdigest()

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

    def load_vdir_file(self, file: Path):
        with open(file, 'r') as f:
            vdir_contents = json.load(f)

        self._tag = vdir_contents['tag']
        self.data_dir = self.base_dir / vdir_contents['data_folder']

    def load_mapping_file(self, file: Path):
        with open(file, 'r') as f:
            mapping = json.load(f)

        for tag, relative_file in mapping.items():
            versioned_file_path = self.base_dir / relative_file
            VersionedFile(base_dir=self.base_dir, file_path=versioned_file_path, _tag=tag)
