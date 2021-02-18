import uuid
from pathlib import Path

from poif.config.tests.test_prompts import get_repo_sequence
from poif.git.repo import GitRepo
from poif.tests import MonkeyPatchSequence
from poif.tests.integration.gitlab.tools import create_repo
from poif.tests.integration.setup import setup
from poif.tests.repo import create_data_repo
from poif.utils import get_relative_path, FileIterator
from poif.versioning.dataset import RepoVersionedCollection
from poif.cli.commands.init import init


def test_init(monkeypatch):
    minio_config, gitlab_config = setup()

    base_dir, repo_config = create_data_repo(minio_config)
    original_files = list(FileIterator(base_dir))  # List is done to capture the original state

    repo_name = str(uuid.uuid4())
    git_url = create_repo(gitlab_config, repo_name)

    sequence, config = get_repo_sequence(expected_result=repo_config)
    monkeypatch.setattr("builtins.input", MonkeyPatchSequence(sequence + [git_url]))

    print(base_dir)
    init([str(base_dir)])

    repo = GitRepo(base_dir=base_dir, init=False)
    latest_commit = repo.get_latest_hash()

    file_collection = RepoVersionedCollection(git_url=git_url, git_commit=latest_commit)
    repo_tagged_files = file_collection.get_files()

    repo_relative_path_mapping = {
        tagged_data.relative_path: tagged_data for tagged_data in repo_tagged_files
    }
    assert len(original_files) > 0
    for original_file in original_files:
        original_relative_path = get_relative_path(base_dir=base_dir, file=original_file)
        linked_tagged_data = repo_relative_path_mapping[original_relative_path]

        with open(original_file, 'rb') as f:
            on_disk_bytes = f.read()

        assert on_disk_bytes == linked_tagged_data.get()
