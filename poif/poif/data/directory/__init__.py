import json
from dataclasses import dataclass, field
from hashlib import md5
from operator import attrgetter
from pathlib import Path
from typing import Dict, List

from tqdm import tqdm

from poif.data.file import VersionedFile
from poif.utils import FileIterator, get_relative_path, hash_object
from poif.typing import FileHash


@dataclass
class VersionedDirectory:
    base_dir: Path
    data_dir: Path

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

    def set_versioned_files(self):
        self._versioned_files = []
        for file in tqdm(FileIterator(self.data_dir)):
            versioned_file = VersionedFile(base_dir=self.base_dir, file_path=file)
            self._versioned_files.append(versioned_file)

    def set_tag(self):
        self._tag = self.get_directory_hash()

    def get_directory_hash(self):
        # Sort the files (Can't be sure that the file system gives them in order)
        sorted_files = sorted(self.versioned_files, key=attrgetter("relative_path"))
        intermediate_hash = md5()

        for versioned_file in sorted_files:
            intermediate_hash.update(versioned_file.tag.encode('utf-8'))

        return intermediate_hash.hexdigest()

    def write_vdir_to_folder(self, folder: Path) -> Path:
        file_name = self._get_vdir_file_name()
        file_path = folder / file_name

        with open(file_path, 'w') as f:
            json.dump({
                'data_folder': get_relative_path(self.base_dir, self.data_dir),
                'tag': self.tag
            }, f)

        return file_path

    def write_mapping_to_folder(self, folder: Path) -> Path:
        file_name = self._get_vdir_file_name()
        file_path = folder / file_name

        mapping_dict = {file.tag: file.relative_path for file in self.versioned_files}
        with open(file_path, 'w') as f:
            json.dump(mapping_dict, f)

        return file_path

    def _get_vdir_file_name(self):
        file_name = self._get_file_name()

        return f'{file_name}.vdir'

    def _get_mapping_file_name(self):
        file_name = self._get_file_name()

        return f'{file_name}.dir'

    def _get_file_name(self):
        relative_path = get_relative_path(self.base_dir, self.data_dir)
        path_snake_case = relative_path.replace('/', '_')

        return path_snake_case
