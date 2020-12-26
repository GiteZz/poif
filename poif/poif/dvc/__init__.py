from typing import List

from poif.data.cache.base.remote import Remote

import tempfile

import configparser
import json
from pathlib import Path
from typing import Dict

import yaml

from poif.data.cache.base.remote import S3Remote
from poif.typing import FileHash, RelFilePath


def get_dvc_remote_config(repo_path: Path) -> Remote:
    dvc_config_file = repo_path / '.dvc' / 'config'
    parser = configparser.ConfigParser()
    parser.read(dvc_config_file)
    for key in parser.keys():
        if 'remote' in key:
            return S3Remote(
                url=parser[key]['url'],
                endpointurl=parser[key]['endpointurl'],
                profile=parser[key]['profile']
            )
    raise Exception('Remote was not found')


def dvc_files_to_tag_file_mapping(dvc_files: List[Path], remote: Remote):
    data_files = {}
    for dvc_file in dvc_files:
        # TODO: wtf?
        if not dvc_file.is_file():
            continue
        data_files = {**data_files, **dvc_file_to_tag_file_mapping(dvc_file, remote)}


def dvc_file_to_tag_file_mapping(dvc_file: Path, remote: Remote) -> Dict[FileHash, RelFilePath]:
    """
    Read one dvc file and return the contents.
    """
    new_files = {}
    with open(dvc_file, 'r') as f:
        contents = yaml.safe_load(f)

    for file_info in contents['outs']:
        if '.dir' in file_info['md5']:
            temp_file = Path(tempfile.mkstemp())

            remote.download_file(file_info["md5"], temp_file)

            with open(temp_file, 'r') as f:
                dir_file_contents = json.load(f)
            for file in dir_file_contents:
                new_files[file['md5']] = f'{file_info["path"]}/{file["relpath"]}'
        else:
            raise NotImplemented("")

        return new_files
