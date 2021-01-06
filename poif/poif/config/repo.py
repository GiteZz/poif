from pathlib import Path

from poif.config.base import Config
from poif.config.collection import DataCollectionConfig
from poif.config.readme import ReadmeConfig
from poif.config.package import PackageConfig


class DataRepoConfig(Config):
    @classmethod
    def get_default_name(cls) -> str:
        return 'repo_config.json'

    collection: DataCollectionConfig
    readme: ReadmeConfig
    package: PackageConfig

    @staticmethod
    def prompt():
        collection = DataCollectionConfig.prompt()
        readme = ReadmeConfig.prompt()
        package = PackageConfig.prompt()

        return DataRepoConfig(collection=collection, readme=readme, python_package=package)

    def write_to_package(self, base_dir: Path, config_dir: Path):

        write_in_base_dir = [self.package, self.readme]
        write_in_config_dir = [self.collection]

        for item in write_in_base_dir:
            item.write(base_dir / item.get_default_name())

        for item in write_in_config_dir:
            item.write(config_dir / item.get_default_name())