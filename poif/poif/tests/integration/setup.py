from typing import Tuple

from poif.tests.integration.gitlab.config import GitlabConfig
from poif.tests.integration.gitlab.setup import gitlab_setup
from poif.tests.integration.minio.config import MinioConfig
from poif.tests.integration.minio.setup import minio_setup


def setup() -> Tuple[MinioConfig, GitlabConfig]:
    minio_config = MinioConfig()
    gitlab_config = GitlabConfig()

    minio_setup(minio_config)
    gitlab_setup(gitlab_config)

    return minio_config, gitlab_config
