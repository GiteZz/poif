import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict

from tqdm import tqdm

from poif.utils import get_relative_path, hash_object, get_file_name_from_path
from poif.typing import FileHash


@dataclass
class VersionedFile:
    base_dir: Path
    file_path: Path

    _tag: FileHash = None

    @property
    def tag(self):
        if self._tag is None:
            self.set_file_hash()
        return self._tag

    @property
    def relative_path(self):
        return get_relative_path(self.base_dir, self.file_path)

    def set_file_hash(self):
        self._tag = hash_object(self.file_path)

    def get_remote_path(self):
        return f'{self.tag[:2]}/{self.tag[2:]}'

    def get_file_name(self):
        file_name = get_file_name_from_path(self.file_path)

        return f'{file_name}.vfile'

    def write_vfile_to_folder(self, folder: Path) -> Path:
        file_path = folder / self.get_file_name()
        with open(file_path, 'w') as f:
            json.dump({
                'path': self.relative_path,
                'tag': self.tag
            }, f)

        return file_path