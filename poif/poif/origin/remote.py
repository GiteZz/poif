from dataclasses import dataclass
from typing import Any, Dict

import requests

from poif.cache.disk_over_http import (GET_FILE_PATH, GET_FILES_PATH,
                                       GET_SIZE_PATH)
from poif.origin.git import DvcOrigin
from poif.typing import FileHash, RelFilePath


@dataclass
class RemoteOrigin(DvcOrigin):
    datacache_url: str

    @property
    def url_params(self):
        return {
            'git_url': self.git_url,
            'git_commit': self.git_commit
        }

    def get_file_url_parameters(self, tag: FileHash):
        return {**self.url_params, 'data_tag': tag}

    def get_tag_file_mapping(self):
        r = requests.get(f'{self.datacache_url}{GET_FILES_PATH}', params=self.url_params)

        return r.json()

    @property
    def tag_to_original_file(self) -> Dict[FileHash, RelFilePath]:
        if self._tag_file_mapping is None:
            self._tag_file_mapping = self.get_tag_file_mapping()
        return self._tag_file_mapping

    def get_file(self, tag: FileHash) -> bytes:
        r = requests.get(f'{self.datacache_url}{GET_FILE_PATH}', params=self.get_file_url_parameters(tag))
        return r.content

    def get_file_size(self, tag: FileHash) -> Any:
        r = requests.get(f'{self.datacache_url}{GET_SIZE_PATH}', params=self.get_file_url_parameters(tag))
        return r.json()['size']
