from typing import Dict, List
import pathlib
import datasets.config_file as config_file
import datasets.git_tools as git_tools
import datasets.tools as tools
import os
import yaml
import subprocess
import jinja2


def init_git(config, name):
    # Create remote repo
    # init local git
    repo_url = git_tools.create_repo(config, 'datasets', name)
    cwd = pathlib.Path.cwd()
    subprocess.call(['git', 'init'])
    subprocess.call(['git', 'remote', 'add', 'origin', repo_url])


def init_dvc(config, data_folders, dataset_name):
    subprocess.call(['dvc', 'init'])
    for data_folder in data_folders:
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
    subprocess.call(['dvc', 'push'])


def init_collect_options(config: Dict) -> Dict:
    options = {}

    print(f'Use default S3 information from origin? [{config["name"]}]?')
    use_s3_default = tools.yes(empy_is_true=True)

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

    print(f'Data folder(s): [default: data][Multiple folders are separated by spaces]')
    data_folders = input()
    if data_folders == "":
        options['data_folders'] = ['data']
    else:
        options['data_folders'] = tools.remove_empty_strings(data_folders)

    return options

def create_datasets_config(options):
    datasets_folder = pathlib.Path.cwd() / '.datasets'
    datasets_folder.mkdir(exist_ok=True)

    dataset_config_data = {
        'dataset_name': options['dataset_name'],
        'data_folders': options['data_folders']
    }

    dataset_config = datasets_folder / 'config.yml'
    with open(dataset_config, 'w') as f:
        yaml.safe_dump(dataset_config_data, f)


def create_information_files(options):
    template_directory =
    information_files = []
    with open(testing_config_input_file) as f:
        template = Template(f.read())

    with open(testing_config_output_file, 'w') as f:
        f.write(template.render(data=spec_dict))


def init(args: List[str]) -> None:
    cwd = pathlib.Path.cwd()
    current_config = config_file.get_current_origin()
    options = init_collect_options(current_config)

    if current_config is None:
        print("Please create or set origin.")
        return

    init_git(current_config, options['dataset_name'])
    init_dvc(current_config, options['data_folders'], options['dataset_name'])


    subprocess.call(['git', 'add', 'dataset_config.yml'])
    subprocess.call(['git', 'commit', '-m', 'Added dataset configuration file'])
    subprocess.call(['git', 'push', '-u', 'origin', 'master'])


if __name__ == "__main__":
    init([])