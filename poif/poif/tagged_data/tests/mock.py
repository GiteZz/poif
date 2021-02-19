from typing import Any

from poif.tagged_data.base import TaggedData
from poif.tests import get_img_file
from poif.utils import hash_object


class MockTaggedData(TaggedData):
    def __init__(self, relative_path: str, data: Any):
        super().__init__(relative_path)
        self.data = data

    @property
    def size(self) -> int:
        return 0

    def get(self) -> bytes:
        raise NotImplementedError

    def get_parsed(self) -> Any:
        return self.data


class ImageMockTaggedData(TaggedData):
    def __init__(self, relative_path: str):
        super().__init__(relative_path)

        self.img_on_disk = get_img_file(extension=super().extension)
        self._tag = hash_object(self.img_on_disk)
        with open(self.img_on_disk, "rb") as f:
            self.bytes = f.read()

    @property
    def size(self) -> int:
        return len(self.bytes)

    def get(self) -> bytes:
        return self.bytes
