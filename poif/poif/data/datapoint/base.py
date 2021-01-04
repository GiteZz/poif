from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any

from poif.data.parser.base import ParseMixin
from poif.data.remote.base import TaggedRepo
from poif.typing import FileHash
from poif.utils import hash_object


class TaggedData(ABC, ParseMixin):
    _tag: FileHash = None
    _relative_path: str = None

    def __init__(self, relative_path: str, tag: FileHash = None):
        self._tag = tag
        self._relative_path = relative_path

    @property
    def tag(self):
        return self._tag

    @abstractmethod
    @property
    def size(self) -> int:
        pass

    @property
    def extension(self) -> str:
        # TODO check better
        return self.relative_path.split('/')[-1].split('.')[-1]

    @property
    def relative_path(self):
        return self._relative_path

    @abstractmethod
    def get(self) -> bytes:
        pass

    def get_parsed(self) -> Any:
        return self.parse_file(self.get(), self.extension)


class LazyLoadedTaggedData(TaggedData, ABC):
    @property
    def tag(self):
        if self._tag is None:
            self.set_tag()
        return self._tag

    @abstractmethod
    def set_tag(self):
        pass


class DiskData(LazyLoadedTaggedData):
    file_path: Path = None

    def __init__(self, file_path: Path, relative_path: str, tag: FileHash = None):
        super().__init__(relative_path, tag)
        self.file_path = file_path

    @property
    def size(self) -> int:
        return self.file_path.stat().st_size

    def get(self) -> bytes:
        with open(self.file_path, 'rb') as f:
            file_bytes = f.read()
        return file_bytes

    def set_tag(self):
        self._tag = hash_object(self.file_path)


class RepoData(TaggedData):
    repo: TaggedRepo

    @property
    def size(self) -> int:
        return self.repo.get_object_size(self)

    def get(self) -> bytes:
        return self.repo.get(self)