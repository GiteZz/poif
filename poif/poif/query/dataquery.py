from dataclasses import dataclass
from typing import List

from poif.input.transform.base import (DataPointSplitter,
                                       DataPointTransformation,
                                       DataSetSplitter, DataSetTransformation)
from poif.versioning.dataset import VersionedCollection, RepoVersionedCollection


@dataclass
class DataQuery:
    data_cache_url: str = None
    git_url: str = None
    git_commit: str = None
    query_type: int = None
    dataset_type: str = None # by_regexes, poif, coco, ?
    regexes: List[str] = None


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

