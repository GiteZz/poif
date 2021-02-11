# TODO figure out / delete

import hashlib
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict

from poif.origin import Origin
from poif.remote.base import Remote
from poif.typing import FileHash, RelFilePath
from poif.versioning.base import Tagged


class LocalGitOrigin(Origin):
    @property
    def dataset_tag(self) -> str:
        pass

    @property
    def origin_tag(self) -> str:
        pass

    @property
    def tag_to_original_file(self) -> Dict[FileHash, RelFilePath]:
        pass


@dataclass
class RemoteGitOrigin(LocalGitOrigin):
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

    _dataset_name: str = field(init=False)

    @property
    def dataset_tag(self):
        if self._dataset_tag is None:
            self._dataset_tag = hashlib.md5(self.git_url.encode("utf-8")).hexdigest()

        return self._dataset_tag

    @property
    def origin_tag(self):
        if self._origin_tag is None:
            ds_url = f"{self.git_url}?c={self.git_commit}"
            self._origin_tag = hashlib.md5(ds_url.encode("utf-8")).hexdigest()

        return self._dataset_tag

    @property
    def tag_to_original_file(self) -> Dict[FileHash, RelFilePath]:
        if self._tag_file_mapping is None:
            self.init()
        return self._tag_file_mapping

    @property
    def remote(self) -> Remote:
        if self._remote is None:
            self.init()
        return self._remote

    def init(self):
        repo = Path(tempfile.mkdtemp())

        subprocess.call(["git", "clone", self.git_url, str(repo)])
        subprocess.call(["git", "checkout", self.git_commit], cwd=str(repo))

        self._remote = get_dvc_remote_config(repo)
        self._tag_file_mapping = get_tag_to_file_from_repo(repo, self._remote)

    def get_file(self, item: Tagged) -> bytes:
        return self.remote.get_file(tag)

    def get_file_size(self, tag: FileHash) -> Any:
        return self.remote.get_object_size(tag)

    def get_extension(self, tag: FileHash) -> str:
        original_file = self.tag_to_original_file[tag]
        file_name = Path(original_file).parts[-1]
        extension = file_name.split(".")[-1]

        return extension
