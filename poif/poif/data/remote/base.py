from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from poif.typing import FileHash


@dataclass
class Remote(ABC):
    @abstractmethod
    def get_file(self, file_name: str) -> bytes:
        pass

    @abstractmethod
    def get_object_size(self, file_name: str):
        pass

    def download_file(self, tag: FileHash, dest: Path):
        file = self.get_file(tag)

        with open(dest, 'wb') as f:
            f.write(file)

    @abstractmethod
    def upload_file(self, source: Path, dest: str):
        pass
