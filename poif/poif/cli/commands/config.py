from pathlib import Path

from poif.config.repo import DataRepoConfig


def config(args):
    print("S3 bucket configuration for uploading data")
    current_config = DataRepoConfig.read_from_package(Path.cwd())
