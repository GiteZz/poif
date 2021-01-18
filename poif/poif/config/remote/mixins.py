from abc import ABC, abstractmethod

from poif.remote.base import FileRemote


class CreateRemoteMixin(ABC):
    @abstractmethod
    def get_configured_remote(self) -> FileRemote:
        pass
