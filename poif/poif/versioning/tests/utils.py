import uuid
from pathlib import Path
from typing import List, Tuple

from poif.cli.commands.init import configured_init
from poif.tests.integration.gitlab.tools import create_repo
from poif.tests.integration.setup import setup
from poif.tests.repo import create_data_repo
from poif.utils import FileIterator


def setup_test_package() -> Tuple[Path, str, List[Path]]:
    minio_config, gitlab_config = setup()

    base_dir, repo_config = create_data_repo(minio_config)

    original_files = list(FileIterator(base_dir))  # list() is done to capture the original state

    repo_name = str(uuid.uuid4())
    git_url = create_repo(gitlab_config, repo_name)

    configured_init(base_dir, repo_config, git_url)

    return base_dir, git_url, original_files
