from dataclasses import dataclass

from poif.tagged_data.base import TaggedData
from poif.input.base import Input


@dataclass
class ClassificationInput(Input):
    tagged_data: TaggedData
    label: str

    def __post_init__(self):
        self.relative_path = self.tagged_data.relative_path

    def output(self):
        return self.tagged_data.get_parsed(), self.label
