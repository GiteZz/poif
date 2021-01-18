from typing import List, Callable, Optional, Union

from poif.input.base import Input
from poif.input.transform.base import Transformation

ZeroOrMoreMetaInput = Optional[Union[Input, List[Input]]]
CallableDataPointTransformation = Callable[[Input], ZeroOrMoreMetaInput]
CallableDataSetTransformation = Callable[[List[Input]], List[Input]]


class MethodTransformation(Transformation):
    def __init__(self,
                 single_transform: CallableDataPointTransformation = None,
                 multi_transform: CallableDataSetTransformation = None
                 ):
        if single_transform is not None and multi_transform is not None:
            raise Exception('Both transformation types can\'t be defined')
        if single_transform is None and multi_transform is None:
            raise Exception('Define one transformation')

        self.single_transform = single_transform
        self.multi_transform = multi_transform

    def transform_single_input(self, ds_input: Input) -> List[Input]:
        if self.single_transform is not None:
            transformed_sample = self.single_transform(ds_input)
            if transformed_sample is None:
                return []
            if not isinstance(transformed_sample, list):
                return [transformed_sample]
            return transformed_sample
        else:
            return super().transform_single_input(ds_input)

    def transform_input_list(self, inputs: List[Input]) -> List[Input]:
        if self.multi_transform is not None:
            return self.multi_transform(inputs)
        else:
            return super().transform_input_list(inputs)