from poif.transform.base import (
    DataPointSplitter,
    DataPointTransformation,
    OutputFilter
)
from poif.access import Input
from typing import Tuple
import numpy as np


def input_to_ds(ds_item: Input) -> str:
    return ds_item.rel_file_path.split('/')[0]


data_splitter = DataPointSplitter(input_to_ds)


def add_label(ds_item: Input) -> Input:
    ds_item.label = ds_item.rel_file_path.split('/')[1]
    return ds_item


add_label_transformation = DataPointTransformation(add_label)


def filter_output(ds_item: Input) -> Tuple[np.ndarray, str]:
    return ds_item.data.get_parsed(), ds_item.label


output_filter = OutputFilter(filter_output)