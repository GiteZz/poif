import typing
from abc import abstractmethod

if typing.TYPE_CHECKING:
    from poif.tagged_data.base import TaggedData


class TaggedRepo:
    """
    Class that is used to upload/download tagged data. This class is meant to be subclassed where then a
    reference to a remote can be used to retrieve the files.
    """

    @abstractmethod
    def get_from_tag(self, tag: str):
        pass

    @abstractmethod
    def get_object_size_from_tag(self, tag: str):
        pass

    def get(self, data: "TaggedData") -> bytes:
        return self.get_from_tag(data.tag)

    def get_object_size(self, data: "TaggedData"):
        return self.get_object_size_from_tag(data.tag)

    @abstractmethod
    def upload(self, data: "TaggedData"):
        pass
