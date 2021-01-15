from abc import ABC, abstractmethod
from typing import List

from poif.data.access.dataset import Dataset
from poif.data.datapoint.base import TaggedData


class DatasetTemplate(ABC):
    @abstractmethod
    def complete(self, inputs: List[TaggedData]) -> Dataset:
        pass

    def create_file_system(self):
        # This should not be an abstractmethod since not every template can be converted to a filesystem
        raise NotImplementedError
