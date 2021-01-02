from abc import ABC, abstractmethod
from typing import Any, Dict

from poif.typing import FileHash, RelFilePath


class Origin(ABC):
    @property
    @abstractmethod
    def dataset_tag(self) -> str:
        pass

    @property
    @abstractmethod
    def origin_tag(self) -> str:
        pass

    @property
    @abstractmethod
    def tag_to_original_file(self) -> Dict[FileHash, RelFilePath]:
        pass
