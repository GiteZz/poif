from pathlib import Path

from poif.config.cache import CacheConfig
from poif.config.collection import DataCollectionConfig
from poif.config.package import PackageConfig
from poif.config.readme import ReadmeConfig
from poif.config.remote.base import RemoteConfig, RemoteType
from poif.config.remote.s3 import S3Config
from poif.config.repo import DataRepoConfig
from poif.data.packaging.base import PackageOptions
from poif.tests import MonkeyPatchSequence, get_temp_file, get_temp_path


def get_s3_sequence():
    expected_results = S3Config(bucket='bucket', url='http://url.be', profile='profile')
    sequence = [expected_results.bucket, expected_results.url, expected_results.profile]

    return sequence, expected_results


def get_remote_config_sequence():
    s3_sequence, s3_config = get_s3_sequence()
    remote_config = RemoteConfig(remote_type=RemoteType.S3, data_folder='data', config=s3_config)

    remote_config_sequence = [remote_config.remote_type] + s3_sequence + [remote_config.data_folder]
    return remote_config_sequence, remote_config


def get_readme_sequence():
    remote_sequence, remote_config = get_remote_config_sequence()

    readme_sequence = ['yes', 'yes', 'yes', ] + remote_sequence
    readme_config = ReadmeConfig(enable=True, enable_filetree=True, enable_image_gallery=True, image_remote=remote_config)

    return readme_sequence, readme_config


def get_cache_sequence():
    config = CacheConfig(enable=True, data_storage_location=Path.home(), git_storage_location=Path.home(), cache_uploads=True)

    sequence = ['y', str(config.data_storage_location), str(config.git_storage_location), 'y']

    return sequence, config


def get_collection_sequence():
    remote_sequence, remote_config = get_remote_config_sequence()
    config = DataCollectionConfig(name='name', folders=['val', 'test'], files=['01.jpg'], data_remote=remote_config)

    sequence = [config.name] + config.folders + [''] + config.files + [''] + remote_sequence

    return sequence, config


def get_package_sequence():
    config = PackageConfig(type=PackageOptions.python_package)
    sequence = ['python_package']

    return sequence, config


def get_repo_sequence():
    collection_sequence, collection_config = get_collection_sequence()
    readme_sequence, readme_config = get_readme_sequence()
    package_sequence, package_config = get_package_sequence()

    repo_sequence = collection_sequence + readme_sequence + package_sequence
    repo_config = DataRepoConfig(collection=collection_config, readme=readme_config, package=package_config)

    return repo_sequence, repo_config


def test_s3_prompt(monkeypatch):
    sequence, expected_output = get_s3_sequence()
    monkeypatch.setattr('builtins.input', MonkeyPatchSequence(sequence))
    config1 = S3Config.prompt()

    assert config1 == expected_output


def test_s3_read_write(monkeypatch):
    config_file = get_temp_file()
    _, config = get_s3_sequence()
    config.write(config_file)

    assert config.read(config_file) == config


def test_remote_config_prompt(monkeypatch):
    sequence, expected_output = get_remote_config_sequence()
    monkeypatch.setattr('builtins.input', MonkeyPatchSequence(sequence))
    config1 = RemoteConfig.prompt()

    assert config1 == expected_output


def test_remote_config_read_write(monkeypatch):
    config_file = get_temp_file()
    _, config = get_remote_config_sequence()
    config.write(config_file)

    assert config.read(config_file) == config


def test_readme_prompt(monkeypatch):
    sequence, expected_output = get_readme_sequence()
    monkeypatch.setattr('builtins.input', MonkeyPatchSequence(sequence))
    config1 = ReadmeConfig.prompt()

    assert config1 == expected_output


def test_readme_read_write():
    config_file = get_temp_file()

    _, config = get_readme_sequence()

    config.write(config_file)

    assert config.read(config_file) == config


def test_collection_prompt(monkeypatch):
    sequence, expected_output = get_collection_sequence()
    monkeypatch.setattr('builtins.input', MonkeyPatchSequence(sequence))
    config1 = DataCollectionConfig.prompt()

    assert config1 == expected_output


def test_collection_read_write(monkeypatch):
    config_file = get_temp_file()
    _, config = get_collection_sequence()
    config.write(config_file)

    assert config.read(config_file) == config


def test_cache_prompt(monkeypatch):
    sequence, expected_output = get_cache_sequence()
    monkeypatch.setattr('builtins.input', MonkeyPatchSequence(sequence))
    config1 = CacheConfig.prompt()

    assert config1 == expected_output


def test_cache_read_write(monkeypatch):
    config_file = get_temp_file()
    _, config = get_cache_sequence()
    config.write(config_file)

    assert config.read(config_file) == config


def test_package_prompt(monkeypatch):
    sequence, expected_output = get_package_sequence()
    monkeypatch.setattr('builtins.input', MonkeyPatchSequence(sequence))
    config1 = PackageConfig.prompt()

    assert config1 == expected_output


def test_package_read_write(monkeypatch):
    config_file = get_temp_file()
    _, config = get_package_sequence()
    config.write(config_file)

    assert config.read(config_file) == config


def test_repo_prompt(monkeypatch):
    sequence, expected_output = get_repo_sequence()
    monkeypatch.setattr('builtins.input', MonkeyPatchSequence(sequence))
    config1 = DataRepoConfig.prompt()

    assert config1 == expected_output


def test_repo_read_write(monkeypatch):
    config_file = get_temp_file()
    _, config = get_repo_sequence()
    config.write(config_file)

    assert config.read(config_file) == config

    temp_dir = get_temp_path()
    config.write_to_package(temp_dir)

    assert DataRepoConfig.read_from_package(temp_dir) == config

