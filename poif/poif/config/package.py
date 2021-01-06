from poif.cli.datasets.tools.cli import enum_input
from poif.config.base import Config
from poif.data.packaging.base import PackageOptions


class PackageConfig(Config):
    type: PackageOptions

    @classmethod
    def get_default_name(cls) -> str:
        return 'package_config.json'

    @staticmethod
    def prompt():
        package_type = enum_input("Package type", PackageOptions)

        return PackageConfig(type=package_type)