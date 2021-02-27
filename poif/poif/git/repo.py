from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from git import Repo

from poif.git.file import FileCreatorMixin
from poif.tests import get_temp_path


@dataclass
class GitRepo:
    base_dir: Optional[Path] = None
    git_url: Optional[str] = None
    git_commit: Optional[str] = None
    init: Optional[bool] = False
    repo: Repo = field(init=False)

    def __post_init__(self):
        if self.init:
            self.repo = Repo.init(path=str(self.base_dir))
        elif self.git_url is not None:
            self.base_dir = self.get_clone_location()

            if self.git_commit is not None:
                self.repo = Repo.clone_from(self.git_url, str(self.base_dir), no_checkout=True)
                self.repo.git.checkout(self.git_commit)
            else:
                self.repo = Repo.clone_from(self.git_url, str(self.base_dir), no_checkout=False)
        else:
            self.repo = Repo(str(self.base_dir))

    def get_clone_location(self) -> Path:
        return get_temp_path(prefix="git_get_clone_location")

    def add_files(self, files: List[Path]):
        for file in files:
            self.repo.index.add(str(file))

    def add_remote(self, remote: str):
        self.repo.create_remote("origin", remote)

    def commit(self, message: str):
        self.repo.index.commit(message)

    def get_latest_hash(self):
        return self.repo.head.object.hexsha

    def push(self):
        print("pushing")
        self.repo.remotes.origin.push(refspec="master:master")
        print("done pushing")

    def add_file_creator(self, creator: FileCreatorMixin):
        self.add_files(creator.get_created_files())


if __name__ == "__main__":
    repo = GitRepo(git_url="http://localhost:360/root/datasets-991bd55b-2c97-4848-8b44-8387dbaa8295.git")
    a = "a"
