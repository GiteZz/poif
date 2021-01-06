from abc import abstractmethod

import typing


if typing.TYPE_CHECKING:
    from poif.data.datapoint.base import TaggedData


class TaggedRepo:
    @abstractmethod
    def get(self, data: 'TaggedData') -> bytes:
        pass

    @abstractmethod
    def get_object_size(self, data: 'TaggedData'):
        pass

    @abstractmethod
    def upload(self, data: 'TaggedData'):
        pass
