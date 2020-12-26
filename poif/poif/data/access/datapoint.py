from abc import ABC, abstractmethod
from dataclasses import dataclass

import cv2
import numpy as np
import requests

from poif.data.access.origin import DvcOrigin
from poif.typing import URL, FileHash, UrlParams


@dataclass
class DataLocation(ABC):
    data_tag: str

    @abstractmethod
    def get(self):
        pass


@dataclass
class StringLocation(DataLocation):
    data_str: str

    def get(self):
        return self.data_str


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
