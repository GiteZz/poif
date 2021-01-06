from abc import abstractmethod

from poif.config import RemoteConfig
from poif.data.datapoint.base import TaggedData


class TaggedRepo:
    @abstractmethod
    def get(self, data: TaggedData) -> bytes:
        pass

    @abstractmethod
    def get_object_size(self, data: TaggedData):
        pass

    @abstractmethod
    def upload(self, data: TaggedData):
        pass


def get_remote_repo_from_config(remote_config: RemoteConfig):
