from typing import List, Dict

from poif.dataset.base import MultiDataset, BaseDataset

from poif.tagged_data.base import TaggedData
from poif.input.detection import DetectionInput, DetectionAnnotation
from poif.typing import RelFilePath, DatasetType


class CocoDetectionTemplate(MultiDataset):
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

        new_inputs = []
        img_id_to_index = {}
        for image_info in annotation_data['images']:
            img_id = image_info['id']
            img_id_to_index[img_id] = len(self.inputs)

            original_filename = self.data_folders[dataset_type] + f'/{image_info["file_name"]}'
            new_inputs.append(DetectionInput(image=mapping[original_filename]))

        for annotation in annotation_data['annotations']:
            img_id = annotation['image_id']
            current_input = new_inputs[img_id_to_index[img_id]]
            x, y, width, height = annotation['bbox']

            img_width = annotation_data['images'][img_id_to_index[img_id]]['width']
            img_height = annotation_data['images'][img_id_to_index[img_id]]['height']

            category_id = annotation['category_id']

            current_input.add_annotation(DetectionAnnotation(category_id=category_id,
                                                             x=x / img_width,
                                                             y=y / img_height,
                                                             w=width / img_width,
                                                             h=height / img_height)
                                         )

        return new_inputs

    def form(self, data: List[TaggedData]):
        sub_dataset_names = list(self.annotation_files.keys())

        for subset in sub_dataset_names:
            new_inputs = self.parse_annotation_file(subset, data)
            self.inputs.extend(new_inputs)
            self.split_dict[subset] = new_inputs

    def create_file_system(self, data_format: str):
        pass


def detection_collection_to_coco_dict(inputs: List[DetectionInput]) -> Dict:
    coco_dict = {}
    coco_dict['images'] = []
    coco_dict['annotations'] = []
    for index, detection_input in enumerate(inputs):
        coco_dict['images'].append({
            'file_name': detection_input.image.relative_path,
            'id': index,
            'width': detection_input.img_width,
            'height': detection_input.img_height
        })
        for bbox in detection_input.annotations:
            coco_dict['annotations'].append({
                'image_id': index,
                'bbox': bbox.coco_bbox(detection_input.img_width, detection_input.img_height),
                'category_id': bbox.category_id
            })

    return coco_dict