import poif.cli.datasets.tools.interface as interface_tools
import poif.cli.datasets.tools.readme as readme_tools
from poif.cli.datasets.tools.config import DatasetConfig


def create(args):
    create_options = {'readme': create_readme, 'project_interface': create_interface}
    dataset_config = DatasetConfig.load()
    if dataset_config is None:
        print("Dataset config is not valid")
        return
    create_options[args[0]](dataset_config)


def create_readme(dataset_config: DatasetConfig):
    readme_tools.create_readme(dataset_config, git_add=True, git_commit=True)


def create_interface(dataset_config: DatasetConfig):
    interface_tools.create_interface(dataset_config, git_add=True, git_commit=True)