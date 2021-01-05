from pathlib import Path
from typing import List

from poif.cli.datasets.tools.interface import PythonPackage
from poif.config import DataRepoConfig
from poif.data.versioning.dataset import (VersionedDataset)
from poif.utils.git import GitRepo
from poif.utils.readme import DatasetReadme, ReadmeSection


def init(args: List[str]) -> None:
    dataset_config = DataRepoConfig.prompt()
    config_file = Path.cwd() / 'dataset_config.json'
    dataset_config.write(config_file)

    versioned_dataset = VersionedDataset(base_dir=Path.cwd(), config=dataset_config)

    package = PythonPackage(base_dir=Path.cwd(), dataset_config=dataset_config)
    package.write()

    resource_dir = package.get_resource_dir()
    versioned_dataset.write_versioning_files(resource_dir)

    cache_dir = Path.cwd() / '.cache'
    cache_dir.mkdir(exist_ok=True)
    versioned_dataset.write_mappings(cache_dir)

    # remote = S3Remote(dataset_config.data_s3)
    # versioned_dataset.upload(remote)

    readme_file = Path.cwd() / 'README.md'
    readme = DatasetReadme(Path.cwd(), config=dataset_config)
    readme.write_to_file(readme_file)

    git_repo = GitRepo(base_dir=Path.cwd(), init=True)
    git_repo.add_files(package.get_created_files())
    git_repo.add_files(versioned_dataset.get_created_files())
    git_repo.add_files([readme_file])
    git_repo.commit('Created dataset')


if __name__ == "__main__":
    init([])