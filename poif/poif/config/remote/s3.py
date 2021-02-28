from dataclasses import dataclass
from typing import Set

from dataclasses_json import dataclass_json

from poif.cli.tools.cli import simple_input
from poif.config.base import Config
from poif.config.remote.mixins import CreateRemoteMixin
from poif.remote.s3 import S3Remote


@dataclass_json
@dataclass
class S3Config(Config, CreateRemoteMixin):
    url: str
    profile: str
    bucket: str
    type = "S3"

    def __init__(self, url: str, profile: str, bucket: str):
        super().__init__()

        self.url = url
        self.profile = profile
        self.bucket = bucket
        self.type = "S3"

    @staticmethod
    def prompt(default: "S3Config" = None) -> "S3Config":
        default_bucket = None if default is None else default.bucket
        default_url = None if default is None else default.url
        default_profile = None if default is None else default.profile

        bucket = simple_input("S3 bucket", default=default_bucket)
        url = simple_input("S3 endpoint", default=default_url)
        profile = simple_input("S3 profile", default=default_profile)

        return S3Config(url=url, profile=profile, bucket=bucket)

    @classmethod
    def get_write_exclusions(cls) -> Set[str]:
        base_excludes = super(S3Config, cls).get_write_exclusions()
        base_excludes.add("remote")

        return base_excludes

    def get_configured_remote(self) -> S3Remote:
        return S3Remote(self)

    @classmethod
    def get_default_name(cls) -> str:
        pass
