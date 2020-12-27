import configparser
import json
import tempfile
from pathlib import Path
from typing import Dict, List, Tuple

import yaml

from poif.data.remote.base import Remote
from poif.data.remote.s3 import S3Remote
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


def get_tag_to_file_from_repo(repo: Path, remote: Remote) -> Dict[FileHash, RelFilePath]:
    dvc_files = get_dvc_files_from_repo(repo)

    data_files = []
    for dvc_file in dvc_files:
        # TODO remote should not really be passed around
        # First get all the remote objects and then parse
        data_files.extend(get_tag_file_tuples(dvc_file, remote))

    return {tag: file_name for tag, file_name in data_files}


def get_tag_file_tuples(dvc_file: Path, remote: Remote) -> List[Tuple[FileHash, RelFilePath]]:
    """
    Read one dvc file and return the contents.
    """
    new_files = []

    for file_info in get_contained_files(dvc_file):
        if is_directory_file(file_info):
            dir_file_contents = get_file_contents(file_info, remote)
            for file in dir_file_contents:
                new_files.append((file['md5'], f'{file_info["path"]}/{file["relpath"]}'))
        else:
            raise NotImplemented("")

    return new_files


def get_contained_files(dvc_file: Path):
    with open(dvc_file, 'r') as f:
        contents = yaml.safe_load(f)

    return contents['outs']


def get_file_contents(file_info: dict, remote: Remote):
    temp_file = Path(tempfile.mkstemp())

    remote.download_file(file_info["md5"], temp_file)

    with open(temp_file, 'r') as f:
        dir_file_contents = json.load(f)

    return dir_file_contents


def is_directory_file(file_info: dict):
    return '.dir' in file_info['md5']


def get_dvc_files_from_repo(repo: Path):
    return [item for item in repo.rglob('*.dvc') if item.is_file()]
