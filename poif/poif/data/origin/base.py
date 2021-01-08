from abc import ABC, abstractmethod
from typing import Any, Dict, List

from poif.data.datapoint.base import TaggedData
from poif.typing import FileHash, RelFilePath


class VersioningCollectionOrigin(ABC):
    @abstractmethod
    def get_files(self) -> List[TaggedData]:
        pass

