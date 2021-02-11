from typing import Any, Callable, Dict, List, Optional, Union

from poif.input.base import DataSetObject

# Used for splitting the dataset, used for train/val/test split
CallableDataSetSplitter = Callable[
    [List[DataSetObject]], Dict[str, List[DataSetObject]]
]
CallableDataPointSplitter = Callable[[DataSetObject], str]


class Transformation:
    def transform_single_object(
        self, dataset_object: DataSetObject
    ) -> List[DataSetObject]:
        raise Exception("Single DataSetObject transform was not defined.")

    def transform_object_list(
        self, objects: List[DataSetObject]
    ) -> List[DataSetObject]:
        new_list = []
        for ds_DataSetObject in objects:
            new_list.extend(self.transform_single_object(ds_DataSetObject))

        return new_list

    def __call__(self, objects: List[DataSetObject]) -> List[DataSetObject]:
        return self.transform_object_list(objects)
