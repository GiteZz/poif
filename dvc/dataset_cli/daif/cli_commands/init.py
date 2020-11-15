from typing import Dict, List
import pathlib
import daif.tools.config as config_tools
import daif.tools.git as git_tools
from daif.tools import yes_with_question, simple_input, remove_empty_strings
import daif.tools.readme as readme_tools
import yaml
import subprocess
from pathlib import Path


def init_git(config, name):
    # Create remote repo
    # init local git
    cwd = pathlib.Path.cwd()
    subprocess.call(['git', 'init'])
    subprocess.call(['git', 'remote', 'add', 'origin', repo_url])


def init_dvc(config, data_folders, dataset_name):
    subprocess.call(['dvc', 'init'])
    print(data_folders)
    for data_folder in data_folders:
        subprocess.call(['dvc', 'add', data_folder])
    subprocess.call(['dvc', 'commit'])
    subprocess.call(['git', 'add', '*.dvc'])
    subprocess.call(['git', 'add', '*.gitignore'])
    subprocess.call(['git', 'add', '.dvc/config'])
    subprocess.call(['dvc', 'remote', 'add', '-d', 's3_storage', f's3://{config["default_s3_bucket"]}/{dataset_name}'])
    subprocess.call(['dvc', 'remote', 'modify', 's3_storage', 'endpointurl', f'{config["default_s3_endpoint"]}'])
    subprocess.call(['dvc', 'remote', 'modify', 's3_storage', 'profile', f'{config["s3_profile"]}'])
    subprocess.call(['git', 'commit', '-am', 'Initial dvc commit'])


def init_collect_options(config: config_tools.DaifConfig) -> config_tools.DatasetConfig:
    new_dataset_dict = {}

    new_dataset_dict['dataset_name'] = simple_input('Dataset name', use_empy_value=False)

    new_dataset_dict['s3_bucket'] = simple_input(
        'Default S3 bucket',
        value_when_empty=config.current_origin.s3_default_bucket
    )
    new_dataset_dict['s3_endpoint'] = simple_input(
        'Default S3 endpoint',
        value_when_empty=config.current_origin.s3_default_endpoint
    )

    print(f'Data folder(s): [default: data][Multiple folders are separated by spaces]')
    data_folders = simple_input('Data folder, if multiple folder are tracked separate by space', value_when_empty='data')
    new_dataset_dict['data_folders'] = remove_empty_strings(data_folders.split(' '))

    if config.current_origin.git_url is not None and yes_with_question('Create git remote?'):
        new_dataset_dict['git_remote_url'] = git_tools.create_repo(config, 'datasets', new_dataset_dict['dataset_name'])
    else:
        new_dataset_dict['git_remote_url]'] = simple_input('Remote git repo')

    return config_tools.DatasetConfig(**new_dataset_dict)


def create_datasets_config(options):
    datasets_folder = pathlib.Path.cwd() / '.daif'
    datasets_folder.mkdir(exist_ok=True)

    dataset_config_data = {
        'dataset_name': options['dataset_name'],
        'data_folders': [str(folder)[len(str(Path.cwd())):] for folder in options['data_folders']]
    }

    dataset_config_file = datasets_folder / 'config.yml'
    with open(dataset_config_file, 'w') as f:
        yaml.safe_dump(dataset_config_data, f)

    subprocess.call(['git', 'add', str(dataset_config_file)])


# def create_information_files(options):
#     template_directory =
#     information_files = []
#     with open(testing_config_input_file) as f:
#         template = Template(f.read())
#
#     with open(testing_config_output_file, 'w') as f:
#         f.write(template.render(data=spec_dict))


def init(args: List[str]) -> None:
    cwd = pathlib.Path.cwd()
    current_config = config_tools.get_config_content()
    options = init_collect_options(current_config)

    if current_config is None:
        print("Please create or set origin.")
        return

    init_git(current_config, options['dataset_name'])
    init_dvc(current_config, tools.folder_list_to_pathlib(options['data_folders']), options['dataset_name'])
    readme_tools.create_readme(options)
    create_datasets_config(options)
    subprocess.call(['git', 'add', 'README.md'])
    subprocess.call(['git', 'commit', '-m', 'Added dataset specific files'])


if __name__ == "__main__":
    init([])