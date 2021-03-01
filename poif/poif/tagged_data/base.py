from abc import ABC, abstractmethod
from typing import Any, Optional

from poif.parser.base import ParseMixin
from poif.typing import FileHash


class BinaryData(ABC):
    @property
    @abstractmethod
    def size(self) -> int:
        pass

    @abstractmethod
    def get(self) -> bytes:
        pass


class StringBinaryData(BinaryData):
    def __init__(self, data_str: str):
        self.data = data_str

    @property
    def size(self) -> int:
        return len(self.data)

    def get(self) -> bytes:
        return bytes(self.data.encode("utf-8"))


class TaggedData(BinaryData, ParseMixin, ABC):
    def __init__(self, relative_path: str, tag: Optional[FileHash] = None):
        super().__init__()
        self._tag = tag
        self._relative_path = relative_path

    @property
    def tag(self):
        return self._tag

    @property
    def extension(self) -> str:
        # TODO check better
        return self.relative_path.split("/")[-1].split(".")[-1]

    @property
    def relative_path(self):
        return self._relative_path

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


class TaggedPassthrough(TaggedData):
    def __init__(self, tagged_data: TaggedData):
        self.tagged_data = tagged_data
        super().__init__(self.tagged_data.relative_path)

    @property
    def size(self) -> int:
        return self.tagged_data.size

    def get(self) -> bytes:
        return self.tagged_data.get()

    def get_parsed(self) -> Any:
        return self.tagged_data.get_parsed()

    @property
    def tag(self):
        return self.tagged_data.tag

    @property
    def extension(self) -> str:
        # TODO check better
        return self.tagged_data.extension

    @property
    def relative_path(self):
        return self.tagged_data.relative_path
