from poif.data.remote.base import FileRemote
from abc import ABC, abstractmethod

class CreateRemoteMixin(ABC):
    @abstractmethod
    def get_configured_remote(self) -> FileRemote:
        pass
