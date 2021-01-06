from pathlib import Path
from typing import List

from dataclasses import dataclass
from git import Repo

from poif.data.git.file import FileCreatorMixin


@dataclass
class GitRepo:
    base_dir: Path
    init: bool = False
    repo: Repo = None

    def __post_init__(self):
        if self.init:
            self.repo = Repo.init()
        else:
            self.repo = Repo(str(self.base_dir))

    def add_files(self, files: List[Path]):
        for file in files:
            self.repo.index.add(str(file))

    def add_remote(self, remote: str):
        self.repo.create_remote('origin', remote)

    def commit(self, message: str):
        self.repo.index.commit(message)

    def push(self):
        self.repo.remotes.origin.push()

    def add_file_creator(self, creator: FileCreatorMixin):
        self.add_files(creator.get_created_files())
