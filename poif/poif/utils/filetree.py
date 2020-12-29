from dataclasses import dataclass
from pathlib import Path
from typing import List

from poif.utils import InOrderPathIterator, get_file_depth


@dataclass
class FileTree:
    base_dir: Path

    def line_iterator(self) -> List[str]:
        lines = [self.base_dir.parts[-1]]
        for file in InOrderPathIterator(self.base_dir, file_per_directory_amount=2):
            lines.append('  ' * get_file_depth(self.base_dir, file) + '- ' + file.parts[-1])
        return lines

    def get_all_folders(self) -> List[Path]:
        pass