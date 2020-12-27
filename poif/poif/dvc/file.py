import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict

from tqdm import tqdm

from poif.dvc.utils import file_to_relative_path, hash_object
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
        return file_to_relative_path(self.base_dir, self.file_path)

    def set_file_hash(self):
        self._tag = hash_object(self.file_path)

    def get_remote_path(self):
        return f'{self.tag[:2]}/{self.tag[2:]}'

    def write_vfile(self, file: Path):
        with open(file, 'w') as f:
            json.dump({
                'path': self.relative_path,
                'tag': self.tag
            }, f)
