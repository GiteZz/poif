import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

if typing.TYPE_CHECKING:
    from poif.data.access.datapoint import DvcDataPoint


@dataclass
class Remote(ABC):
    @abstractmethod
    def download_file(self, file_location: 'DvcDataPoint', save_path: Path):
        pass

    @abstractmethod
    def get_object_size(self, file_location: 'DvcDataPoint'):
        pass

