from abc import ABC
from enum import Enum
from typing import List

from poif.dataset.base import MultiDataset
from poif.dataset.object.annotations import BoundingBox
from poif.dataset.object.base import DataSetObject


class DetectionFileOutputFormat(str, Enum):
    coco = "coco"
    yolo = "yolo"
    yolov2 = "yolov2"
    yolov5 = "yolov5"


yolo_family = [
    DetectionFileOutputFormat.yolo,
    DetectionFileOutputFormat.yolov2,
    DetectionFileOutputFormat.yolov5,
]


def detection_input_to_yolo_annotation(ds_object: DataSetObject):
    output_str = ""
    yet_insert_newline = False
    for annotation in ds_object.annotations:
        if isinstance(annotation, BoundingBox):
            if yet_insert_newline:
                output_str += "\n"
            output_str += annotation.yolo_label()
            yet_insert_newline = True

    return output_str


class DetectionDataset(MultiDataset, ABC):
    def __init__(self):
        super().__init__()

        self.category_mapping = {}

    def create_sub_dataset_from_objects(self, new_objects: List):
        sub_dataset = DetectionDataset()
        sub_dataset.objects = new_objects
        sub_dataset.category_mapping = self.category_mapping

        return sub_dataset
