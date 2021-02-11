from pathlib import Path
from typing import List

from poif.tagged_data.base import LazyLoadedTaggedData
from poif.typing import FileHash
from poif.utils import get_relative_path, hash_object


class DiskData(LazyLoadedTaggedData):
    file_path: Path = None

    def __init__(self, file_path: Path, relative_path: str, tag: FileHash = None):
        super().__init__(relative_path, tag)
        self.file_path = file_path

    @property
    def size(self) -> int:
        return self.file_path.stat().st_size

    def get(self) -> bytes:
        with open(self.file_path, "rb") as f:
            file_bytes = f.read()
        return file_bytes

    def set_tag(self):
        self._tag = hash_object(self.file_path)

    @staticmethod
    def from_folder(folder: Path) -> List["DiskData"]:
        data = []
        for file in folder.rglob("*"):
            rel_path = get_relative_path(base_dir=folder, file=file)
            data.append(DiskData(relative_path=rel_path, file_path=file))

        return data
