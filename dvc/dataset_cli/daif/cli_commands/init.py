from typing import Dict, List
import pathlib
import daif.tools.config as config_tools
import daif.tools.git as git_tools
from daif.tools import remove_empty_strings, folder_list_to_pathlib
from daif.tools.cli import yes_with_question, simple_input, s3_input
import daif.tools.readme as readme_tools
import yaml
import subprocess
from pathlib import Path


def init_git(dataset_config: config_tools.DatasetConfig):
    # init local git
    subprocess.call(['git', 'init'])
    subprocess.call(['git', 'remote', 'add', 'origin', dataset_config.git_remote_url])


def init_dvc(dataset_config: config_tools.DatasetConfig):
    subprocess.call(['dvc', 'init'])

    for data_folder in folder_list_to_pathlib(dataset_config.data_folders):
        subprocess.call(['dvc', 'add', data_folder])
    subprocess.call(['dvc', 'commit'])
    subprocess.call(['git', 'add', '*.dvc'])
    subprocess.call(['git', 'add', '*.gitignore'])
    subprocess.call(['git', 'add', '.dvc/config'])
    subprocess.call(['dvc', 'remote', 'add', '-d', 's3_storage', f's3://{dataset_config.s3_bucket}/{dataset_config.dataset_name}'])
    subprocess.call(['dvc', 'remote', 'modify', 's3_storage', 'endpointurl', f'{dataset_config.s3_endpoint}'])
    subprocess.call(['dvc', 'remote', 'modify', 's3_storage', 'profile', f'{dataset_config.s3_profile}'])
    subprocess.call(['git', 'commit', '-am', 'Initial dvc commit'])


def ask_for_readme_creation(dataset_config: config_tools.DatasetConfig):
    if not yes_with_question('Create readme?'):
        return

    bucket_suggestion = "datasets-images" if dataset_config.readme_s3_bucket is None else dataset_config.readme_s3_bucket
    readme_bucket = simple_input(
        'S3 bucket for images, this bucket should be publicly available',
        value_when_empty=bucket_suggestion
    )
    dataset_config.readme_s3_bucket = readme_bucket
    dataset_config.save()
    readme_tools.create_readme(dataset_config)


def init_collect_options(config: config_tools.DaifConfig) -> config_tools.DatasetConfig:
    new_dataset_dict = {}

    new_dataset_dict['dataset_name'] = simple_input('Dataset name', use_empy_value=False)

    s3_config = {}
    s3_config['s3_bucket'] = simple_input(
        'S3 bucket',
        value_when_empty=config.current_origin.s3_default_bucket
    )
    s3_config['s3_endpoint'] = simple_input(
        'S3 endpoint',
        value_when_empty=config.current_origin.s3_default_endpoint
    )
    s3_config['s3_profile'] = simple_input(
        'S3 profile',
        value_when_empty=config.current_origin.s3_profile
    )
    new_dataset_dict['dvc_s3'] = config_tools.S3Config(**s3_config)

    data_folders = simple_input('Data folder, if multiple folder are tracked separate by space', value_when_empty='data')
    new_dataset_dict['data_folders'] = remove_empty_strings(data_folders.split(' '))

    if config.current_origin.git_url is not None and yes_with_question('Create git remote?'):
        new_dataset_dict['git_remote_url'] = git_tools.create_repo(config, 'datasets', new_dataset_dict['dataset_name'])
    else:
        new_dataset_dict['git_remote_url]'] = simple_input('Remote git repo')

    return config_tools.DatasetConfig(**new_dataset_dict)


def init(args: List[str]) -> None:
    cwd = pathlib.Path.cwd()
    current_config = config_tools.get_config_content()
    if current_config is None:
        print("Please create or set origin.")
        return
    dataset_config = init_collect_options(current_config)

    init_git(dataset_config)
    init_dvc(dataset_config)
    ask_for_readme_creation(dataset_config)
    save_loc = dataset_config.save()
    subprocess.call(['git', 'add', str(save_loc)])
    # subprocess.call(['git', 'add', 'README.md'])
    subprocess.call(['git', 'commit', '-m', 'Added dataset specific files'])


if __name__ == "__main__":
    init([])