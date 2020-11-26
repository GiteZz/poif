from dataclasses import dataclass, field
from pathlib import Path

from typing import List, Tuple, Union, Callable, Dict, Any
from poif.base_classes.input import MetaInput, DataInput
from poif.data_handlers.disk_loader.gather_functions import file_gatherer


DataPointTransformation = Callable[[MetaInput], List[MetaInput]]

MetadataProcessor = Callable[[MetaInput], MetaInput]

# Used for splitting the dataset, used for train/val/test split
DatasetFilter = Callable[[List[MetaInput]], Dict[str, List[MetaInput]]]
DataPointFilter = Callable[[MetaInput], str]

@dataclass
class DataQuery:
    query_type: int
    dataset_type: str # by_regexes, poif, coco, ?
    regexes: List[str] = None
    path: Path = None
    dataset_filer: DatasetFilter = None,
    datapoint_filter: DataPointFilter = None,
    metadata_processors: Union[List[MetadataProcessor], MetadataProcessor] = None

    meta_inputs: List[MetaInput] = field(init=False)
    meta_inputs_split: Dict[str, List[MetaInput]] = field(init=False)

    def get_dataset(self):
        if self.query_type == DataQueryType.FROM_DISK:
            self.create_dataset_from_disk()
        else:
            raise NotImplementedError()

    def create_dataset_from_disk(self):
        if self.dataset_type == DatasetFormat.BY_REGEX:
            meta_inputs = file_gatherer(self.path, self.regexes)

    def parse_meta_inputs(self):
        pass


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

