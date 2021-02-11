from collections import defaultdict
from typing import Dict, List

from poif.input.base import DataSetObject
from poif.typing import SubSetName

SplitterDict = Dict[SubSetName, List[DataSetObject]]


class Splitter:
    def split_single_input(self, ds_input: DataSetObject) -> SubSetName:
        raise Exception("Single input transform was not defined.")

    def split_input_list(self, inputs: List[DataSetObject]) -> SplitterDict:
        splitter_dict = defaultdict(list)
        for ds_input in inputs:
            splitter_dict[self.split_single_input(ds_input)].append(ds_input)

        return splitter_dict

    def __call__(self, inputs: List[DataSetObject]) -> SplitterDict:
        return self.split_input_list(inputs)
