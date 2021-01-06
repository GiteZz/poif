from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path
from typing import List

from poif.data.git.file import FileCreatorMixin


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


from .python_package import PythonPackage


class PackageOptions(str, Enum):
    python_package = 'package'


packages = {
    PackageOptions.python_package: PythonPackage
}