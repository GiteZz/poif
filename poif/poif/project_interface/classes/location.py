import configparser
import hashlib
import subprocess
from abc import ABC, abstractmethod
from pathlib import Path

from dataclasses import dataclass, field
from typing import Dict
import tempfile

import cv2
import numpy as np
import requests

from poif.data_cache.base.remote.base import Remote
from poif.typing import URL, FileHash, UrlParams, RelFilePath
from poif.dvc import get_dvc_remote_config, dvc_files_to_tag_file_mapping


@dataclass
class DataLocation:
    data_tag: str

    def get(self):
        Exception('Base class should not be used')


@dataclass
class StringLocation(DataLocation):
    data_str: str

    def get(self):
        return self.data_str


class Origin(ABC):
    @property
    @abstractmethod
    def dataset_tag(self):
        pass

    @property
    @abstractmethod
    def origin_tag(self):
        pass

    @abstractmethod
    def get_tag_file_mapping(self) -> Dict[FileHash, RelFilePath]:
        pass

    @abstractmethod
    def get_remote(self) -> Remote:
        pass


@dataclass
class DvcOrigin:
    """
    Class is lazy loaded which means that until get_tag_file_mapping or get_remote is called the repo
    information is not yet present. If one of these two is called the repo will be cloned and data
    for both(!) of these functions is loaded.
    """
    git_url: str
    git_commit: str

    """
    _dataset_tag is used to define a unique tag per dataset, this is done by hashing the git url
    such that multiple versions of the dataset can coexists and files that stay the same across commits
    are only cached once.
    """
    _dataset_tag: str = field(init=False)
    """
    _origin_tag is defined to have a unique way of representing a specific version of a dataset such that
    the meta information (dir files etc.) are not overwritten of mixed.
    """
    _origin_tag: str = field(init=False)

    _remote: Remote = field(init=False)
    _tag_file_mapping: Dict[FileHash, RelFilePath] = field(init=False)

    def to_url_params(self):
        return {
            'git_url': self.git_url,
            'git_commit': self.git_commit
        }

    @property
    def dataset_tag(self):
        if self._dataset_tag is None:
            self._dataset_tag = hashlib.md5(self.git_url.encode('utf-8')).hexdigest()

        return self._dataset_tag

    @property
    def origin_tag(self):
        if self._origin_tag is None:
            ds_url = f'{self.git_url}?c={self.git_commit}'
            self._origin_tag = hashlib.md5(ds_url.encode('utf-8')).hexdigest()

        return self._dataset_tag

    def init(self):
        repo_path = Path(tempfile.mkdtemp())

        subprocess.call(['git', 'clone', self.git_url, str(repo_path)])
        subprocess.call(['git', 'checkout', self.git_commit], cwd=str(repo_path))

        dvc_files = list(repo_path.rglob('*.dvc'))

        self._remote = get_dvc_remote_config(repo_path)
        self._tag_file_mapping = dvc_files_to_tag_file_mapping(dvc_files, self._remote)

    def get_tag_file_mapping(self) -> Dict[FileHash, RelFilePath]:
        if self._tag_file_mapping is None:
            self.init()
        return self._tag_file_mapping

    def get_remote(self) -> Remote:
        if self._remote is None:
            self.init()
        return self._remote


@dataclass
class DvcDataPoint(DvcOrigin):
    data_tag: FileHash

    def to_url_params(self):
        return {
            'git_url': self.git_url,
            'git_commit': self.git_commit,
            'data_tag': self.data_tag
        }

@dataclass
class DvcLocation(DataLocation):
    url: URL
    git_commit: str
    git_url: str

    def get_params(self) -> UrlParams:
        return {
            'git_url': self.git_url,
            'git_commit': self.git_commit,
            'data_tag': self.data_tag
        }

    def get(self):
        r = requests.get(self.url, params=self.get_params())
        np_buf = np.frombuffer(r.content, np.uint8)
        # TODO check if correct with all formats eg black and white img
        return cv2.imdecode(np_buf, cv2.IMREAD_COLOR)
