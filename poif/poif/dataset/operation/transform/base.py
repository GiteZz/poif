from typing import List

from poif.dataset.object.base import DataSetObject

# Used for splitting the dataset, used for train/val/test split
from poif.dataset.operation.base import Operation


class Transformation(Operation):
    """
    This Operation is meant to
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
