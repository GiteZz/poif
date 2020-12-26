import configparser
import json
from pathlib import Path
from typing import Dict

import yaml
from disk.config import FileHash, RelFilePath, S3Config

from poif.data_cache.base.remote.base import Remote
from poif.data_cache.disk import s3_download_file

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


def read_dvc_file(dvc_file: Path, remote: Remote, data_folder: Path) -> Dict[FileHash, RelFilePath]:
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

            remote.download_file(file_info["md5"], dir_dest)

            with open(dir_dest, 'r') as f:
                dir_file_contents = json.load(f)
            for file in dir_file_contents:
                new_files[file['md5']] = f'{file_info["path"]}/{file["relpath"]}'
        else:
            raise NotImplemented("")

        return new_files


if __name__ == "__main__":
    get_dvc_files('https://github.ugent.be/gballege/pneunomia_dataset', 'cfd0ffa638f5db0fd8d828153bfaefe775bb4716')
    # read_dvc_file(Path('/home/gilles/datasets/pneumonia/test.dvc'))
    print(get_dvc_remote_config(Path('/home/gilles/datasets/pneumonia')))