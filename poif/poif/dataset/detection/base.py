from abc import ABC
from enum import Enum
from pathlib import Path

from poif.dataset.base import MultiDataset


class DetectionFileOutputFormat(str, Enum):
    coco = 'coco'
    yolo = 'yolo'
    yolov2 = 'yolov2'
    yolov5 = 'yolov5'


class DetectionDataset(MultiDataset, ABC):
    def __init__(self):
        super().__init__()

    def create_file_system(self, data_format: DetectionFileOutputFormat, base_folder: Path):
        if data_format == DetectionFileOutputFormat.yolov5:


