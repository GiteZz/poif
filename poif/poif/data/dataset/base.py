from typing import Any, Dict, List, Union
from abc import ABC, abstractmethod

from poif.data.access.input import Input
from poif.data.datapoint.base import TaggedData
from poif.data.transform.transform import (DataPointSplitter,
                                           DataPointTransformation,
                                           DataSetSplitter, DataSetTransformation,
                                           OutputFilter)

SplitterType = Union[DataPointSplitter, DataSetSplitter]
TransformationType = Union[DataPointTransformation, DataSetTransformation]


class BaseDataset(ABC):
    def create_file_system(self, data_format: str):
        raise NotImplementedError

    @abstractmethod
    def form(self, data: List[TaggedData]):
        pass

    @abstractmethod
    def __len__(self):
        pass

    @abstractmethod
    def __getitem__(self, idx: int):
        pass


class MultiDataset(BaseDataset, ABC):
    def __getattr__(self, item) -> Union[BaseDataset, 'MultiDataset']:
        try:
            if item in self.available_sub_datasets:
                return self.get_sub_dataset(item)
            else:
                raise AttributeError
        except:
            raise AttributeError

    @abstractmethod
    def get_sub_dataset(self, key: str) -> BaseDataset:
        pass

    @property
    @abstractmethod
    def available_sub_datasets(self):
        pass