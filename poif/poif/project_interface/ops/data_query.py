from dataclasses import dataclass, field
from pathlib import Path
import requests
from collections import defaultdict

from typing import List, Tuple, Union, Callable, Dict, Any
from poif.project_interface.classes.input import Input
from poif.project_interface.data_handlers.disk_loader.gather_functions import file_gatherer
from poif.typing import FileHash, RelFilePath
from poif.project_interface.classes.location import HttpLocation
from poif.project_interface.classes.transform import (
    DataPointTransformation,
    DataSetTransformation,
    DataPointSplitter,
    DataSetSplitter,
    OutputFilter
)
from poif.project_interface.classes.data import Dataset, DataQuery


def get_dataset(input_query: DataQuery):
    inputs = get_inputs(input_query)
    inputs = transform_inputs(inputs, input_query)
    data_splits = split_inputs(inputs, input_query)

    return Dataset(inputs=inputs, dataset_splits=data_splits, data_query=input_query)


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


def get_inputs(input_query: DataQuery) -> List[Input]:
    files = get_files(input_query)
    input_list = []
    for file_hash, rel_file_path in files.items():
        meta_data = {
            'file_name': Path(rel_file_path).parts[-1],
            'rel_file_path': '/'.join(Path(rel_file_path).parts[:-1])
        }

        remote_loc = HttpLocation(
            url=f'{input_query.data_cache_url}/datasets/file_content',
            git_commit=input_query.git_commit,
            git_url=input_query.git_url,
            data_tag=file_hash
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
