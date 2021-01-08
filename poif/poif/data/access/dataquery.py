from collections import defaultdict

from dataclasses import dataclass
from enum import Enum
from typing import List, Union, Dict

from poif.data.access.dataset import SplitterType, TransformationType, Dataset
from poif.data.access.input import Input
from poif.data.access.transform import (DataPointSplitter,
                                        DataPointTransformation,
                                        DataSetSplitter, DataSetTransformation,
                                        OutputFilter)
from poif.data.versioning.dataset import VersionedCollection, RepoVersionedCollection


@dataclass
class DataQuery:
    data_cache_url: str = None
    git_url: str = None
    git_commit: str = None
    query_type: int = None
    dataset_type: str = None # by_regexes, poif, coco, ?
    regexes: List[str] = None

    splitter_list: Union[SplitterType, List[SplitterType]] = None
    transformation_list: Union[TransformationType, List[TransformationType]] = None
    output_filter: OutputFilter = None

    _data_collection: VersionedCollection = None

    def __post_init__(self):
        if self.data_cache_url is not None and self.git_url is not None and self.git_commit is not None:
            # Http FileOrigin
            raise NotImplementedError
        elif self.git_url is not None and self.git_commit is not None:
            self._data_collection = RepoVersionedCollection(git_url=self.git_url, git_commit=self.git_commit)
        else:
            raise Exception('No valid collection could be constructed')

        if self.splitter_list is not None and (
                isinstance(self.splitter_list, DataSetSplitter) or isinstance(self.splitter_list, DataPointSplitter)
        ):
            self.splitter_list = [self.splitter_list]
        elif self.splitter_list is None:
            self.splitter_list = []

        if self.transformation_list is not None and (
                isinstance(self.transformation_list,
                           DataSetTransformation) or
                isinstance(self.transformation_list,
                           DataPointTransformation)
        ):
            self.transformation_list = [self.transformation_list]
        elif self.splitter_list is None:
            self.transformation_list = []

    def to_dataset(self):
        inputs = self.get_inputs()
        inputs = self.transform_inputs(inputs)
        data_splits = self.split_inputs(inputs)

        return Dataset(inputs=inputs, dataset_splits=data_splits, output_filter=self.output_filter)

    def get_inputs(self) -> List[Input]:
        files = self._data_collection.get_files()
        input_list = []
        for file in files:
            meta_data = {
                'rel_file_path': file.relative_path,
                'data': file
            }

            input_list.append(Input(meta_data=meta_data))

        return input_list

    def transform_inputs(self, input_list: List[Input]) -> List[Input]:
        current_list = input_list
        for transformation in self.transformation_list:
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

    def split_inputs(self, input_list: List[Input]) -> Dict[str, List[Input]]:
        list_split_dicts = []
        for splitter in self.splitter_list:
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