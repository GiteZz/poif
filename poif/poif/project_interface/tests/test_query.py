import pytest

from poif.project_interface.base_classes.input import Input
from poif.project_interface.base_classes.location import DataLocation
from poif.project_interface.base_classes.input import Input
import uuid
from collections import defaultdict
from typing import List, Optional, Union

@pytest.fixture
def meta_input_list():
    meta_data_list = [
        {
            'file_name': '00.jpg',
            'rel_file_path': 'train/img_rgb'
        },
        {
            'file_name': '00.jpg',
            'rel_file_path': 'train/img_bw'
        },
        {
            'file_name': '00.jpg',
            'rel_file_path': 'train/mask'
        },
        {
            'file_name': '01.jpg',
            'rel_file_path': 'test/img_rgb'
        },
        {
            'file_name': '01.jpg',
            'rel_file_path': 'test/img_bw'
        },
        {
            'file_name': '01.jpg',
            'rel_file_path': 'test/mask'
        }
    ]
    return [
        Input(data_loc=DataLocation(),
              tag=uuid.uuid4().hex,
              meta_data=meta_data
              ) for meta_data in meta_data_list
    ]


def filter_bw_img(meta_input: Input) -> Optional[Union[List[Input], Input]]:
    if 'img_bw' in meta_input.rel_file_path:
        return None
    else:
        return meta_input

def combine_mask_and_img(meta_inputs: List[Input]) -> List[Input]:
    same_set_and_name = defaultdict(list)

    for item in meta_inputs:
        dataset_name = item.rel_file_path.split('/')[0]
        same_set_and_name[(dataset_name, item.file_name)].append(item)

    for key, value in same_set_and_name.items():
        if len(value) != 2:
            print('WARNING: no two meta inputs as expected')
            continue
        new_meta_input =

def test_meta_input_transformation(meta_input_list):
    pass