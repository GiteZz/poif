from pathlib import Path
import jinja2
from daif.tools.config import DatasetConfig
import daif.tools.readme as readme_tools
import daif.tools.interface as interface_tools
from daif.tools.cli import yes_with_question, simple_input, s3_input
import subprocess


def create(args):
    create_options = {'readme': create_readme, 'interface': create_interface}
    dataset_config = DatasetConfig.load()
    if dataset_config is None:
        print("Dataset config is not valid")
        return
    create_options[args[0]](dataset_config)


def create_readme(dataset_config: DatasetConfig):
    readme_tools.create_readme(dataset_config, git_add=True, git_commit=True)


def create_interface(dataset_config: DatasetConfig):
    interface_tools.create_interface(dataset_config, git_add=True, git_commit=True)