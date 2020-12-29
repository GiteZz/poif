from abc import ABC, abstractmethod

from poif.typing import FileHash


class TagMixin(ABC):
    _tag: FileHash = None

    @property
    def tag(self):
        if self._tag is None:
            self.set_tag()
        return self._tag

    @abstractmethod
    def set_tag(self):
        pass

    def remote_file_name(self):
        return f'{self._tag[:2]}/{self._tag[2:]}'