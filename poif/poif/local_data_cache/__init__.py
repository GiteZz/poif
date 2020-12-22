from dataclasses import dataclass, field
from pathlib import Path
from poif.local_data_cache.config import DatasetInfo, S3Config
from poif.project_interface.classes.location import DvcOrigin, DvcDataPoint
from poif.typing import FileHash
from typing import Dict, List, Tuple
from .dvc import get_dvc_remote_config, read_dvc_file, download_s3_file
import subprocess
import hashlib


@dataclass
class LocalCache:
    work_dir: Path

    config_folder: Path = field(init=False)
    ds_info_cache: Path = field(init=False)
    git_folder: Path = field(init=False)
    data_folder: Path = field(init=False)

    cached_ds_info: Dict[FileHash, DatasetInfo] = field(init=False)

    def __post_init__(self):
        # Folder initiation
        self.config_folder = self.work_dir / 'config'
        self.ds_info_cache = self.work_dir / 'ds_info'
        self.git_folder = self.work_dir / 'git_repos'
        self.data_folder = self.work_dir / 'data'

        self.work_dir.mkdir(exist_ok=True)
        self.config_folder.mkdir(exist_ok=True)
        self.ds_info_cache.mkdir(exist_ok=True)
        self.git_folder.mkdir(exist_ok=True)
        self.data_folder.mkdir(exist_ok=True)

        # Reload previous configs
        for file in self.ds_info_cache.glob('*.json'):
            ds_info = DatasetInfo.load(file)
            ds_id = file.parts[-1].replace('.json', '')
            self.cached_ds_info[ds_id] = ds_info

    @staticmethod
    def git_to_tag(dvc_orgin: DvcOrigin):
        ds_url = f'{dvc_orgin.git_url}?c={dvc_orgin.git_commit}'
        ds_key = hashlib.md5(ds_url.encode('utf-8')).hexdigest()
        return ds_key

    def dvc_origin_to_repo_path(self, dvc_origin: DvcOrigin, initialize=False):
        ds_key = LocalCache.git_to_tag(dvc_origin)
        repo_path = self.git_folder / ds_key

        if initialize:
            # We presume that if the folder exist that it contains the correct remote repo
            if not repo_path.exists():
                self.init_git(dvc_origin)

        return repo_path

    def init_git(self, dvc_origin: DvcOrigin):
        repo_url = self.dvc_origin_to_repo_path(dvc_origin)
        subprocess.call(['git', 'clone', dvc_origin.git_url, str(repo_url)])
        subprocess.call(['git', 'checkout', dvc_origin.git_commit], cwd=str(repo_url))

    def get_dvc_files(self, dvc_origin: DvcOrigin) -> List[Path]:
        # Check if the git repo is already initialized
        repo_path = self.dvc_origin_to_repo_path(dvc_origin, initialize=True)
        dvc_files = list(repo_path.rglob('*.dvc'))

        return dvc_files

    def get_dvc_remote(self, dvc_origin: DvcOrigin) -> S3Config:
        repo_path = self.dvc_origin_to_repo_path(dvc_origin, initialize=True)
        remote_config = get_dvc_remote_config(repo_path)

        return remote_config

    def get_dataset_info(self, dvc_origin: DvcOrigin) -> DatasetInfo:
        ds_key = LocalCache.git_to_tag(dvc_origin)

        # Check if info is not already loaded
        if ds_key in self.cached_ds_info:
            return self.cached_ds_info[ds_key]

        ds_info_json = self.ds_info_cache / f'{ds_key}.json'
        if ds_info_json.exists():
            ds_info = DatasetInfo.load(ds_info_json)
            self.cached_ds_info[ds_key] = ds_info
            return ds_info

        dvc_files = self.get_dvc_files(dvc_origin)
        dvc_remote_config = self.get_dvc_remote(dvc_origin)

        repo_data_folder = self.data_folder / ds_key
        repo_data_folder.mkdir(exist_ok=True)

        data_files = {}
        for dvc_file in dvc_files:
            if not dvc_file.is_file():
                continue
            data_files = {**data_files, **read_dvc_file(dvc_file, dvc_remote_config, repo_data_folder)}

        new_ds_info = DatasetInfo(files=data_files, s3_config=dvc_remote_config)
        new_ds_info.save(self.ds_info_cache / f'{ds_key}.json')
        self.cached_ds_info[ds_key] = new_ds_info
        return new_ds_info

    def get_file(self, file_location: DvcDataPoint):
        file_path = self.get_file_path(file_location)

    def get_file_path(self, file_location: DvcDataPoint) -> Path:
        dataset_id = LocalCache.git_to_tag(file_location)
        file_path = self.data_folder / dataset_id / file_location.data_tag
        if file_path.is_file():
            return file_path

        if not dataset_id in self.cached_ds_info:
            ds_info = self.get_dataset_info(file_location)
        else:
            ds_info = self.cached_ds_info[dataset_id]

        download_s3_file(ds_info.s3_config, file_location, file_path)

        return file_path