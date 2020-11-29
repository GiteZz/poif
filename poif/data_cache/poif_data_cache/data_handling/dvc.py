from poif_data_cache.config import git_mapping, git_folder, data_folder
import hashlib
from pathlib import Path
import subprocess
import yaml
import configparser
from typing import List
from dataclasses import dataclass, field
from botocore.client import Config
import boto3
import json
from poif_data_cache.data_handling.config import S3Config

DatasetID = str


def init_git(init_folder: Path, git_url: str, commit: str) -> None:
    subprocess.call(['git', 'clone', git_url, str(init_folder)])
    subprocess.call(['git', 'checkout', {commit}], cwd=str(init_folder))


def get_dvc_files(git_url, commit):
    ds_key = f'{git_url}?c={commit}'
    ds_key = hashlib.md5(ds_key.encode('utf-8')).hexdigest()
    repo_path = git_folder / ds_key
    if not (git_folder / ds_key).exists():
        init_git(repo_path, git_url, commit)

    dvc_files = repo_path.rglob('*.dvc')
    dvc_config = get_dvc_remote_config(repo_path)

    repo_data_folder = data_folder / ds_key
    repo_data_folder.mkdir(exist_ok=True)

    data_files = []
    for dvc_file in dvc_files:
        if not dvc_file.is_file():
            continue
        data_files.extend(read_dvc_file(dvc_file, dvc_config, repo_data_folder))
    return {
        'dataset_key': ds_key,
        'files': data_files
    }


def get_dvc_remote_config(repo_url: Path) -> S3Config:
    dvc_config_file = repo_url / '.dvc' / 'config'
    parser = configparser.ConfigParser()
    parser.read(dvc_config_file)
    for key in parser.keys():
        if 'remote' in key:
            return S3Config(url=parser[key]['url'],
                             endpointurl=parser[key]['endpointurl'],
                             profile=parser[key]['profile']
                             )


def read_dvc_file(dvc_file: Path, dvc_config: S3Config, data_folder: Path):
    new_files = []
    with open(dvc_file, 'r') as f:
        contents = yaml.safe_load(f)

    for file_info in contents['outs']:
        if '.dir' in file_info['md5']:
            dataset_sess = boto3.session.Session(profile_name=dvc_config.profile)
            s3 = dataset_sess.resource('s3',
                                       endpoint_url=dvc_config.endpointurl,
                                       config=Config(signature_version='s3v4')
                                       )
            file_name = f'{dvc_config.folder}/{file_info["md5"][:2]}/{file_info["md5"][2:]}'
            dvc_file_folder_path = data_folder / file_info['path']
            dvc_file_folder_path.mkdir(exist_ok=True)
            dir_dest = dvc_file_folder_path / 'folder.dir'
            s3.Bucket(f'{dvc_config.bucket}').download_file(file_name, str(dir_dest))

            with open(dir_dest, 'r') as f:
                dir_file_contents = json.load(f)
            for file in dir_file_contents:
                new_content = {
                    'md5': file['md5'],
                    'path': f'{file_info["path"]}/{file["relpath"]}'
                }
                new_files.append(new_content)
        else:
            raise NotImplemented("")

        return new_files

if __name__ == "__main__":
    get_dvc_files('https://github.ugent.be/gballege/pneunomia_dataset', 'cfd0ffa638f5db0fd8d828153bfaefe775bb4716')
    # read_dvc_file(Path('/home/gilles/datasets/pneumonia/test.dvc'))
    print(get_dvc_remote_config(Path('/home/gilles/datasets/pneumonia')))