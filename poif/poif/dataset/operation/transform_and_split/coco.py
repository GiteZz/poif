from typing import Dict, List

from poif.dataset.object.base import DataSetObject
from poif.dataset.operation.split.base import SplitterDict
from poif.dataset.operation.transform.coco import SingleCoco
from poif.dataset.operation.transform_and_split.base import TransformAndSplit
from poif.typing import DatasetType, RelFilePath


class MultiCoco(TransformAndSplit):
    def __init__(self, annotation_files: Dict[DatasetType, RelFilePath], data_folders: Dict[DatasetType, RelFilePath]):
        self.annotation_files = annotation_files
        self.data_folders = data_folders

    def multi(self, inputs: List[DataSetObject]) -> SplitterDict:
        split_dict = {}

        for subset in self.annotation_files.keys():
            annotation_file = self.annotation_files[subset]
            data_folder = self.data_folders[subset]

            single_coco_transform = SingleCoco(annotation_file=annotation_file, data_folder=data_folder)
            new_objects = single_coco_transform(inputs)

            split_dict[subset] = new_objects

        return split_dict
