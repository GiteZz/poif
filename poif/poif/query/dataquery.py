from dataclasses import dataclass
from typing import List

from poif.versioning.dataset import RepoVersionedCollection, VersionedCollection


@dataclass
class DataQuery:
    data_cache_url: str = None
    git_url: str = None
    git_commit: str = None
    query_type: int = None
    dataset_type: str = None  # by_regexes, poif, coco, ?
    regexes: List[str] = None

    _data_collection: VersionedCollection = None

    def __post_init__(self):
        if self.data_cache_url is not None and self.git_url is not None and self.git_commit is not None:
            # Http FileOrigin
            raise NotImplementedError
        elif self.git_url is not None and self.git_commit is not None:
            self._data_collection = RepoVersionedCollection(git_url=self.git_url, git_commit=self.git_commit)
        else:
            raise Exception("No valid collection could be constructed")
