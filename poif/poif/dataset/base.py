from abc import ABC, abstractmethod
from pathlib import Path
from typing import Dict, List, Union

from poif.tagged_data.base import TaggedData
from poif.typing import SubSetName
from poif.utils.splitting import random_split


class BaseDataset(ABC):
    def __init__(self):
        self.inputs = []

    def create_file_system(self, data_format: str, base_folder: Path):
        raise Exception("File system not supported for this dataset")

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

    def __getattr__(self, item) -> Union[BaseDataset, "MultiDataset"]:
        if item in self.available_sub_datasets:
            return self.get_sub_dataset(item)
        else:
            raise AttributeError

    def get_sub_dataset(self, key: str) -> BaseDataset:
        return self.create_sub_dataset_from_objects(self.split_dict[key])

    @abstractmethod
    def create_sub_dataset_from_objects(self, new_objects: List):
        pass

    @property
    def available_sub_datasets(self):
        return list(self.split_dict.keys())

    def random_split(self, percentage_dict: Dict[SubSetName, float]):
        self.split_dict = random_split(self.inputs, percentage_dict)
