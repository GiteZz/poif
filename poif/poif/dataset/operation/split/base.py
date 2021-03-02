from collections import defaultdict
from typing import Callable, Dict, List, Optional

from poif.dataset.object.base import DataSetObject
from poif.dataset.operation.base import Operation
from poif.typing import SubSetName
from poif.utils.splitting import random_split

SplitterDict = Dict[SubSetName, List[DataSetObject]]


class Splitter(Operation):
    """
    A Splitter operation is used to split up the dataset into subsets. This is done similarly as in the Transformation
    operation whereby there exist a single and a list function. Here the split_single_input assigns one
    DataSetObject to a subset, while the split_input_list split the entire list into subsets.
    """

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
    """
    Randomly splits into subsets.

    Percentage dict example: {'train': 0.7, 'val': 0.15, 'test": 0.15} means that 70% of the data will be in
    ds.train etc.
    """

    def __init__(self, percentage_dict: Dict[SubSetName, float]):
        super().__init__()
        self.percentage_dict = percentage_dict

    def split_input_list(self, inputs: List[DataSetObject]) -> SplitterDict:
        return random_split(inputs, self.percentage_dict)


class GroupSplitter(RandomSplitter):
    """
    The group Splitter is a splitter that ensures that items of the same group will be in the same subset and not
    split across multiple subsets. For example: person1 will only be in train dataset and not in val or test.

    Percentage dict example: {'train': 0.7, 'val': 0.15, 'test": 0.15} means that 70% of the data will be in
    ds.train etc.

    The group_extractor is function that extracts a subset from a DataSetObject. An example of this is
    lambda ds_object: ds_object.relative_path.split("_")[1] . This examples split the path and takes the
    first item. This is useful if your relative path is vid01_frame01.png and you dont't want to have
    frames from the same video across subsets.
    """

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
