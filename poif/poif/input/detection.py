from typing import List

from dataclasses import dataclass, field

from poif.tagged_data.base import TaggedData

from poif.input.base import Image
from poif.input.annotations import BoundingBox


@dataclass
class DetectionInput(Image):
    def add_bounding_box(self, bbox: BoundingBox):
        self.annotations.append(bbox)

    def output(self):
        return self.data.get_parsed(), [annotation.output() for annotation in self.annotations]