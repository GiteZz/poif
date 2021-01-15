from abc import ABC
from typing import List, Dict

from dataclasses import dataclass, field

from poif.data.access.dataset import Dataset
from poif.data.data_templates.base import DatasetTemplate
from poif.data.datapoint.base import TaggedData
from poif.typing import RelFilePath, DatasetType


@dataclass
class DetectionAnnotation:
    category_id: int
    x: float
    y: float
    w: float
    h: float


@dataclass
class DetectionInput:
    image: TaggedData
    annotations: List[DetectionAnnotation] = field(default_factory=list)

    def add_annotation(self, annotation: DetectionAnnotation):
        self.annotations.append(annotation)


class DetectionTemplate(DatasetTemplate, ABC):
    def __init__(self):
        self.inputs = []


class CocoDetectionTemplate(DetectionTemplate):
    def __init__(self, annotation_files: Dict[DatasetType, RelFilePath], data_folders: Dict[DatasetType, RelFilePath]):
        super().__init__()

        self.annotation_files = annotation_files
        self.data_folders = data_folders

    def get_rel_file_mapping(self, inputs: List[TaggedData]) -> Dict[RelFilePath, TaggedData]:
        mapping = {}
        for tagged_data in inputs:
            mapping[tagged_data.relative_path] = tagged_data

        return mapping


    def parse_annotation_file(self, dataset_type: str, inputs: List[TaggedData]):
        mapping = self.get_rel_file_mapping(inputs)

        annotation_data = mapping[self.annotation_files[dataset_type]].get_parsed()

        img_id_to_index = {}
        for image_info in annotation_data['images']:
            img_id = image_info['id']
            img_id_to_index[img_id] = len(self.inputs)

            original_filename = self.data_folders[dataset_type] + f'/{image_info["file_name"]}'
            self.inputs.append(DetectionInput(image=mapping[original_filename]))

        for annotation in annotation_data['annotations']:
            img_id = annotation['image_id']
            current_input = self.inputs[img_id_to_index[img_id]]
            x, y, width, height = annotation['bbox']

            img_width = annotation_data['images'][img_id_to_index[img_id]]['width']
            img_height = annotation_data['images'][img_id_to_index[img_id]]['height']

            category_id = annotation['category_id']

            current_input.add_annotation(DetectionAnnotation(category_id=category_id,
                                                             x=x / img_width,
                                                             y=y / img_height,
                                                             w=width / img_width,
                                                             h=height / img_height)

    def complete(self, inputs: List[TaggedData]) -> Dataset:
        for dataset_type in self.annotation_files.keys():



    def create_file_system(self):
        pass