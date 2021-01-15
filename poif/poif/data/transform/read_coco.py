from dataclasses import dataclass, field
from pycocotools.coco import COCO
from pathlib import Path
import json
import sys
from typing import List

from poif.data.access.dataset import BaseDataset

ds_path = Path('/home/gilles/datasets/coco_val')

annotation_file = ds_path / 'annotations' / 'instances_val2014.json'

with open(annotation_file) as f:
    coco_content = json.load(f)


@dataclass
class DetectionAnnotation:
    category_id: int
    x: float
    y: float
    w: float
    h: float


@dataclass
class DetectionInput:
    image: Path
    annotations: List[DetectionAnnotation] = field(default_factory=list)

    def add_annotation(self, annotation: DetectionAnnotation):
        self.annotations.append(annotation)


class DetectionDataset(BaseDataset):
    inputs: List[DetectionInput]



class CocoDataset(DetectionDataset):
    def __init__(self, annotation_file: Path, img_path: Path, inputs: List[Input]):
        super().__init__(inputs)
        self.inputs = []
        with open(annotation_file) as f:
            # TODO find a way to stream into memory
            #  now the annotation file need to be present two times in memory for a short time
            annotation_content = json.load(f)

        img_id_to_index = {}
        for image_info in annotation_content['images']:
            img_id = image_info['id']
            img_id_to_index[img_id] = len(self.inputs)
            self.inputs.append(DetectionInput(image=img_path / image_info['file_name']))

        for annotation in annotation_content['annotations']:
            img_id = annotation['image_id']
            current_input = self.inputs[img_id_to_index[img_id]]
            x, y, width, height = annotation['bbox']

            img_width = annotation_content['images'][img_id_to_index[img_id]]['width']
            img_height = annotation_content['images'][img_id_to_index[img_id]]['height']

            category_id = annotation['category_id']

            current_input.add_annotation(DetectionAnnotation(category_id=category_id,
                                                             x=x/img_width,
                                                             y=y/img_height,
                                                             w=width/img_width,
                                                             h=height/img_height)
                                         )

ds = CocoDataset(annotation_file=annotation_file, img_path=ds_path / 'images')
