from dataclasses import dataclass
from pathlib import Path
from typing import List

from poif.utils import InOrderPathIterator, get_file_depth, FileIterator, sorted_files_by_extension, is_more_populated


class FileTreeIterator(InOrderPathIterator):
    limit: int = 2

    def __next__(self):
        if len(self.stack) > 0:
            first_item = self.stack.pop(0)
            if not isinstance(first_item, Path):
                return first_item

            if first_item.is_dir():
                self.add_dir_to_stack(first_item)
            return first_item

        else:
            raise StopIteration

    def select_files_from_directory(self, directory: Path):
        extension_bins = sorted_files_by_extension(directory, limit=self.limit)

        selected_files = []
        for files in extension_bins.values():
            selected_files.extend(files)

        if len(selected_files) == 0:
            return []

        if is_more_populated(directory, len(selected_files)):
            last_file = selected_files[-1]

            selected_files.append(last_file.parent / '...')

        return selected_files


@dataclass
class FileTree:
    base_dir: Path

    def line_iterator(self) -> List[str]:
        lines = [self.base_dir.parts[-1]]
        for file in FileTreeIterator(self.base_dir):
            lines.append('  ' * get_file_depth(self.base_dir, file) + '- ' + file.parts[-1])
        return lines

    def get_all_folders(self) -> List[Path]:
        pass