import subprocess
from pathlib import Path
from typing import List

from poif.cli.datasets.tools import (folder_list_to_pathlib,
                                     remove_empty_strings)
from poif.cli.datasets.tools.cli import (multi_input, s3_input, simple_input,
                                         yes_with_question)
from poif.cli.datasets.tools.config import DefaultConfig, get_default_config
from poif.cli.datasets.tools.interface import PythonPackage
from poif.data.remote.s3 import S3Remote
from poif.data.versioning.dataset import (VersionedDataset,
                                          VersionedDatasetConfig)
from poif.utils.git import GitRepo
from poif.utils.readme import DatasetReadme, ReadmeSection



def init_collect_options(config: DefaultConfig) -> VersionedDatasetConfig:
    dataset_name = simple_input('Dataset name', use_empy_value=False)

    folders = multi_input('Data folders', empty_allowed=True)
    files = multi_input('Individual files', empty_allowed=True)

    git_url = simple_input('Remote git repo')

    print('S3 bucket configuration for uploading data')
    data_s3 = s3_input(default_config=config.data_s3)

    if yes_with_question('Add images to readme? Files are displayed via http accessible S3 bucket.'):
        print('S3 bucket configuration for uploading data')
        readme_s3 = s3_input(default_config=config.readme_s3)
    else:
        readme_s3 = None

    return VersionedDatasetConfig(dataset_name=dataset_name,
                                  folders=folders,
                                  files=files,
                                  git_url=git_url,
                                  data_s3=data_s3,
                                  readme_s3=readme_s3)


def init(args: List[str]) -> None:
    default_config = get_default_config()

    dataset_config = init_collect_options(default_config)
    config_file = Path.cwd() / 'dataset_config.json'
    dataset_config.write(config_file)

    versioned_dataset = VersionedDataset(base_dir=Path.cwd(), config=dataset_config)

    package = PythonPackage(base_dir=Path.cwd(), dataset_config=dataset_config)
    package.write()

    resource_dir = package.get_resource_dir()
    versioned_dataset.write_versioning_files(resource_dir)

    cache_dir = Path.cwd() / '.cache'
    cache_dir.mkdir(exist_ok=True)
    versioned_dataset.write_mappings(cache_dir)

    # remote = S3Remote(dataset_config.data_s3)
    # versioned_dataset.upload(remote)

    readme_file = Path.cwd() / 'README.md'
    readme = DatasetReadme(Path.cwd(), config=dataset_config)
    readme.write_to_file(readme_file)

    git_repo = GitRepo(base_dir=Path.cwd(), init=True)
    git_repo.add_files(package.get_created_files())
    git_repo.add_files(versioned_dataset.get_created_files())
    git_repo.add_files([readme_file])
    git_repo.commit('Created dataset')


if __name__ == "__main__":
    template_path = Path(__file__).parents[1] / 'templates' / 'project_interface'
    p1 = list(template_path.glob('**/*.jinja2'))[1]


    print(str(p1)[len(str(template_path)) + 1:])