from typing import List, Union
from abc import ABC, abstractmethod
from pathlib import Path

from poif.tagged_data.base import TaggedData


class BaseDataset(ABC):
    def __init__(self):
        self.inputs = []

    def create_file_system(self, data_format: str, base_folder: Path):
        raise Exception('File system not supported for this dataset')

    @abstractmethod
    def form(self, data: List[TaggedData]):
        pass

    def __len__(self):
        len(self.inputs)

    def __getitem__(self, idx: int):
        return self.inputs[idx].output()


class MultiDataset(BaseDataset, ABC):
    def __init__(self):
        super().__init__()
        self.split_dict = {}

    def __getattr__(self, item) -> Union[BaseDataset, 'MultiDataset']:
        try:
            if item in self.available_sub_datasets:
                return self.get_sub_dataset(item)
            else:
                raise AttributeError
        except:
            raise AttributeError

    def get_sub_dataset(self, key: str) -> BaseDataset:
        return self.create_sub_dataset_from_objects(self.split_dict[key])

    @abstractmethod
    def create_sub_dataset_from_objects(self, new_objects: List):
        pass

    @property
    def available_sub_datasets(self):
        return list(self.split_dict.keys())