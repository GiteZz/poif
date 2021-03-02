import random
from collections import defaultdict
from typing import Any, Callable, List

from poif.dataset.object.base import DataSetObject
from poif.dataset.operation.transform.base import Transformation

BinCreator = Callable[[DataSetObject], Any]


class LimitSamplesByBin(Transformation):
    def __init__(self, sample_limit: int, bin_creator: BinCreator):
        super().__init__()
        self.sample_limit = sample_limit
        self.bin_creator = bin_creator

    def transform_object_list(self, objects: List[DataSetObject]) -> List[DataSetObject]:
        items_per_bin = defaultdict(list)

        for ds_object in objects:
            items_per_bin[self.bin_creator(ds_object)].append(ds_object)

        new_objects = []
        for object_bin in items_per_bin.keys():
            for _ in range(self.sample_limit):
                item_list = items_per_bin[object_bin]
                if len(item_list) == 0:
                    break

                index_to_remove = random.randrange(len(item_list))  # get random index
                # swap with the last element
                item_list[index_to_remove], item_list[-1] = item_list[-1], item_list[index_to_remove]
                new_objects.append(item_list.pop())

        return new_objects
