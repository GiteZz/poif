from dataclasses import dataclass, field
from pathlib import Path
import requests
from collections import defaultdict

from typing import List, Tuple, Union, Callable, Dict, Any
from poif.project_interface.base_classes.input import Input
from poif.project_interface.data_handlers.disk_loader.gather_functions import file_gatherer
from poif.typing import FileHash, RelFilePath
from poif.project_interface.base_classes.location import HttpLocation
from poif.project_interface.base_classes.transform import (
    DataPointTransformation,
    DataSetTransformation,
    DataPointSplitter,
    DataSetSplitter
)


@dataclass
class DataQuery:
    data_cache_url: str = None
    git_url: str = None
    git_commit: str = None
    query_type: int = None
    dataset_type: str = None # by_regexes, poif, coco, ?
    regexes: List[str] = None

    splitter_list: List[Union[DataPointSplitter, DataSetSplitter]] = None
    transformation_list: List[Union[DataPointTransformation, DataSetTransformation]] = None

    def __post_init__(self):
        if self.data_cache_url is not None and self.data_cache_url[-1] == '/':
            self.data_cache_url = self.data_cache_url[:-1]

        if self.splitter_list is None:
            self.splitter_list = []
        if self.transformation_list is None:
            self.transformation_list = []


def transform_inputs(input_list: List[Input], input_query: DataQuery) -> List[Input]:
    current_list = input_list
    for transformation in input_query.transformation_list:
        if isinstance(transformation, DataPointTransformation):
            new_list = []
            for item in current_list:
                # The transformation can give back None, one or more meta inputs, therefore we have to
                # take different actions based on the format returned.
                new_item = transformation(item)
                if new_item is None:
                    continue
                if isinstance(new_item, list):
                    new_list.extend(new_item)
                else:
                    new_list.append(new_item)
            current_list = new_list

        elif isinstance(transformation, DataSetTransformation):
            current_list = transformation(current_list)
    return current_list


def split_inputs(input_list: List[Input], input_query: DataQuery) -> Dict[str, List[Input]]:
    list_split_dicts = []
    for splitter in input_query.splitter_list:
        if isinstance(splitter, DataPointSplitter):
            splitter_dict = defaultdict(list)
            for input_item in input_list:
                splitter_dict[splitter(input_item)].append(input_item)
            list_split_dicts.append(splitter_dict)
        elif isinstance(splitter, DataSetSplitter):
            list_split_dicts.append(splitter(input_list))


    collect_dicts = defaultdict(set)
    for split_dict in list_split_dicts:
        for key, input_list in split_dict.items():
            collect_dicts[key].update(input_list)

    return {key: list(value) for key, value in collect_dicts.items()}


def get_dataset(input_query: DataQuery):
    meta_files = get_inputs(input_query)
    meta_files = transform_inputs(meta_files, input_query)


def get_inputs(input_query: DataQuery) -> List[Input]:
    files = get_files(input_query)
    input_list = []
    for file_hash, rel_file_path in files:
        meta_data = {
            'file_name': Path(rel_file_path).parts[-1],
            'rel_file_path': '/'.join(Path(rel_file_path).parts[:-1])
        }

        remote_loc = HttpLocation(
            url=input_query.data_cache_url,
            commit=input_query.git_commit,
            git_url=input_query.git_url
        )

        input_list.append(Input(data_locations=remote_loc, meta_data=meta_data))

    return input_list


def get_files(input_query: DataQuery) -> Dict[FileHash, RelFilePath]:
    params = {
        'git_url': input_query.git_url,
        'git_commit': input_query.git_commit
    }
    r = requests.get(f'{input_query.data_cache_url}/datasets/files', params=params)
    return r.json()


class DataQueryType:
    FROM_DISK: 0
    DVC_GIT: 1

class DatasetFormat:
    BY_REGEX: 0
    COCO: 1



"""
Use cases:

from poif import datasets


dogs_vs_cats.get_meta_files()
dogs_vs_cats.train.get_meta_files()
dogs_vs_cats.train[0] -> (data, meta_data)
"""

