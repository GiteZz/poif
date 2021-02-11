from dataclasses import dataclass

from poif.input.base import DataSetObject
from poif.tagged_data.base import TaggedData


@dataclass
class TaggedDataInput(DataSetObject):
    relative_path: str = None

    def __post_init__(self):
        self.relative_path = self.data.relative_path

    def output(self):
        return self.data.get_parsed()
