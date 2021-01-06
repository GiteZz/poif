from pathlib import Path
from typing import List

from poif.data.packaging.base import packages
from poif.data.packaging.python_package import PythonPackage
from poif.config.repo import DataRepoConfig
from poif.data.repo.file_remote import get_remote_repo_from_config

from poif.data.versioning.dataset import (VersionedDataset)
from poif.data.git.repo import GitRepo
from poif.utils.readme import DatasetReadme, ReadmeSection


def init(args: List[str]) -> None:
    repo_config = DataRepoConfig.prompt()
    resource_dir = packages[repo_config.package.type].get_resource_directory(base_dir=Path.cwd())
    repo_config.write_to_package(base_dir=Path.cwd())

    versioned_dataset = VersionedDataset(base_dir=Path.cwd(), config=repo_config)

    package = PythonPackage(base_dir=Path.cwd(), collection_config=repo_config.collection)
    package.init()

    versioned_dataset.write_versioning_files(resource_dir)

    readme = DatasetReadme(Path.cwd(), config=repo_config)
    readme.write_to_folder(Path.cwd())

    tagged_repo = get_remote_repo_from_config(repo_config.collection.data_remote)
    versioned_dataset.upload(tagged_repo)

    git_repo = GitRepo(base_dir=Path.cwd(), init=True)
    git_repo.add_file_creator(package)
    git_repo.add_file_creator(versioned_dataset)
    git_repo.add_file_creator(readme)
    git_repo.commit('Created dataset')
    git_repo.push()


if __name__ == "__main__":
    init([])