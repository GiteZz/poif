from enum import Enum
from typing import Union

from pydantic import AnyUrl

from poif.cli.datasets.tools.cli import answer_from_list, simple_input
from poif.config.base import Config


class RemoteType(str, Enum):
    S3: 'S3'


class RemoteConfig(Config):
    remote_type: RemoteType
    data_folder: str
    config: Union['S3Config']

    @classmethod
    def get_default_name(cls) -> str:
        return 'remote_config.json'

    @staticmethod
    def prompt(default_remote: 'RemoteConfig' = None) -> 'RemoteConfig':
        # Given remote has priority
        if default_remote is None:
            default_remote = RemoteConfig.get_default()

        new_config = RemoteConfig()
        new_config.remote_type = answer_from_list('Remote type?', list(remote_types.keys()), default=None if default_remote is None else default_remote.remote_type)

        if default_remote is not None and isinstance(default_remote.config, remote_types[new_config.remote_type]):
            new_config.config = remote_types[new_config.remote_type].prompt(default=default_remote.config)
        else:
            new_config.config = remote_types[new_config.remote_type].prompt()

        new_config.data_folder = simple_input('Data folder on remote?', default=new_config.data_folder)

        return new_config


class S3Config(Config):
    @classmethod
    def get_default_name(cls) -> str:
        pass

    url: AnyUrl
    profile: str
    bucket: str
    type: str = 'S3'

    @staticmethod
    def prompt(default: 'S3Config'=None) -> 'S3Config':
        default_bucket = None if default is None else default.bucket
        default_url = None if default is None else default.url
        default_profile = None if default is None else default.profile

        bucket = simple_input(
            'S3 bucket',
            default=default_bucket
        )
        url = simple_input(
            'S3 endpoint',
            default=default_url
        )
        profile = simple_input(
            'S3 profile',
            default=default_profile
        )

        return S3Config(url=url, profile=profile, bucket=bucket)


remote_types = {
    RemoteType.S3: S3Config
}