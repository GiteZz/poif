from typing import Callable, List, Optional, Union

from poif.dataset.object.base import DataSetObject
from poif.dataset.operation.transform.base import Transformation

# Used for splitting the dataset, used for train/val/test split


ZeroOrMoreMetaInput = Optional[Union[DataSetObject, List[DataSetObject]]]
CallableDataPointTransformation = Callable[[DataSetObject], ZeroOrMoreMetaInput]
CallableDataSetTransformation = Callable[[List[DataSetObject]], List[DataSetObject]]


class SingleMethodTransformation(Transformation):
    def __init__(self, transform: CallableDataPointTransformation):
        self.transform = transform

    def transform_single_input(self, ds_input: DataSetObject) -> List[DataSetObject]:
        return self.transform(ds_input)


class MultiMethodTransformation(Transformation):
    def __init__(self, transform: CallableDataSetTransformation):
        self.transform = transform

    def transform_input_list(self, inputs: List[DataSetObject]) -> List[DataSetObject]:
        return self.transform(inputs)
