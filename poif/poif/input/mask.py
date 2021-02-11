from dataclasses import dataclass

from poif.input.base import DataSetObject
from poif.tagged_data.base import TaggedData


@dataclass
class MaskInput(TaggedData):
    image: TaggedData
    mask: TaggedData

    def output(self):
        return self.image.get_parsed(), self.mask.get_parsed()
