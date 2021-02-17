from poif.utils import is_close
from poif.utils.splitting import random_split


def test_random_split():
    objects = list(range(10000))

    split_percentages = {"train": 0.7, "val": 0.15, "test": 0.15}

    split_dict = random_split(objects, split_percentages)

    for ds_type in split_percentages.keys():
        actual_percentage = len(split_dict[ds_type]) / len(objects)
        ideal_percentage = split_percentages[ds_type]

        assert is_close(actual_percentage, ideal_percentage, 0.02)
