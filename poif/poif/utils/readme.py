from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional

from poif.data.versioning.dataset import DataCollectionConfig
from poif.utils import has_newline
from poif.utils.filetree import FileTree


class ReadmeSection:
    _title: str = None
    _content: str = None
    _subsections: List['ReadmeSection']

    def __init__(self, title: str, content: Optional[str] = None):
        self._title = title
        self._content = content
        self._subsections = []

    @property
    def title(self):
        return self._title

    @property
    def content(self):
        if self._content is None:
            return ""
        return self._content

    @staticmethod
    def lines_as_code(lines: List[str]) -> str:
        code_block_start = "```\n"

        for line in lines:
            code_block_start += f'{line}\n'

        code_block_start += '```'

        return code_block_start

    def add_section(self, section: 'ReadmeSection'):
        self._subsections.append(section)

    def render(self, level=0):
        rendered_title = self.render_title(level=level)
        rendered_content = self.render_content()
        rendered_subsections = self.render_subsections(level=level + 1)

        return rendered_title + rendered_content + rendered_subsections

    def render_title(self, level=0):
        title_level = '#' * (level + 1)
        return f'{title_level} {self.title}\n'

    def render_content(self):
        if len(self.content) > 0 and not has_newline(self.content):
            return self.content + '\n'

        return self.content

    def render_subsections(self, level):
        combination = ""

        for subsection in self._subsections:
            combination += subsection.render(level)

        return combination

    def write_to_file(self, file: Path):
        rendered = self.render()

        with open(file, 'w') as f:
            f.write(rendered)


class FileTreeSection(ReadmeSection):
    def __init__(self, base_dir: Path):
        title = self.get_title_from_dir(base_dir)
        content = self.get_filetree_content(base_dir)
        super().__init__(title, content)

    def get_title_from_dir(self, base_dir: Path):
        return base_dir.parts[-1]

    def get_filetree_content(self, base_dir: Path):
        tree = FileTree(base_dir=base_dir, limit=2)

        return ReadmeSection.lines_as_code(tree.get_lines())


class ImageGallerySection(ReadmeSection):
    def __init__(self, title: str):
        super().__init__(title)


class DatasetReadme(ReadmeSection):
    config: DataCollectionConfig

    def __init__(self, base_dir: Path, config: DataCollectionConfig):
        self.base_dir = base_dir
        self.config = config
        super().__init__(self.config.collection_name)

        self.add_dataset_sections()

    def add_dataset_sections(self):
        file_trees_section = ReadmeSection(title='Data directories')
        self.add_section(file_trees_section)

        for data_folder in self.config.folders:
            base_dir = self.base_dir / data_folder
            single_file_tree = FileTreeSection(base_dir)
            file_trees_section.add_section(single_file_tree)
