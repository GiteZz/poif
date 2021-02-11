from pathlib import Path

from poif.cli.tools.cli import path_input, yes_with_question
from poif.config.base import Config


class CacheConfig(Config):
    enable: bool
    data_storage_location: Path = None
    git_storage_location: Path = None
    cache_uploads: bool = None

    @classmethod
    def get_default_name(cls) -> str:
        return "cache_config.json"

    @staticmethod
    def prompt():
        enable = yes_with_question("Enable caching on disk?")
        data_storage = path_input("Data storage location?", default=Path.cwd() / "data_cache" / "data")
        git_storage = path_input(
            "Git storage location? Used to avoid duplicated cloning.",
            default=Path.cwd() / "data_cache" / "git",
        )
        cache_upload = yes_with_question("Cache on upload?", default=True)

        return CacheConfig(
            enable=enable,
            data_storage_location=data_storage,
            git_storage_location=git_storage,
            cache_uploads=cache_upload,
        )
