from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from poif.typing import FileHash


@dataclass
class Remote(ABC):
    @abstractmethod
    def get_file(self, tag: FileHash) -> bytes:
        pass

    @abstractmethod
    def get_object_size(self, tag: FileHash):
        pass

    def download_file(self, tag: FileHash, dest: Path):
        file = self.get_file(tag)

        with open(dest, 'wb') as f:
            f.write(file)
