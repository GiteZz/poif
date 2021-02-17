import itertools
import random
from collections import defaultdict

from poif.dataset.object.split.base import GroupSplitter
from poif.dataset.object.tests.mock import MockDataSetObject
from poif.utils import is_close


def test_group_splitter():
    ds_objects = []
    for group_index in range(100):
        group_count = random.randint(50, 150)

        for within_group_index in range(group_count):
            ds_objects.append(MockDataSetObject(f"vid_{group_index}_{within_group_index}.jpg", group_index))

    percentage_dict = {"train": 0.7, "val": 0.15, "test": 0.15}
    splitter = GroupSplitter(
        percentage_dict=percentage_dict, group_extractor=lambda ds_object: ds_object.relative_path.split("_")[1]
    )

    split_dict = splitter(ds_objects)

    group_types_per_subset = defaultdict(set)

    for ds_type in percentage_dict.keys():
        actual_percentage = len(split_dict[ds_type]) / len(ds_objects)
        ideal_percentage = percentage_dict[ds_type]

        assert is_close(actual_percentage, ideal_percentage, 0.02)

        for ds_object in split_dict[ds_type]:
            group_types_per_subset[ds_type].add(ds_object.get_parsed())

    for groups_in_subset1, groups_in_subset2 in itertools.permutations(group_types_per_subset.values(), r=2):
        assert len(set.intersection(groups_in_subset1, groups_in_subset2)) == 0
