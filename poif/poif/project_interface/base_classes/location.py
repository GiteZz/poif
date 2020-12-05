from dataclasses import dataclass
from typing import Dict
from poif.typing import URL, UrlParams
import requests
import numpy as np
import cv2


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


@dataclass
class HttpLocation(DataLocation):
    url: URL
    commit: str
    git_url: str

    def get_parames(self) -> UrlParams:
        return {

        }

    def get(self):
        r = requests.get(self.url, params=self.params)
        np_buf = np.frombuffer(r.content)
        # TODO check if correct with all formats eg black and white img
        return cv2.imdecode(np_buf, cv2.IMREAD_COLOR)
