import hashlib
from pathlib import Path
import subprocess
import yaml
import configparser
from typing import List, Dict
from dataclasses import dataclass, field
from botocore.client import Config
import boto3
import json
from poif.data_cache.data_handling.config import (
    poif_ds_info_dict,
    S3Config,
    DatasetInfo,
    RelFilePath,
    poif_git_folder,
    poif_data_folder,
    FileHash,
    poif_ds_info_folder
)

DatasetID = str


def init_git(init_folder: Path, git_url: str, commit: str) -> None:
    subprocess.call(['git', 'clone', git_url, str(init_folder)])
    subprocess.call(['git', 'checkout', commit], cwd=str(init_folder))


def git_to_tag(git_url: str, git_commit: str) -> str:
    ds_url = f'{git_url}?c={git_commit}'
    ds_key = hashlib.md5(ds_url.encode('utf-8')).hexdigest()
    return ds_key


def get_dataset_info(git_url: str, git_commit: str) -> DatasetInfo:
    ds_key = git_to_tag(git_url, git_commit)

    # Check if info is not already loaded
    if ds_key in poif_ds_info_dict:
        return poif_ds_info_dict[ds_key]

    ds_info_json = poif_ds_info_folder / f'{ds_key}.json'
    if ds_info_json.exists():
        ds_info = DatasetInfo.load(ds_info_json)
        poif_ds_info_dict[ds_key] = ds_info
        return ds_info

    # Check if the git repo is already initialized
    repo_path = poif_git_folder / ds_key
    if not (poif_git_folder / ds_key).exists():
        init_git(repo_path, git_url, git_commit)

    dvc_files = repo_path.rglob('*.dvc')
    remote_config = get_dvc_remote_config(repo_path)

    repo_data_folder = poif_data_folder / ds_key
    repo_data_folder.mkdir(exist_ok=True)

    data_files = {}
    for dvc_file in dvc_files:
        if not dvc_file.is_file():
            continue
        data_files = {**data_files, **read_dvc_file(dvc_file, remote_config, repo_data_folder)}

    new_ds_info = DatasetInfo(files=data_files, s3_config=remote_config)
    new_ds_info.save(poif_ds_info_folder / f'{ds_key}.json')
    poif_ds_info_dict[ds_key] = new_ds_info
    return new_ds_info


def get_dvc_remote_config(repo_url: Path) -> S3Config:
    dvc_config_file = repo_url / '.dvc' / 'config'
    parser = configparser.ConfigParser()
    parser.read(dvc_config_file)
    for key in parser.keys():
        if 'remote' in key:
            return S3Config(
                url=parser[key]['url'],
                endpointurl=parser[key]['endpointurl'],
                profile=parser[key]['profile']
                )


def read_dvc_file(dvc_file: Path, s3_config: S3Config, data_folder: Path) -> Dict[FileHash, RelFilePath]:
    """
    Read one dvc file and return the contents.
    """
    new_files = {}
    with open(dvc_file, 'r') as f:
        contents = yaml.safe_load(f)

    for file_info in contents['outs']:
        if '.dir' in file_info['md5']:
            dvc_file_folder_path = data_folder / file_info['path']
            dvc_file_folder_path.mkdir(exist_ok=True)
            dir_dest = dvc_file_folder_path / 'folder.dir'

            download_s3_file(s3_config, file_info["md5"], dir_dest)

            with open(dir_dest, 'r') as f:
                dir_file_contents = json.load(f)
            for file in dir_file_contents:
                new_files[file['md5']] = f'{file_info["path"]}/{file["relpath"]}'
        else:
            raise NotImplemented("")

        return new_files


def download_s3_file(s3_config: S3Config, file_hash: FileHash, dest_file: Path) -> None:
    dataset_sess = boto3.session.Session(profile_name=s3_config.profile)
    s3 = dataset_sess.resource('s3',
                               endpoint_url=s3_config.endpointurl,
                               config=Config(signature_version='s3v4')
                               )
    file_name = f'{s3_config.folder}/{file_hash[:2]}/{file_hash[2:]}'

    s3.Bucket(f'{s3_config.bucket}').download_file(file_name, str(dest_file))


def get_file_path(git_url: str, git_commit: str, file_id: FileHash) -> Path:
    dataset_id = git_to_tag(git_url, git_commit)
    file_path = poif_data_folder / dataset_id / file_id
    if file_path.is_file():
        return file_path
    ds_info = poif_ds_info_dict[dataset_id]
    download_s3_file(ds_info.s3_config, file_id, file_path)

    return file_path


if __name__ == "__main__":
    get_dvc_files('https://github.ugent.be/gballege/pneunomia_dataset', 'cfd0ffa638f5db0fd8d828153bfaefe775bb4716')
    # read_dvc_file(Path('/home/gilles/datasets/pneumonia/test.dvc'))
    print(get_dvc_remote_config(Path('/home/gilles/datasets/pneumonia')))