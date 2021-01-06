from pathlib import Path
from typing import List


class FileCreatorMixin:
    def __init__(self):
        self._created_files = []

    def add_created_file(self, file: Path):
        self._created_files.append(file)

    def get_created_files(self) -> List[Path]:
        return self._created_files