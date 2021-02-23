from collections import defaultdict
from typing import Callable, Dict, List, Optional

from poif.dataset.object.base import DataSetObject
from poif.typing import SubSetName
from poif.utils.splitting import random_split

SplitterDict = Dict[SubSetName, List[DataSetObject]]


class Splitter:
    def split_single_input(self, ds_input: DataSetObject) -> Optional[SubSetName]:
        raise Exception("Single object transform was not defined.")

    def split_input_list(self, inputs: List[DataSetObject]) -> SplitterDict:
        splitter_dict = defaultdict(list)
        for ds_input in inputs:
            subset = self.split_single_input(ds_input)
            if subset is not None:
                splitter_dict[subset].append(ds_input)

        return splitter_dict

    def __call__(self, inputs: List[DataSetObject]) -> SplitterDict:
        return self.split_input_list(inputs)


class RandomSplitter(Splitter):
    def __init__(self, percentage_dict: Dict[SubSetName, float]):
        super().__init__()
        self.percentage_dict = percentage_dict

    def split_input_list(self, inputs: List[DataSetObject]) -> SplitterDict:
        return random_split(inputs, self.percentage_dict)


class GroupSplitter(RandomSplitter):
    def __init__(self, percentage_dict: Dict[SubSetName, float], group_extractor: Callable[[DataSetObject], str]):
        super().__init__(percentage_dict)
        self.group_extractor = group_extractor

    def split_input_list(self, ds_objects: List[DataSetObject]) -> SplitterDict:
        object_bins = defaultdict(list)

        for ds_object in ds_objects:
            object_bins[self.group_extractor(ds_object)].append(ds_object)

        bin_counts = [(group, len(group_items)) for group, group_items in object_bins.items()]

        biggest_to_smallest = sorted(bin_counts, key=lambda x: x[1], reverse=True)

        split: Dict[SubSetName, List[DataSetObject]] = {subset: [] for subset in self.percentage_dict.keys()}
        max_capacity = {subset: percentage * len(ds_objects) for subset, percentage in self.percentage_dict.items()}
        subsets = list(self.percentage_dict.keys())
        current_subset_index = 0

        for group, group_count in biggest_to_smallest:
            destination_found = False
            min_subset = subsets[0]
            min_diff = float("inf")
            for subset_offset in range(len(subsets)):

                current_subset = subsets[(current_subset_index + subset_offset) % len(subsets)]
                current_max_capacity = max_capacity[current_subset]
                current_count = len(split[current_subset])
                current_remaining_capacity = current_max_capacity - current_count

                if group_count < current_remaining_capacity:
                    split[current_subset].extend(object_bins[group])
                    destination_found = True
                    break
                else:
                    current_diff = (current_count + group_count) / current_max_capacity

                    if current_diff < min_diff:
                        min_diff = current_diff
                        min_subset = current_subset

            if destination_found:
                continue

            split[min_subset].extend(object_bins[group])

        return split
