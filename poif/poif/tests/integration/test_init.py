import uuid
from pathlib import Path

from poif.config.tests.test_prompts import get_repo_sequence
from poif.tests import MonkeyPatchSequence
from poif.tests.integration.gitlab.tools import create_repo
from poif.tests.integration.setup import setup
from poif.tests.repo import create_data_repo


def test_init(monkeypatch):
    minio_config, gitlab_config = setup()

    base_dir, repo_config = create_data_repo(minio_config)

    repo_name = str(uuid.uuid4())
    git_url = create_repo(gitlab_config, repo_name)

    sequence, config = get_repo_sequence(expected_result=repo_config)
    monkeypatch.setattr("builtins.input", MonkeyPatchSequence(sequence + [git_url]))

    monkeypatch.setattr(Path, "cwd", lambda: base_dir)

    from poif.cli.commands import init

    init([])
