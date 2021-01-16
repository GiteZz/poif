import uuid
from collections import defaultdict
from typing import List, Optional, Union

import pytest

from poif.data.access.dataquery import DataQuery
from poif.data.access.input import Input
from poif.data.transform.base import (DataPointSplitter,
                                      DataPointTransformation,
                                      DataSetTransformation)
from poif.data.datapoint.base import StringLocation
from poif.project_interface.ops.data_query import (split_inputs,
                                                   transform_inputs)


@pytest.fixture
def meta_input_list():
    meta_data_list = [
        {
            'file_name': '00.jpg',
            'relative_path': 'train/img_rgb'
        },
        {
            'file_name': '00.jpg',
            'relative_path': 'train/img_bw'
        },
        {
            'file_name': '00.jpg',
            'relative_path': 'train/mask'
        },
        {
            'file_name': '01.jpg',
            'relative_path': 'test/img_rgb'
        },
        {
            'file_name': '01.jpg',
            'relative_path': 'test/img_bw'
        },
        {
            'file_name': '01.jpg',
            'relative_path': 'test/mask'
        }
    ]
    return [Input(
        meta_data=meta_data,
        data_locations=StringLocation(
            data_tag=uuid.uuid4().hex,
            data_str=meta_data['rel_file_path'] + meta_data['file_name']))
        for meta_data in meta_data_list
    ]


def filter_bw_img(meta_input: Input) -> Optional[Union[List[Input], Input]]:
    if 'img_bw' in meta_input.rel_file_path:
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
        if 'mask' in input_list[0].relative_path:
            new_input.data.mask = input_list[0].data
            new_input.data.img = input_list[1].data
        else:
            new_input.data.mask = input_list[1].data
            new_input.data.img = input_list[0].data

        new_input_list.append(new_input)
    return new_input_list


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
