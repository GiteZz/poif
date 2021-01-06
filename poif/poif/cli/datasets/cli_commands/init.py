from pathlib import Path
from typing import List

from poif.data.packaging.base import packages
from poif.data.packaging.python_package import PythonPackage
from poif.config.repo import DataRepoConfig
from poif.data.versioning.dataset import (VersionedDataset)
from poif.data.git.repo import GitRepo
from poif.utils.readme import DatasetReadme, ReadmeSection


def init(args: List[str]) -> None:
    repo_config = DataRepoConfig.prompt()
    config_dir = packages[repo_config.package.type].get_resource_directory(base_dir=Path.cwd())
    repo_config.write_to_package(base_dir=Path.cwd(), config_dir=config_dir)

    versioned_dataset = VersionedDataset(base_dir=Path.cwd(), config=repo_config)

    package = PythonPackage(base_dir=Path.cwd(), collection_config=repo_config.collection)
    package.init()

    resource_dir = package.get_resource_directory(Path.cwd())
    versioned_dataset.write_versioning_files(resource_dir)

    readme = DatasetReadme(Path.cwd(), config=repo_config)
    readme.write_to_folder(Path.cwd())

    git_repo = GitRepo(base_dir=Path.cwd(), init=True)
    git_repo.add_file_creator(package)
    git_repo.add_file_creator(versioned_dataset)
    git_repo.add_file_creator(readme)
    git_repo.commit('Created dataset')


if __name__ == "__main__":
    init([])