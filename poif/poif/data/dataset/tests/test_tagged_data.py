from poif.data.datapoint.base import TaggedData
from typing import Any, List, Dict

from poif.data.dataset.detection.base import DetectionAnnotation, DetectionInput
from poif.data.dataset.tagged_data import TaggedDataBaseDataset
from poif.tests import get_img

import random
import uuid
from collections import defaultdict
from typing import List, Optional, Union

import pytest

from poif.data.access.dataquery import DataQuery
from poif.data.access.input import Input
from poif.data.transform.transform import (DataPointSplitter,
                                           DataPointTransformation,
                                           DataSetTransformation)

class MockTaggedData(TaggedData):
    def __init__(self, relative_path: str, data: Any):
        super().__init__(relative_path)
        self.data = data

    @property
    def size(self) -> int:
        return 0

    def get(self) -> bytes:
        raise NotImplementedError

    def get_parsed(self) -> Any:
        return self.data

def generate_classification_dataset(imgs_per_set=10, amount_categories=5):
    data_points = []
    sub_datasets = ['train', 'val', 'test']
    labels = [f'cat{i}' for i in range(amount_categories)]

    for sub_dataset in sub_datasets:
        for label in labels:
            data_points.extend(
                [MockTaggedData(f'{sub_dataset}/{label}/rgb_{i}.jpg', get_img())
                 for i in range(imgs_per_set)]
            )
            data_points.extend(
                [MockTaggedData(f'{sub_dataset}/{label}/bw_{i}.jpg', get_img())
                 for i in range(imgs_per_set)]
            )

    return data_points


def generate_mask_dataset(imgs_per_set=10, sub_datasets=None):
    if sub_datasets is None:
        sub_datasets = ['train', 'val', 'test']
    data_points = []


    for sub_dataset in sub_datasets:
        data_points.extend([MockTaggedData(f'{sub_dataset}/mask_{i}.jpg', get_img()) for i in range(imgs_per_set)])
        data_points.extend([MockTaggedData(f'{sub_dataset}/image_{i}.jpg', get_img()) for i in range(imgs_per_set)])

    return data_points


def filter_bw_img(meta_input: Input) -> Optional[Union[List[Input], Input]]:
    if 'bw_' in meta_input.rel_file_path:
        return None
    else:
        return meta_input




def combine_mask_and_img(meta_inputs: List[Input]) -> List[Input]:
    same_set_and_name = defaultdict(list)
    new_input_list = []
    for item in meta_inputs:
        dataset_name = item.rel_file_path.split('/')[0]
        same_set_and_name[(dataset_name, item.file_name)].append(item)

    for key, input_list in same_set_and_name.items():
        if len(input_list) != 2:
            print('WARNING: no two meta inputs as expected')
            continue
        new_input = Input({})
        if 'mask' in input_list[0].rel_file_path:
            new_input.data.mask = input_list[0].data
            new_input.data.img = input_list[1].data
        else:
            new_input.data.mask = input_list[1].data
            new_input.data.img = input_list[0].data

        new_input_list.append(new_input)
    return new_input_list


def test_combining_mask_img():
    transformation_list = [
        DataSetTransformation(combine_mask_and_img)
    ]

    data_points = generate_mask_dataset(imgs_per_set=10, sub_datasets = ['train', 'val', 'test'])

    ds = TaggedDataBaseDataset(transformations=transformation_list)
    ds.form(data_points)

    assert len(ds) == 3 * 10





def train_test_split(input_item: Input) -> str:
    return input_item.rel_file_path.split('/')[0]


def test_meta_input_transformation(meta_input_list):
    transformation_list = [
        DataPointTransformation(filter_bw_img),
        DataSetTransformation(combine_mask_and_img)
    ]

    query = DataQuery(
        transformation_list=transformation_list
    )

    new_input_list = transform_inputs(meta_input_list, query)

    assert len(new_input_list) == 2
    assert new_input_list[0].data.mask is not None
    assert new_input_list[1].data.img is not None


def test_splitter(meta_input_list):
    splitter_list = [
        DataPointSplitter(train_test_split)
    ]
    query = DataQuery(
        splitter_list=splitter_list
    )
    splitted_dict = split_inputs(meta_input_list, query)
    assert 'train' in splitted_dict
    assert 'test' in splitted_dict

    assert len(splitted_dict['train']) == 3
    assert len(splitted_dict['test']) == 3

