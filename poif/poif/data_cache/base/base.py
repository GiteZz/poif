from abc import ABC, abstractmethod
from typing import Dict, Any

from poif.data_cache.base.mixins import ParseMixin
from poif.project_interface.classes.location import DvcOrigin, DvcDataPoint
from poif.typing import FileHash, RelFilePath


class DvcCache(ABC, ParseMixin):
    @abstractmethod
    def get_files(self, dvc_origin: DvcOrigin) -> Dict[FileHash, RelFilePath]:
        pass

    @abstractmethod
    def get_file(self, dvc_datapoint: DvcDataPoint) -> Any:
        pass


class SingleRepoCache(ParseMixin):
    def __init__(self, dvc_origin: DvcOrigin, base_cache: DvcCache):
        self.dvc_origin = dvc_origin
        self.base_cache = base_cache

    def get_files(self) -> Dict[FileHash, RelFilePath]:
        return self.base_cache.get_files(self.dvc_origin)

    def get_file(self, data_tag: FileHash):
        return self.base_cache.get_file(DvcDataPoint(data_tag=data_tag,
                                                     git_url=self.dvc_origin.git_url,
                                                     git_commit=self.dvc_origin.git_commit)
                                        )