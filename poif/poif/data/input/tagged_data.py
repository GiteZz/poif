from dataclasses import dataclass

from poif.data.datapoint.base import TaggedData
from poif.data.input.base import Input


@dataclass
class TaggedDataInput(Input):
    tagged_data: TaggedData
    relative_path: str = None

    def __post_init__(self):
        self.relative_path = self.tagged_data.relative_path

    def output(self):
        return self.tagged_data.get_parsed()