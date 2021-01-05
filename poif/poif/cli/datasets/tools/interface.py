import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import List

from jinja2 import Template

from poif.config import DataCollectionConfig
from poif.templates import get_python_package_template_dir
from poif.utils import get_relative_path


def strip_jinja_extension(file_name: str):
    file_name_without_jinja = file_name[:-7]

    return file_name_without_jinja


def render_template_path(path: str, collection_config: DataCollectionConfig):
    without_jinja = strip_jinja_extension(path)
    adjusted_ds_name = without_jinja.replace('_dataset_name_', collection_config.collection_name)

    return adjusted_ds_name


@dataclass
class PythonPackage:
    base_dir: Path
    dataset_config: DataCollectionConfig

    _created_files: List[Path] = field(default_factory=list)

    def write(self):
        template_path = get_python_package_template_dir()
        for template_file in template_path.rglob('*.jinja2'):
            destination = self.get_template_destination(template_file, template_path)
            self.write_template(template_file, destination)

            self._created_files.append(destination)

    def get_template_destination(self, template_file: Path, template_source: Path):
        relative_file = get_relative_path(template_source, template_file)
        rendered_path = render_template_path(relative_file, self.dataset_config)

        destination_file = self.base_dir / rendered_path
        destination_file.parent.mkdir(parents=True, exist_ok=True)

        return destination_file

    def write_template(self, template_loc: Path, destination: Path):
        template = Template(open(template_loc).read())
        rendered_template = template.render(data={'dataset_name': self.dataset_config.collection_name})

        with open(destination, 'w') as f:
            f.write(rendered_template)

    def get_created_files(self):
        return self._created_files

    def get_resource_dir(self):
        resource_dir = self.base_dir / 'datasets' / 'resources'
        resource_dir.mkdir(exist_ok=True, parents=True)

        return resource_dir

