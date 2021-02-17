from typing import Any

from poif.dataset.object.base import DataSetObject
from poif.tagged_data.tests.mock import MockTaggedData
from poif.typing import RelFilePath


class TripleDataSetObject(DataSetObject):
    def output(self) -> Any:
        return self.tagged_data.get_parsed() * 3


class MockDataSetObject(DataSetObject):
    def __init__(self, rel_path: RelFilePath, data: Any):
        super().__init__(MockTaggedData(rel_path, data))
