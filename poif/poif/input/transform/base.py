
from typing import Any, Callable, Dict, List, Optional, Union

from poif.input.base import Input


# Used for splitting the dataset, used for train/val/test split
CallableDataSetSplitter = Callable[[List[Input]], Dict[str, List[Input]]]
CallableDataPointSplitter = Callable[[Input], str]


class Transformation:
    def transform_single_input(self, ds_input: Input) -> List[Input]:
        raise Exception('Single input transform was not defined.')

    def transform_input_list(self, inputs: List[Input]) -> List[Input]:
        new_list = []
        for ds_input in inputs:
            new_list.extend(self.transform_single_input(ds_input))

        return new_list

    def __call__(self, inputs: List[Input]) -> List[Input]:
        return self.transform_input_list(inputs)



