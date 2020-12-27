from abc import ABC, abstractmethod
from typing import Dict, Any

from poif.data.remote.base import Remote
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

    @abstractmethod
    def get_file(self, tag: FileHash) -> Any:
        pass

    @abstractmethod
    def get_file_size(self, tag: FileHash) -> Any:
        pass

    @abstractmethod
    def get_extension(self, tag: FileHash) -> str:
        pass
