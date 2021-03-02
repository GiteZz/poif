from collections import defaultdict
from typing import Any, Dict, List

from poif.dataset.object.base import DataSetObject
from poif.dataset.operation.split.base import Splitter, SplitterDict
from poif.dataset.operation.transform.sampler import BinCreator


class SplitByBin(Splitter):
    def __init__(self, bins: Dict[str, List[Any]], bin_creator: BinCreator):
        super().__init__()
        self.bins = bins
        self.bin_creator = bin_creator

    def split_input_list(self, objects: List[DataSetObject]) -> SplitterDict:
        items_per_bin = defaultdict(list)

        for ds_object in objects:
            items_per_bin[self.bin_creator(ds_object)].append(ds_object)

        return items_per_bin
