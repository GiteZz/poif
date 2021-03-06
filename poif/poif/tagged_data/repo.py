from poif.repo.base import TaggedRepo
from poif.tagged_data.base import TaggedData
from poif.typing import FileHash


class RepoData(TaggedData):
    def __init__(self, relative_path: str, repo: TaggedRepo, tag: FileHash = None):
        super().__init__(relative_path, tag=tag)
        self.repo = repo

    @property
    def size(self) -> int:
        return self.repo.get_object_size(self)

    def get(self) -> bytes:
        return self.repo.get(self)
