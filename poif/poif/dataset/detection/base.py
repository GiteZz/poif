from abc import ABC
from enum import Enum

from poif.dataset.base import MultiDataset


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
