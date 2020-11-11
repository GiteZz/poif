from typing import Dict, List
import pathlib
import datasets.config_file as config_file
import datasets.git_tools as git_tools
from datasets.tools import yes
import os
import subprocess


def init_git(config, name):
    # Create remote repo
    # init local git
    repo_url = git_tools.create_repo(config, 'datasets', name)
    cwd = pathlib.Path.cwd()
    subprocess.call(['git', 'init'])
    subprocess.call(['git', 'remote', 'add', 'origin', repo_url])


def init_dvc(config, data_folder, dataset_name):
    subprocess.call(['dvc', 'init'])
    data_folder = pathlib.Path.cwd() / data_folder
    subprocess.call(['dvc', 'add', data_folder])
    subprocess.call(['dvc', 'commit'])
    subprocess.call(['git', 'add', '*.dvc'])
    subprocess.call(['git', 'add', '*.gitignore'])
    subprocess.call(['git', 'add', '.dvc/config'])
    subprocess.call(['dvc', 'remote', 'add', '-d', 's3_storage', f's3://{config["default_s3_bucket"]}/{dataset_name}'])
    subprocess.call(['dvc', 'remote', 'modify', 's3_storage', 'endpointurl', f'{config["default_s3_endpoint"]}'])
    subprocess.call(['dvc', 'remote', 'modify', 's3_storage', 'profile', f'{config["s3_profile"]}'])
    subprocess.call(['git', 'commit', '-am', 'Initial dvc commit'])
    subprocess.call(['git', 'push', '-u', 'origin', 'master'])
    subprocess.call(['dvc', 'push'])


def init_collect_options(config: Dict) -> Dict:
    options = {}

    print(f'Use default S3 information from origin: {config["name"]}?')
    use_s3_default= yes()

    if use_s3_default:
        options['s3_bucket'] = config['default_s3_bucket']
        options['s3_endpoint'] = config['default_s3_endpoint']
    else:
        print("S3 bucket name:")
        options['s3_bucket'] = input()
        print("S3 endpoint url:")
        options['s3_endpoint'] = input()

    print(f'Dataset name:')
    options['dataset_name'] = input()

    print(f'Data folder')
    options['data_folder'] = input()

    return options


def init(args: List[str]) -> None:
    cwd = pathlib.Path.cwd()
    current_config = config_file.get_current_origin()
    options = init_collect_options(current_config)

    if current_config is None:
        print("Please create or set origin.")
        return

    init_git(current_config, options['dataset_name'])
    init_dvc(current_config, options['data_folder'], options['dataset_name'])


if __name__ == "__main__":
    init([])