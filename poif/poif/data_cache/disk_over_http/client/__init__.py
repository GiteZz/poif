
from dataclasses import dataclass
from typing import Any, Dict

import requests

from poif.data_cache.base.base import DvcCache
from poif.data_cache.disk_over_http import GET_FILE_PATH, GET_FILES_PATH
from poif.project_interface.classes.location import DvcDataPoint, DvcOrigin
from poif.typing import FileHash, RelFilePath


@dataclass
class RemoteCache(DvcCache):
    datacache_url: str

    def __post_init__(self):
        if self.datacache_url[-1] == '/':
            self.datacache_url = self.datacache_url[:-1]

    def get_file(self, dvc_datapoint: DvcDataPoint) -> Any:
        r = requests.get(f'{self.datacache_url}{GET_FILE_PATH}', params=dvc_datapoint.to_url_params())
        return self.parse_file(r.content, r.headers['extension'])

    def get_files(self, dvc_origin: DvcOrigin) -> Dict[FileHash, RelFilePath]:
        r = requests.get(f'{self.datacache_url}{GET_FILES_PATH}', params=dvc_origin.to_url_params())

        return r.json()

    def get_file_size(self, dvc_datapoint: DvcDataPoint) -> int:
        pass