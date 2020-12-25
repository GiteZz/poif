from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Dict, List, Tuple, Union

import requests

from poif.project_interface.classes.input import Input
from poif.project_interface.classes.location import HttpLocation
from poif.project_interface.classes.transform import (DataPointSplitter,
                                                      DataPointTransformation,
                                                      DataSetSplitter,
                                                      DataSetTransformation,
                                                      OutputFilter)
from poif.project_interface.data_handlers.disk_loader.gather_functions import \
    file_gatherer
from poif.typing import FileHash, RelFilePath

SplitterType = Union[DataPointSplitter, DataSetSplitter]
TransformationType = Union[DataPointTransformation, DataSetTransformation]


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

    def __post_init__(self):
        if self.data_cache_url is not None and self.data_cache_url[-1] == '/':
            self.data_cache_url = self.data_cache_url[:-1]

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


class BaseDataset:
    def __init__(self,
                 inputs: List[Input],
                 output_filter: OutputFilter = None):

        self.inputs = inputs
        self.output_filter = output_filter

    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, idx) -> Any:
        input_item = self.inputs[idx]

        if self.output_filter is not None:
            return self.output_filter(input_item)
        else:
            return input_item


class Dataset(BaseDataset):
    def __init__(self,
                 inputs: List[Input],
                 data_query: DataQuery,
                 dataset_splits: Dict[str, List[Input]] = None
                 ):

        # Make sure self.metadata_processors is always a list.
        super().__init__(inputs, data_query.output_filter)
        self.data_query = data_query
        self.dataset_splits = dataset_splits

    def __getattr__(self, item):
        try:
            if item in self.dataset_splits:
                return BaseDataset(self.dataset_splits[item], output_filter=self.data_query.output_filter)
            else:
                raise AttributeError()
        except:
            raise AttributeError()