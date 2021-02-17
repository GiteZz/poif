from dataclasses import dataclass
from enum import Enum
from typing import Union

from dataclasses_json import dataclass_json

from poif.cli.tools.cli import answer_from_list, simple_input
from poif.config.base import Config
from poif.config.remote.s3 import S3Config


class RemoteType(str, Enum):
    S3 = "S3"


remote_types = {"S3": S3Config}


@dataclass_json
@dataclass
class RemoteConfig(Config):
    remote_type: RemoteType
    data_folder: str
    config: Union["S3Config"]

    @classmethod
    def get_default_name(cls) -> str:
        return "remote_config.json"

    @staticmethod
    def prompt(default_remote: "RemoteConfig" = None) -> "RemoteConfig":
        # Given remote has priority
        if default_remote is None:
            default_remote = RemoteConfig.get_default()

        default_type = "S3"
        if default_remote is not None and default_remote.remote_type is not None:
            default_type = default_remote.remote_type.value

        remote_type = answer_from_list(
            "Remote type?",
            list(remote_types.keys()),
            default=default_type,
        )

        if default_remote is not None and type(default_remote.config) == remote_types[remote_type]:
            config = remote_types[remote_type].prompt(default=default_remote.config)
        else:
            config = remote_types[remote_type].prompt()

        data_folder = simple_input(
            "Data folder on remote?",
            default=None if default_remote is None else default_remote.data_folder,
        )

        return RemoteConfig(remote_type=remote_type, data_folder=data_folder, config=config)
