from abc import ABC, abstractmethod
from dataclasses import dataclass
from pathlib import Path

from poif.project_interface.classes.data_location import DvcDataPoint


@dataclass
class Remote(ABC):
    @abstractmethod
    def download_file(self, file_location: DvcDataPoint, save_path: Path):
        pass

    @abstractmethod
    def get_object_size(self, file_location: DvcDataPoint):
        pass

