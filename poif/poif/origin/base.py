from abc import ABC, abstractmethod
from typing import List

from poif.tagged_data.base import TaggedData


class VersioningCollectionOrigin(ABC):
    @abstractmethod
    def get_files(self) -> List[TaggedData]:
        pass

