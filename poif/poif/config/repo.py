from pathlib import Path

from poif.config.base import Config
from poif.config.collection import DataCollectionConfig
from poif.config.package import PackageConfig
from poif.config.readme import ReadmeConfig
from poif.git.file import FileCreatorMixin
from poif.packaging.base import packages


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

    def write_to_package(self, base_dir: Path):
        resource_dir = packages[self.package.type].get_resource_directory(base_dir=base_dir)

        write_in_base_dir = [self.package, self.readme]
        write_in_config_dir = [self.collection]

        for item in write_in_base_dir:
            new_file = base_dir / item.get_default_name()
            item.write(new_file)

            self.add_created_file(new_file)

        for item in write_in_config_dir:
            new_file = resource_dir / item.get_default_name()
            item.write(new_file)

            self.add_created_file(new_file)

    @classmethod
    def read_from_package(cls, base_dir: Path):
        readme_file = base_dir / ReadmeConfig.get_default_name()
        readme_config = ReadmeConfig.read(readme_file)

        package_file = base_dir / PackageConfig.get_default_name()
        package_config = PackageConfig.read(package_file)

        resource_dir = packages[package_config.type].get_resource_directory(base_dir=base_dir)

        collection_file = resource_dir / DataCollectionConfig.get_default_name()
        collection_config = DataCollectionConfig.read(collection_file)

        return DataRepoConfig(collection=collection_config, readme=readme_config, package=package_config)
