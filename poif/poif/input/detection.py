from dataclasses import dataclass, field
from typing import List

from poif.input.annotations import BoundingBox
from poif.input.base import Image
from poif.tagged_data.base import TaggedData


@dataclass
class DetectionInput(Image):
    def add_bounding_box(self, bbox: BoundingBox):
        self.annotations.append(bbox)

    def output(self):
        return self.data.get_parsed(), [
            annotation.output() for annotation in self.annotations
        ]
