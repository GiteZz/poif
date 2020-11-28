from poif_data_cache.config import git_mapping, git_folder, data_folder
import hashlib
from pathlib import Path
import subprocess
import yaml
import configparser

DatasetID = str


def init_git(init_folder: Path, git_url: str, commit: str) -> None:
    subprocess.call(['git', 'clone', git_url, str(init_folder)])
    subprocess.call(['git', 'checkout', {commit}], cwd=init_folder)


def get_dvc_files(git_url, commit):
    ds_key = f'{git_url}?c={commit}'
    ds_key = hashlib.md5(ds_key.encode('utf-8')).hexdigest()
    repo_path = git_folder / ds_key
    if not (git_folder / ds_key).exists():
        init_git(repo_path, git_url, commit)

    dvc_files = repo_path.rglob('*.dvc')

def get_dvc_config(repo_url: Path):
    dvc_config_file = repo_url / '.dvc' / 'config'
    parser = configparser.ConfigParser()
    parser.read(dvc_config_file)
    for key in parser.keys():
        if 'remote' in key:
            print(str(list(parser[key].keys())))
    print(list(parser.keys()))
    b = 5

def read_dvc_file(dvc_file: Path):
    new_files = []
    with open(dvc_file, 'r') as f:
        contents = yaml.safe_load(f)

    for file_info in contents['outs']:
        a = 5

if __name__ == "__main__":
    # read_dvc_file(Path('/home/gilles/datasets/pneumonia/test.dvc'))
    get_dvc_config(Path('/home/gilles/datasets/pneumonia'))