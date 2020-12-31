from dataclasses import dataclass
from pathlib import Path
from typing import List

from git import Repo


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