from typing import Callable, List, Optional, Union

from poif.dataset.object.base import DataSetObject
from poif.dataset.object.transform.base import Transformation

ZeroOrMoreMetaInput = Optional[Union[DataSetObject, List[DataSetObject]]]
CallableDataPointTransformation = Callable[[DataSetObject], ZeroOrMoreMetaInput]
CallableDataSetTransformation = Callable[[List[DataSetObject]], List[DataSetObject]]


class MethodTransformation(Transformation):
    def __init__(
        self,
        single_transform: CallableDataPointTransformation = None,
        multi_transform: CallableDataSetTransformation = None,
    ):
        if single_transform is not None and multi_transform is not None:
            raise Exception("Both transformation types can't be defined")
        if single_transform is None and multi_transform is None:
            raise Exception("Define one transformation")

        self.single_transform = single_transform
        self.multi_transform = multi_transform

    def transform_single_input(self, ds_input: DataSetObject) -> List[DataSetObject]:
        if self.single_transform is not None:
            transformed_sample = self.single_transform(ds_input)
            if transformed_sample is None:
                return []
            if not isinstance(transformed_sample, list):
                return [transformed_sample]
            return transformed_sample
        else:
            return super().transform_single_object(ds_input)

    def transform_input_list(self, inputs: List[DataSetObject]) -> List[DataSetObject]:
        if self.multi_transform is not None:
            return self.multi_transform(inputs)
        else:
            return super().transform_object_list(inputs)
