from abc import ABC
from enum import Enum
from typing import List, Dict

from dataclasses import dataclass, field

from poif.data.dataset.base import MultiDataset
from poif.data.datapoint.base import TaggedData
from poif.typing import RelFilePath, DatasetType


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


@dataclass
class DetectionInput:
    image: TaggedData
    img_width: int = None
    img_height: int = None
    annotations: List[DetectionAnnotation] = field(default_factory=list)

    def add_annotation(self, annotation: DetectionAnnotation):
        self.annotations.append(annotation)


class DetectionFileOutputFormat(str, Enum):
    coco = 'coco'
    yolo = 'yolo'
    yolov2 = 'yolov2'
    yolov5 = 'yolov5'


class DetectionTemplate(MultiDataset, ABC):
    def __init__(self):
        self.inputs = []

    def create_file_system(self, data_format: str):
        pass
