from typing import Dict, List
import pathlib
import datasets.config_file as config_file
import datasets.git_tools as git_tools
from datasets.tools import yes
import os


def init_git(config, name):
    # Create remote repo
    # init local git
    repo_url = git_tools.create_repo(config, 'datasets', name)
    cwd = pathlib.Path.cwd()
    os.popen(f'git init')
    os.popen(f'git remote add origin {repo_url}')


def init_dvc(config, data_folder, dataset_name):
    os.popen('dvc init')
    data_folder = pathlib.Path.cwd() / data_folder
    os.popen(f'dvc add -R {data_folder}')
    os.popen(f'git add *.dvc')
    os.popen(f'git add *.gitignore')
    os.popen(f'git commit -am "Initial dvc commit"')
    os.popen(f'git push -u origin master')
    os.popen(f'dvc remote add -d s3_storage s3://{config["default_s3_bucket"]}/{dataset_name}')
    os.popen(f'dvc remote modify s3_storage endpointurl {config["default_s3_endpoint"]}')
    os.popen(f'dvc remote modify s3_storage profile {config["s3_profile"]}')
    os.popen(f'dvc push')


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