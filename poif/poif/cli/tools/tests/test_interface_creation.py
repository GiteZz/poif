import pytest

from poif.cli.tools.interface import render_template_path, strip_jinja_extension
from poif.config.collection import DataCollectionConfig
from poif.config.remote.base import RemoteConfig, RemoteType
from poif.config.remote.s3 import S3Config
from poif.packaging.python_package import PythonPackage
from poif.tests import get_temp_path


def test_strip_jinja_extension():
    jinja_file = "test/__init__.py.jinja2"

    without_extension = strip_jinja_extension(jinja_file)

    assert without_extension == "test/__init__.py"


@pytest.fixture
def dummy_config() -> DataCollectionConfig:
    dummy_s3_config = S3Config(url="", profile="", bucket="")
    dummy_remote_config = RemoteConfig(config=dummy_s3_config, data_folder="data", remote_type=RemoteType.S3)
    dummy_ds_config = DataCollectionConfig(name="dummy", data_remote=dummy_remote_config, files=[], folders=[])

    return dummy_ds_config


def test_rendered_path(dummy_config):
    jinja_file = "test/_dataset_name_/__init__.py.jinja2"

    assert render_template_path(jinja_file, dummy_config) == "test/dummy/__init__.py"


# TODO a bit more extensive
def test_interface_creation(dummy_config):
    base_dir = get_temp_path(prefix="test_interface_creation")

    package = PythonPackage(base_dir=base_dir, collection_config=dummy_config)
    package.init()

    assert (base_dir / "setup.py").exists()
    assert (base_dir / "datasets" / dummy_config.name / "__init__.py").exists()
