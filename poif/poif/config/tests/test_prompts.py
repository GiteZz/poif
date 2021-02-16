from pathlib import Path

from poif.config.cache import CacheConfig
from poif.config.collection import DataCollectionConfig
from poif.config.package import PackageConfig
from poif.config.readme import ReadmeConfig
from poif.config.remote.base import RemoteConfig, RemoteType
from poif.config.remote.s3 import S3Config
from poif.config.repo import DataRepoConfig
from poif.packaging import PackageOptions
from poif.tests import MonkeyPatchSequence, get_temp_file, get_temp_path


def get_s3_sequence(expected_result: S3Config = None):
    if expected_result is None:
        expected_result = S3Config(bucket="bucket", url="http://url.be", profile="profile")
    sequence = [expected_result.bucket, expected_result.url, expected_result.profile]

    return sequence, expected_result


def get_remote_config_sequence(expected_result: RemoteConfig = None):
    if expected_result is None:
        s3_sequence, s3_config = get_s3_sequence()
        expected_result = RemoteConfig(remote_type=RemoteType.S3, data_folder="data", config=s3_config)
    else:
        s3_sequence, s3_config = get_s3_sequence(expected_result.config)

    remote_config_sequence = [expected_result.remote_type] + s3_sequence + [expected_result.data_folder]
    return remote_config_sequence, expected_result


def bool_to_yes_no(value: bool) -> str:
    if value:
        return "yes"
    else:
        return "no"


def get_readme_sequence(expected_result: ReadmeConfig = None):
    if expected_result is None:
        remote_sequence, remote_config = get_remote_config_sequence()

        expected_result = ReadmeConfig(
            enable=True,
            enable_filetree=True,
            enable_image_gallery=True,
            image_remote=remote_config,
        )
    else:
        remote_sequence, remote_config = get_remote_config_sequence(expected_result.image_remote)

    readme_sequence = [
        bool_to_yes_no(expected_result.enable),
        bool_to_yes_no(expected_result.enable_filetree),
        bool_to_yes_no(expected_result.enable_image_gallery),
    ] + remote_sequence

    return readme_sequence, expected_result


def get_cache_sequence(expected_result: CacheConfig = None):
    if expected_result is None:
        expected_result = CacheConfig(
            enable=True,
            data_storage_location=Path.home(),
            git_storage_location=Path.home(),
            cache_uploads=True,
        )

    sequence = [
        bool_to_yes_no(expected_result.enable),
        str(expected_result.data_storage_location),
        str(expected_result.git_storage_location),
        bool_to_yes_no(expected_result.cache_uploads),
    ]

    return sequence, expected_result


def get_collection_sequence(expected_result: DataCollectionConfig = None):
    if expected_result is None:
        remote_sequence, remote_config = get_remote_config_sequence()
        expected_result = DataCollectionConfig(
            name="name",
            folders=["val", "test"],
            files=["01.jpg"],
            data_remote=remote_config,
        )
    else:
        remote_sequence, remote_config = get_remote_config_sequence(expected_result.data_remote)

    sequence = [expected_result.name] + expected_result.folders + [""] + expected_result.files + [""] + remote_sequence

    return sequence, expected_result


def get_package_sequence(expected_result: PackageConfig = None):
    if expected_result is None:
        expected_result = PackageConfig(type=PackageOptions.python_package)

    sequence = [expected_result.type]

    return sequence, expected_result


def get_repo_sequence(expected_result: DataRepoConfig = None):
    if expected_result is None:
        collection_sequence, collection_config = get_collection_sequence()
        readme_sequence, readme_config = get_readme_sequence()
        package_sequence, package_config = get_package_sequence()
    else:
        collection_sequence, collection_config = get_collection_sequence(expected_result.collection)
        readme_sequence, readme_config = get_readme_sequence(expected_result.readme)
        package_sequence, package_config = get_package_sequence(expected_result.package)

    repo_sequence = collection_sequence + readme_sequence + package_sequence
    repo_config = DataRepoConfig(collection=collection_config, readme=readme_config, package=package_config)

    return repo_sequence, repo_config


def test_s3_prompt(monkeypatch):
    sequence, expected_output = get_s3_sequence()
    monkeypatch.setattr("builtins.input", MonkeyPatchSequence(sequence))
    config1 = S3Config.prompt()

    assert config1 == expected_output


def test_s3_read_write(monkeypatch):
    config_file = get_temp_file()
    _, config = get_s3_sequence()
    config.write(config_file)

    assert config.read(config_file) == config


def test_remote_config_prompt(monkeypatch):
    sequence, expected_output = get_remote_config_sequence()
    monkeypatch.setattr("builtins.input", MonkeyPatchSequence(sequence))
    config1 = RemoteConfig.prompt()

    assert config1 == expected_output


def test_remote_config_read_write(monkeypatch):
    config_file = get_temp_file()
    _, config = get_remote_config_sequence()
    config.write(config_file)

    assert config.read(config_file) == config


def test_readme_prompt(monkeypatch):
    sequence, expected_output = get_readme_sequence()
    monkeypatch.setattr("builtins.input", MonkeyPatchSequence(sequence))
    config1 = ReadmeConfig.prompt()

    assert config1 == expected_output


def test_readme_read_write():
    config_file = get_temp_file()

    _, config = get_readme_sequence()

    config.write(config_file)

    assert config.read(config_file) == config


def test_collection_prompt(monkeypatch):
    sequence, expected_output = get_collection_sequence()
    monkeypatch.setattr("builtins.input", MonkeyPatchSequence(sequence))
    config1 = DataCollectionConfig.prompt()

    assert config1 == expected_output


def test_collection_read_write(monkeypatch):
    config_file = get_temp_file()
    _, config = get_collection_sequence()
    config.write(config_file)

    assert config.read(config_file) == config


def test_cache_prompt(monkeypatch):
    sequence, expected_output = get_cache_sequence()
    monkeypatch.setattr("builtins.input", MonkeyPatchSequence(sequence))
    config1 = CacheConfig.prompt()

    assert config1 == expected_output


def test_cache_read_write(monkeypatch):
    config_file = get_temp_file()
    _, config = get_cache_sequence()
    config.write(config_file)

    assert config.read(config_file) == config


def test_package_prompt(monkeypatch):
    sequence, expected_output = get_package_sequence()
    monkeypatch.setattr("builtins.input", MonkeyPatchSequence(sequence))
    config1 = PackageConfig.prompt()

    assert config1 == expected_output


def test_package_read_write(monkeypatch):
    config_file = get_temp_file()
    _, config = get_package_sequence()
    config.write(config_file)

    assert config.read(config_file) == config


def test_repo_prompt(monkeypatch):
    sequence, expected_output = get_repo_sequence()
    monkeypatch.setattr("builtins.input", MonkeyPatchSequence(sequence))
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
