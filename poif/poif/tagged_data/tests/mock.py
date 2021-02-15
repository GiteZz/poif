from typing import Any

from poif.tagged_data.base import TaggedData


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
