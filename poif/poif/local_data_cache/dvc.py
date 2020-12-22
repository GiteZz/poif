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
from poif.local_data_cache.config import (
    S3Config,
    DatasetInfo,
    RelFilePath,
    FileHash
)
from poif.project_interface.classes.location import DvcDataPoint

DatasetID = str


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


def download_s3_file(s3_config: S3Config, dvc_datapoint: DvcDataPoint, dest_file: Path) -> None:
    dataset_sess = boto3.session.Session(profile_name=s3_config.profile)
    s3 = dataset_sess.resource('s3',
                               endpoint_url=s3_config.endpointurl,
                               config=Config(signature_version='s3v4')
                               )
    file_name = f'{s3_config.folder}/{dvc_datapoint.data_tag[:2]}/{dvc_datapoint.data_tag[2:]}'

    s3.Bucket(f'{s3_config.bucket}').download_file(file_name, str(dest_file))



if __name__ == "__main__":
    get_dvc_files('https://github.ugent.be/gballege/pneunomia_dataset', 'cfd0ffa638f5db0fd8d828153bfaefe775bb4716')
    # read_dvc_file(Path('/home/gilles/datasets/pneumonia/test.dvc'))
    print(get_dvc_remote_config(Path('/home/gilles/datasets/pneumonia')))