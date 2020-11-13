import subprocess
import yaml
import pathlib


def get(args):
    git_url = args[0]
    subprocess.call(['git', 'clone', git_url, 'new_data_folder'])
    with open('./new_data_folder/.datasets/config.yml', 'r') as f:
        dataset_config = yaml.safe_load(f)
    dataset_name = dataset_config['dataset_name']
    subprocess.call(['mv', 'new_data_folder', dataset_name])
    if len(args) > 1:
        commit = args[1]
        subprocess.call(['git', 'checkout', commit])
    subprocess.call(['dvc', 'pull'], cwd=pathlib.Path.cwd() / dataset_name)