from pathlib import Path

from poif.config.repo import DataRepoConfig
from poif.git.repo import GitRepo
from poif.repo.file_remote import get_remote_repo_from_config
from poif.utils.readme import DatasetReadme
from poif.versioning.dataset import FromDiskVersionedCollection, ResourceDirCollection


def update(args):
    configured_update(Path.cwd())


def configured_update(base_dir: Path):
    resource_dir_link = base_dir / ".resource_folder"
    with open(resource_dir_link, "r") as f:
        relative_resource_dir = f.read()

    resource_dir = base_dir / relative_resource_dir

    repo_config = DataRepoConfig.read_from_package(base_dir)

    previous_collection = ResourceDirCollection(resource_dir)
    previous_files = previous_collection.get_files()
    tags_on_remote = [file.tag for file in previous_files]

    new_dataset = FromDiskVersionedCollection(base_dir=base_dir, config=repo_config.collection)

    new_dataset.write_versioning_files(resource_dir)

    readme = DatasetReadme(base_dir, config=repo_config.collection)
    readme.write_to_folder(base_dir)

    tagged_repo = get_remote_repo_from_config(repo_config.collection.data_remote)
    tagged_repo.upload_collection(new_dataset, excluded_tags=tags_on_remote)

    git_repo = GitRepo(base_dir=base_dir, init=False)

    git_repo.add_file_creator(repo_config)
    git_repo.add_file_creator(new_dataset)
    git_repo.add_file_creator(readme)
    git_repo.commit("Updated dataset")

    if git_repo.has_remote():
        git_repo.push()
