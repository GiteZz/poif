from dataclasses import dataclass, field
from pathlib import Path
import requests

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

    filter_list: List[Union[DataPointSplitter, DataSetSplitter]] = field(default_factory=[])
    transformation_list: List[Union[DataPointTransformation, DataSetTransformation]] = field(default_factory=[])

    def __post_init__(self):
        if self.data_cache_url[-1] == '/':
            self.data_cache_url = self.data_cache_url[:-1]


def process_meta_input(meta_input: List[Input], input_query: DataQuery) -> List[Input]:
    current_list = meta_input
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


def get_dataset(input_query: DataQuery):
    meta_files = get_meta_files(input_query)
    meta_files = process_meta_input(meta_files, input_query)


def get_meta_files(input_query: DataQuery) -> List[Input]:
    files = get_files(input_query)
    meta_input_list = []
    for file_hash, rel_file_path in files:


        meta_data = {
            'file_name': Path(rel_file_path).parts[-1],
            'rel_file_path': '/'.join(Path(rel_file_path).parts[:-1])
        }

        remote_loc = HttpLocation(
            input_query.data_cache_url,
            commit=input_query.git_commit,
            data_tag=file_hash,
            git_url=input_query.git_url
        )

        meta_input_list.append(Input(data_loc=remote_loc, meta_data=meta_data, tag=file_hash))

    return meta_input_list


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

