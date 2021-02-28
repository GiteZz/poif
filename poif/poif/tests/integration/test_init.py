from poif.git.repo import GitRepo
from poif.utils import get_relative_path
from poif.versioning.dataset import GitRepoCollection
from poif.versioning.tests.utils import setup_test_package


def test_init():
    base_dir, git_url, original_files = setup_test_package()

    repo = GitRepo(base_dir=base_dir, init=False)
    latest_commit = repo.get_latest_hash()

    file_collection = GitRepoCollection(git_url=git_url, git_commit=latest_commit)
    repo_tagged_files = file_collection.get_files()

    repo_relative_path_mapping = {tagged_data.relative_path: tagged_data for tagged_data in repo_tagged_files}
    assert len(original_files) > 0
    for original_file in original_files:
        original_relative_path = get_relative_path(base_dir=base_dir, file=original_file)
        linked_tagged_data = repo_relative_path_mapping[original_relative_path]

        with open(original_file, "rb") as f:
            on_disk_bytes = f.read()

        assert on_disk_bytes == linked_tagged_data.get()
