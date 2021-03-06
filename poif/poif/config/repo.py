from dataclasses import dataclass
from pathlib import Path

from dataclasses_json import dataclass_json

from poif.config.base import Config
from poif.config.collection import DataCollectionConfig
from poif.config.package import PackageConfig
from poif.config.readme import ReadmeConfig
from poif.git.file import FileCreatorMixin
from poif.packaging.base import Package
from poif.utils import get_relative_path


@dataclass_json
@dataclass
class DataRepoConfig(Config, FileCreatorMixin):
    @classmethod
    def get_default_name(cls) -> str:
        return "repo_config.json"

    collection: DataCollectionConfig
    readme: ReadmeConfig
    package: PackageConfig

    @staticmethod
    def prompt():
        collection = DataCollectionConfig.prompt()
        readme = ReadmeConfig.prompt()
        package = PackageConfig.prompt()

        return DataRepoConfig(collection=collection, readme=readme, package=package)

    def write_to_package(self, package: Package):
        resource_dir = package.get_resource_directory()

        write_in_base_dir = [self.package, self.readme]
        write_in_resource_dir = [self.collection]

        # Files that are written in at the top level, used for updating the dataset
        for item in write_in_base_dir:
            new_file = package.base_dir / item.get_default_name()
            item.write(new_file)

            self.add_created_file(new_file)

        for item in write_in_resource_dir:
            new_file = resource_dir / item.get_default_name()
            item.write(new_file)

            self.add_created_file(new_file)

        resource_dir_link = package.base_dir / ".resource_folder"
        with open(resource_dir_link, "w") as f:
            f.write(get_relative_path(base_dir=package.base_dir, file=resource_dir))
        self.add_created_file(resource_dir_link)

    @classmethod
    def read_from_package(cls, base_dir: Path):
        readme_file = base_dir / ReadmeConfig.get_default_name()
        readme_config = ReadmeConfig.read(readme_file)

        package_file = base_dir / PackageConfig.get_default_name()
        package_config = PackageConfig.read(package_file)

        resource_dir_link = base_dir / ".resource_folder"
        with open(resource_dir_link, "r") as f:
            relative_resource_dir = f.read()

        resource_dir = base_dir / relative_resource_dir

        collection_file = resource_dir / DataCollectionConfig.get_default_name()
        collection_config = DataCollectionConfig.read(collection_file)

        return DataRepoConfig(collection=collection_config, readme=readme_config, package=package_config)
