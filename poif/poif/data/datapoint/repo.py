from poif.data.datapoint.base import TaggedData
from poif.data.repo.base import TaggedRepo


class RepoData(TaggedData):
    repo: TaggedRepo

    @property
    def size(self) -> int:
        return self.repo.get_object_size(self)

    def get(self) -> bytes:
        return self.repo.get(self)