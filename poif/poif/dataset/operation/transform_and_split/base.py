from collections import defaultdict
from typing import List, Tuple

from poif.dataset.object.base import DataSetObject
from poif.dataset.operation.base import Operation
from poif.dataset.operation.split.base import SplitterDict
from poif.typing import SubSetName


class TransformAndSplit(Operation):
    def single(self, ds_input: DataSetObject) -> Tuple[SubSetName, List[DataSetObject]]:
        raise Exception("Single object transform was not defined.")

    def multi(self, inputs: List[DataSetObject]) -> SplitterDict:
        splitter_dict = defaultdict(list)
        for ds_input in inputs:
            subset, new_objects = self.single(ds_input)
            splitter_dict[subset].extend(new_objects)

        return splitter_dict

    def __call__(self, inputs: List[DataSetObject]) -> SplitterDict:
        return self.multi(inputs)
