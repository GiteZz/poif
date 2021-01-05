from abc import ABC, abstractmethod
from typing import Any

from poif.data.parser.base import ParseMixin
from poif.typing import FileHash


class TaggedData(ABC, ParseMixin):
    _tag: FileHash = None
    _relative_path: str = None

    def __init__(self, relative_path: str, tag: FileHash = None):
        self._tag = tag
        self._relative_path = relative_path

    @property
    def tag(self):
        return self._tag

    @property
    @abstractmethod
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
