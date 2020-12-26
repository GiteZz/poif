import hashlib
import subprocess
import tempfile
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict

from poif.dvc import dvc_files_to_tag_file_mapping, get_dvc_remote_config
from poif.typing import FileHash, RelFilePath


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