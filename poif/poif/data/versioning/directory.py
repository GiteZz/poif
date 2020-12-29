import json
from dataclasses import dataclass
from hashlib import md5
from operator import attrgetter
from pathlib import Path

from tqdm import tqdm

from poif.data.versioning.base import TagMixin
from poif.data.versioning.file import VersionedFile
from poif.typing import FileHash
from poif.utils import FileIterator, get_relative_path


@dataclass
class VersionedDirectory(TagMixin):
    base_dir: Path
    data_dir: Path

    _files = None

    @property
    def files(self):
        if self._files is None:
            self.set_files()
        return self._files

    def set_files(self):
        self._files = []
        for file in tqdm(FileIterator(self.data_dir)):
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

    def write_vdir_to_file(self, file: Path):
        with open(file, 'w') as f:
            json.dump({
                'data_folder': get_relative_path(self.base_dir, self.data_dir),
                'tag': self.tag
            }, f)

    def write_mapping_to_file(self, file: Path):
        mapping_dict = {file.tag: file.relative_path for file in self.files}
        with open(file, 'w') as f:
            json.dump(mapping_dict, f)

    def get_vdir_name(self):
        file_name = self._get_file_name()

        return f'{file_name}.vdir'

    def get_mapping_name(self):
        file_name = self._get_file_name()

        return f'{file_name}.dir'

    def _get_file_name(self):
        relative_path = get_relative_path(self.base_dir, self.data_dir)
        path_snake_case = relative_path.replace('/', '_')

        return path_snake_case