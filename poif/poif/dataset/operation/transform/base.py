from typing import List

from poif.dataset.object.base import DataSetObject

# Used for splitting the dataset, used for train/val/test split
from poif.dataset.operation.base import Operation


class Transformation(Operation):
    """
    This Operation is meant to change the DataSetObjects in the Dataset. Therefore two functions are created.
    The transform_single_object is used for transformations that only need access to one DataSetObject, an example of
    this is adding labels from the objects relative path. For this no information outside that single input is needed.
    The single_object function will by default be called from the transform_object_list function. This means that
    either you have to override the transform_single_object of override the transform_object_list. The
    transform_object_list is used for transformations where the entire dataset is needed. An example of this
    is reading a COCO annotation file, hereby the annotation file first need to be found and then used. Another
    example is evenly limiting the amount of samples per bin.
    """

    def transform_single_object(self, dataset_object: DataSetObject) -> List[DataSetObject]:
        raise Exception("Single DataSetObject transform was not defined.")

    def transform_object_list(self, objects: List[DataSetObject]) -> List[DataSetObject]:
        new_list = []
        for ds_DataSetObject in objects:
            new_list.extend(self.transform_single_object(ds_DataSetObject))

        return new_list

    def __call__(self, objects: List[DataSetObject]) -> List[DataSetObject]:
        return self.transform_object_list(objects)
