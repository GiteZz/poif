import typing
from abc import abstractmethod

if typing.TYPE_CHECKING:
    from poif.data.datapoint.base import TaggedData


class TaggedRepo:
    @abstractmethod
    def get_from_tag(self, tag: str):
        pass

    @abstractmethod
    def get_object_size_from_tag(self, tag: str):
        pass

    def get(self, data: 'TaggedData') -> bytes:
        return self.get_from_tag(data.tag)

    def get_object_size(self, data: 'TaggedData'):
        return self.get_object_size_from_tag(data.tag)

    @abstractmethod
    def upload(self, data: 'TaggedData'):
        pass
