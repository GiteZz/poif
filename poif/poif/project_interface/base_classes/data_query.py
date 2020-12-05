from dataclasses import dataclass, field
from pathlib import Path
import requests

from typing import List, Tuple, Union, Callable, Dict, Any
from poif.project_interface.base_classes.input import MetaInput, DataInput
from poif.project_interface.data_handlers.disk_loader.gather_functions import file_gatherer
from poif.typing import FileHash, RelFilePath
from poif.project_interface.base_classes.location import HttpLocation


DataPointTransformation = Callable[[MetaInput], Union[MetaInput, List[MetaInput]]]


# Used for splitting the dataset, used for train/val/test split
DatasetSplitter = Callable[[List[MetaInput]], Dict[str, List[MetaInput]]]
DataPointFilter = Callable[[MetaInput], str]


@dataclass
class DataQuery:
    data_cache_url: str = None
    git_url: str = None
    git_commit: str = None
    query_type: int = None
    dataset_type: str = None # by_regexes, poif, coco, ?
    regexes: List[str] = None

    dataset_filter: DatasetSplitter = None,
    datapoint_filter: DataPointFilter = None,

    datapoint_transformations: Union[List[DataPointTransformation], DataPointTransformation] = None

    def validate(self):
        if self.dataset_filter is not None and self.datapoint_filter is not None:
            return ValueError('dataset_filter and datapoint_filter can not be both defined.')

    def __post_init__(self):
        if self.data_cache_url[-1] == '/':
            self.data_cache_url = self.data_cache_url[:-1]


def get_dataset(input_query: DataQuery):
    pass

def get_meta_files(input_query: DataQuery) -> List[MetaInput]:
    files = get_files(input_query)

    for file_hash, reLfile_path in files:
        meta_input_list = []

        file_name = Path(reLfile_path).parts[-1]
        rel_file_path = '/'.join(Path(reLfile_path).parts[:-1])

        http_params = {

        }
        remote_loc = HttpLocation(input_query.data_cache_url, )
        meta_input = MetaInput()

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

