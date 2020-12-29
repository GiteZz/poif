import json
from dataclasses import dataclass
from pathlib import Path

from poif.data.versioning.base import TagMixin
from poif.typing import FileHash
from poif.utils import get_file_name_from_path, get_relative_path, hash_object


@dataclass
class VersionedFile(TagMixin):
    base_dir: Path
    file_path: Path

    @property
    def relative_path(self):
        return get_relative_path(self.base_dir, self.file_path)

    def set_tag(self):
        self._tag = hash_object(self.file_path)

    def get_remote_path(self):
        return f'{self.tag[:2]}/{self.tag[2:]}'

    def get_vfile_name(self):
        file_name = get_file_name_from_path(self.file_path)

        return f'{file_name}.vfile'

    def write_vfile_to_file(self, file: Path):
        with open(file, 'w') as f:
            json.dump({
                'path': self.relative_path,
                'tag': self.tag
            }, f)