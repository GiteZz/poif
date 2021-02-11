from enum import Enum

from poif.packaging.python_package import PythonPackage


class PackageOptions(str, Enum):
    python_package = "python_package"


packages = {PackageOptions.python_package: PythonPackage}