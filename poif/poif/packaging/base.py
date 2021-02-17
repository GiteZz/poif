from abc import ABC, abstractmethod
from pathlib import Path

from poif.config.collection import DataCollectionConfig
from poif.git.file import FileCreatorMixin


class Package(ABC, FileCreatorMixin):
    def __init__(self, base_dir: Path, collection_config: DataCollectionConfig):
        super().__init__()
        self._created_files = []
        self.base_dir = base_dir
        self.collection_config = collection_config

    @abstractmethod
    def get_resource_directory(self) -> Path:
        pass

    @abstractmethod
    def init(self):
        pass
