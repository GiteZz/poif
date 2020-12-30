from dataclasses import dataclass
from pathlib import Path
from typing import List

from git import Repo


@dataclass
class GitRepo:
    base_dir: Path

    repo: Repo = None

    def __post_init__(self):
        self.repo = Repo.init()

    def add_files(self, files: List[Path]):
        for file in files:
            self.repo.index.add(str(file))

    def commit(self, message: str):
        self.repo.index.commit(message)