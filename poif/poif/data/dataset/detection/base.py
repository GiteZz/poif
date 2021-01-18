from abc import ABC
from enum import Enum
from typing import List, Dict

from dataclasses import dataclass, field

from poif.data.dataset.base import MultiDataset
from poif.data.datapoint.base import TaggedData
from poif.typing import RelFilePath, DatasetType





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
