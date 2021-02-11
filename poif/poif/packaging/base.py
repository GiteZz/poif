from abc import ABC, abstractmethod
from pathlib import Path

from poif.git.file import FileCreatorMixin


class Package(ABC, FileCreatorMixin):
    def __init__(self):
        super().__init__()
        self._created_files = []

    @classmethod
    @abstractmethod
    def get_resource_directory(cls, base_path: Path) -> Path:
        pass

    @abstractmethod
    def init(self):
        pass
