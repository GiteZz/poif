from pathlib import Path

import pytest

from poif.cli.datasets.tools.interface import (render_template_path,
                                               strip_jinja_extension)
from poif.config import S3Config
from poif.data.packaging.python_package import PythonPackage
from poif.data.versioning.dataset import VersionedDatasetConfig
from poif.tests import get_temp_path


def test_strip_jinja_extension():
    jinja_file = 'test/__init__.py.jinja2'

    without_extension = strip_jinja_extension(jinja_file)

    assert without_extension == 'test/__init__.py'


@pytest.fixture
def dummy_config():
    dummy_s3_config = S3Config(url='', profile='', bucket='')
    dummy_ds_config = VersionedDatasetConfig(dataset_name='dummy',
                                             git_url='',
                                             data_s3=dummy_s3_config,
                                             files=[],
                                             folders=[]
                                             )

    return dummy_ds_config


def test_rendered_path(dummy_config):
    jinja_file = 'test/_dataset_name_/__init__.py.jinja2'

    assert render_template_path(jinja_file, dummy_config) == 'test/dummy/__init__.py'


# TODO a bit more extensive
def test_interface_creation(dummy_config):
    base_dir = get_temp_path()

    package = PythonPackage(base_dir=base_dir, dataset_config=dummy_config)
    package.write()

    assert (base_dir / 'setup.py').exists()
    assert (base_dir / 'datasets' / dummy_config.dataset_name / '__init__.py').exists()