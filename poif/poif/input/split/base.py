from typing import List, Dict

from poif.input.base import Input
from poif.typing import SubSetName
from collections import defaultdict


SplitterDict = Dict[SubSetName, List[Input]]


class Splitter:
    def split_single_input(self, ds_input: Input) -> SubSetName:
        raise Exception('Single input transform was not defined.')

    def split_input_list(self, inputs: List[Input]) -> SplitterDict:
        splitter_dict = defaultdict[list]
        for ds_input in inputs:
            splitter_dict[self.split_single_input(ds_input)].append(ds_input)

        return splitter_dict

    def __call__(self, inputs: List[Input]) -> SplitterDict:
        return self.split_input_list(inputs)