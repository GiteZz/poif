from typing import Set

from poif.cli.datasets import simple_input
from poif.config.base import Config
from poif.config.remote.mixins import CreateRemoteMixin
from poif.remote.s3 import S3Remote


class S3Config(Config, CreateRemoteMixin):
    @classmethod
    def get_default_name(cls) -> str:
        pass

    url: str
    profile: str
    bucket: str
    type: str = "S3"

    @staticmethod
    def prompt(default: "S3Config" = None) -> "S3Config":
        default_bucket = None if default is None else default.bucket
        default_url = None if default is None else default.url
        default_profile = None if default is None else default.profile

        bucket = simple_input("S3 bucket", default=default_bucket)
        url = simple_input("S3 endpoint", default=default_url)
        profile = simple_input("S3 profile", default=default_profile)

        return S3Config(url=url, profile=profile, bucket=bucket)

    def get_write_exclusions(cls) -> Set[str]:
        base_excludes = super(S3Config, cls).get_write_exclusions()
        base_excludes.add("remote")

        return base_excludes

    def get_configured_remote(self) -> S3Remote:
        return S3Remote(self)
