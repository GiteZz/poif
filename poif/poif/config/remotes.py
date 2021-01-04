from copy import deepcopy
from dataclasses import dataclass

from poif.cli.datasets.tools.cli import simple_input


@dataclass
class S3Config:
    url: str = None
    profile: str = None
    bucket: str = None

    @staticmethod
    def prompt(default: 'S3Config'=None) -> 'S3Config':
        if default is not None:
            new_config = deepcopy(default)
        else:
            new_config = S3Config()

        new_config.bucket = simple_input(
            'S3 bucket',
            default=new_config.bucket
        )
        new_config.url = simple_input(
            'S3 endpoint',
            default=new_config.url
        )
        new_config.profile = simple_input(
            'S3 profile',
            default=new_config.profile
        )

        return new_config



remote_types = {
    'S3': S3Config
}