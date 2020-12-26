from dataclasses import dataclass
from typing import List, Union

from poif.data.access.dataset import SplitterType, TransformationType
from poif.data.access.transform import (DataPointSplitter,
                                        DataPointTransformation,
                                        DataSetSplitter, DataSetTransformation,
                                        OutputFilter)


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