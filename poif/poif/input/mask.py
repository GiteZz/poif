from dataclasses import dataclass

from poif.tagged_data.base import TaggedData
from poif.input.base import Input


@dataclass
class MaskInput(Input):
    image: TaggedData
    mask: TaggedData

    def output(self):
        return self.image.get_parsed(), self.mask.get_parsed()
