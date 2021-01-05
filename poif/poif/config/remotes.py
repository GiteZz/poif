from copy import deepcopy
from pydantic import BaseModel, AnyUrl
from enum import Enum

from poif.cli.datasets.tools.cli import simple_input


class S3Config(BaseModel):
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


available_remotes = [S3Config]


remote_types = {
    'S3': S3Config
}