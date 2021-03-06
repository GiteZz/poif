from pathlib import Path

from jinja2 import Template

from poif.cli.tools.interface import render_template_path
from poif.config.collection import DataCollectionConfig
from poif.packaging.base import Package
from poif.templates import get_python_package_template_dir
from poif.utils import get_relative_path


class PythonPackage(Package):
    def __init__(self, base_dir: Path, collection_config: DataCollectionConfig):
        print(f"Python package init in {base_dir}")
        super().__init__(base_dir, collection_config)

    def init(self):
        template_path = get_python_package_template_dir()
        for template_file in template_path.rglob("*.jinja2"):
            destination = self.get_template_destination(template_file, template_path)
            self.write_template(template_file, destination)

            self.add_created_file(destination)

    def get_template_destination(self, template_file: Path, template_source: Path):
        relative_file = get_relative_path(template_source, template_file)
        rendered_path = render_template_path(relative_file, self.collection_config)

        destination_file = self.base_dir / rendered_path
        destination_file.parent.mkdir(parents=True, exist_ok=True)

        return destination_file

    def write_template(self, template_loc: Path, destination: Path):
        template = Template(open(template_loc).read())
        rendered_template = template.render(data={"dataset_name": self.collection_config.name})

        with open(destination, "w") as f:
            f.write(rendered_template)

    def get_resource_directory(self):
        resource_dir = self.base_dir / "datasets" / self.collection_config.name / "resources"
        resource_dir.mkdir(exist_ok=True, parents=True)

        return resource_dir
