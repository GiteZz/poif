from typing import Tuple

from poif.config.remote.base import RemoteConfig, RemoteType
from poif.config.remote.s3 import S3Config
from poif.remote.s3 import S3Remote
from poif.tests.integration.docker import docker_run
from poif.tests.integration.gitlab.wait import wait_on_url
from poif.tests.integration.minio.config import MinioConfig
from poif.tests.integration.minio.start import create_buckets, set_public


def minio_setup(config: MinioConfig):
    docker_run(config.get_docker_config())

    wait_on_url(config.get_docker_config().readiness_url)

    create_buckets(config, [config.data_bucket, config.readme_bucket])
    set_public(config, [config.readme_bucket])


def get_repo_remotes_from_config(config: MinioConfig) -> Tuple[RemoteConfig, RemoteConfig]:
    data_config = S3Config(url=f'http://localhost:{config.port}', bucket='datasets', profile='datasets')
    readme_config = S3Config(url=f'http://localhost:{config.port}', bucket='readme-images', profile='datasets')

    data_remote = RemoteConfig(remote_type=RemoteType.S3, data_folder='data', config=data_config)
    readme_remote = RemoteConfig(remote_type=RemoteType.S3, data_folder='data', config=readme_config)

    return data_remote, readme_remote


def get_remote_from_config(config: MinioConfig) -> S3Remote:
    data_config = S3Config(url=f'http://localhost:{config.port}', bucket='datasets', profile='datasets')

    return data_config.get_configured_remote()


if __name__ == "__main__":
    config = MinioConfig()
    minio_setup(config)