from dataclasses import dataclass
from pathlib import Path
from typing import List

@dataclass
class FileTree:
    base_dir: Path

    def get_printed_tree(self: List[str]):
        pass

    def get_all_folders(self) -> List[Path]:
        pass