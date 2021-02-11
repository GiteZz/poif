from pathlib import Path
from typing import List, Tuple

from poif.config.collection import DataCollectionConfig
from poif.config.package import PackageConfig
from poif.config.readme import ReadmeConfig
from poif.config.remote.base import RemoteConfig
from poif.config.repo import DataRepoConfig
from poif.packaging.base import PackageOptions
from poif.tests import get_temp_path, write_image_in_file, write_json_in_file
from poif.tests.integration.minio.config import MinioConfig
from poif.tests.integration.minio.setup import get_repo_remotes_from_config


def create_realistic_folder_structure() -> Tuple[Path, List[str], List[str]]:
    base_dir = get_temp_path()

    files = [f"0{i}.jpg" for i in range(10)]
    base_folders = ["train", "val", "test"]
    sub_folders = ["image", "mask"]

    additional_files = [
        "meta.json",
        "train/train_meta.json",
        "val/val_meta.json",
        "test/test_meta.json",
    ]

    for base_folder in base_folders:
        for sub_folder in sub_folders:
            for file in files:
                file_path = base_dir / base_folder / sub_folder / file
                file_path.parent.mkdir(parents=True, exist_ok=True)
                write_image_in_file(file_path)

    for file in additional_files:
        write_json_in_file(base_dir / file)

    return base_dir, base_folders, additional_files


def create_data_collection(remote: RemoteConfig):
    base_dir, dirs, files = create_realistic_folder_structure()

    return base_dir, DataCollectionConfig(
        name="test", folders=dirs, files=files, data_remote=remote
    )


def create_data_repo(minio_config: MinioConfig) -> Tuple[Path, DataRepoConfig]:
    data_remote, readme_remote = get_repo_remotes_from_config(minio_config)
    readme_config = ReadmeConfig(
        enable=True,
        enable_filetree=True,
        enable_image_gallery=True,
        image_remote=readme_remote,
    )
    base_dir, collection_config = create_data_collection(data_remote)
    package_config = PackageConfig(type=PackageOptions.python_package)

    return base_dir, DataRepoConfig(
        collection=collection_config, readme=readme_config, package=package_config
    )
