import subprocess
from pathlib import Path
from typing import List

from poif.cli.datasets.tools import (folder_list_to_pathlib,
                                     remove_empty_strings)
from poif.cli.datasets.tools.cli import (multi_input, s3_input, simple_input,
                                         yes_with_question)
from poif.cli.datasets.tools.config import DefaultConfig, get_default_config
from poif.data.versioning.dataset import (VersionedDataset,
                                          VersionedDatasetConfig)


def init_git(dataset_config: VersionedDatasetConfig):
    # init disk git
    subprocess.call(['git', 'init'])
    subprocess.call(['git', 'disk_over_http', 'add', 'origin', dataset_config.git_remote_url])


def init_dvc(dataset_config: VersionedDatasetConfig):
    subprocess.call(['dvc', 'init'])

    for data_folder in folder_list_to_pathlib(dataset_config.data_folders):
        subprocess.call(['dvc', 'add', data_folder])
    subprocess.call(['dvc', 'commit'])
    subprocess.call(['git', 'add', '*.dvc'])
    subprocess.call(['git', 'add', '*.gitignore'])
    subprocess.call(['git', 'add', '.dvc/config'])
    subprocess.call(['dvc', 'disk_over_http', 'add', '-d', 's3_storage', f's3://{dataset_config.dvc_s3.bucket}/{dataset_config.dataset_name}'])
    subprocess.call(['dvc', 'disk_over_http', 'modify', 's3_storage', 'endpointurl', f'{dataset_config.dvc_s3.endpoint}'])
    subprocess.call(['dvc', 'disk_over_http', 'modify', 's3_storage', 'profile', f'{dataset_config.dvc_s3.profile}'])
    subprocess.call(['git', 'commit', '-am', 'Initial dvc commit'])


def ask_for_readme_creation(dataset_config: VersionedDatasetConfig):
    if not yes_with_question('Create readme?'):
        return
    readme_tools.create_readme(dataset_config, git_add=True, git_commit=False)


def ask_for_interface_creation(dataset_config: VersionedDatasetConfig):
    if not yes_with_question('Do you want to create an project_interface package for the dataset?'):
        return
    interface_tools.create_interface(dataset_config, git_add=True, git_commit=False)


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


def setup_package_structure(base_dir: Path):


def init(args: List[str]) -> None:
    default_config = get_default_config()

    dataset_config = init_collect_options(default_config)

    versioned_dataset = VersionedDataset(base_dir=Path.cwd(), config=dataset_config)

    init_git(dataset_config)
    ask_for_readme_creation(dataset_config)
    save_loc = dataset_config.save()
    subprocess.call(['git', 'add', str(save_loc)])
    # subprocess.call(['git', 'add', 'README.md'])
    subprocess.call(['git', 'commit', '-m', 'Added dataset specific files'])


if __name__ == "__main__":
    template_path = Path(__file__).parents[1] / 'templates' / 'project_interface'
    p1 = list(template_path.glob('**/*.jinja2'))[1]


    print(str(p1)[len(str(template_path)) + 1:])