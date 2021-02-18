from pathlib import Path
from typing import List

from poif.cli.tools.cli import simple_input
from poif.config.repo import DataRepoConfig
from poif.git.repo import GitRepo
from poif.packaging.python_package import PythonPackage
from poif.repo.file_remote import get_remote_repo_from_config
from poif.utils.readme import DatasetReadme
from poif.versioning.dataset import FromDiskVersionedCollection


def init(args: List[str]) -> None:
    if len(args) == 1:
        base_dir = Path(args[0])
    else:
        base_dir = Path.cwd()
    print(f"init from {base_dir}")
    repo_config = DataRepoConfig.prompt()
    git_remote = simple_input(title="Git remote?")
    if git_remote == "":
        print("No git remote provided, git repo will be created but files will not be pushed to remote.")

    package = PythonPackage(base_dir=base_dir, collection_config=repo_config.collection)
    package.init()

    resource_dir = package.get_resource_directory()
    repo_config.write_to_package(package)

    versioned_dataset = FromDiskVersionedCollection(base_dir=base_dir, config=repo_config.collection)

    versioned_dataset.write_versioning_files(resource_dir)

    readme = DatasetReadme(Path.cwd(), config=repo_config.collection)
    readme.write_to_folder(Path.cwd())

    tagged_repo = get_remote_repo_from_config(repo_config.collection.data_remote)
    tagged_repo.upload_collection(versioned_dataset)

    git_repo = GitRepo(base_dir=base_dir, init=True)

    git_repo.add_file_creator(repo_config)
    git_repo.add_file_creator(package)
    git_repo.add_file_creator(versioned_dataset)
    git_repo.add_file_creator(readme)
    git_repo.commit("Created dataset")

    if git_remote != "":
        git_repo.add_remote(git_remote)
        git_repo.push()


if __name__ == "__main__":
    init([])
