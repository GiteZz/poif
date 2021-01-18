from abc import ABC
from enum import Enum
from typing import List, Dict

from dataclasses import dataclass, field

from poif.data.dataset.base import MultiDataset
from poif.data.datapoint.base import TaggedData
from poif.typing import RelFilePath, DatasetType

from poif.data.input.base import Input


@dataclass
class DetectionAnnotation:
    category_id: int
    x: float
    y: float
    w: float
    h: float

    def coco_bbox(self, img_width, img_height):
        return f'{int(self.x * img_width)} {int(self.y * img_height)} ' \
               f'{int(self.w * img_width)} {int(self.h * img_height)}'

    def output(self):
        return [self.category_id, self.x, self.y, self.w, self.h]


@dataclass
class DetectionInput(Input):
    image: TaggedData
    img_width: int = None
    img_height: int = None
    annotations: List[DetectionAnnotation] = field(default_factory=list)

    def add_annotation(self, annotation: DetectionAnnotation):
        self.annotations.append(annotation)

    def output(self):
        return [annotation.output() for annotation in self.annotations]