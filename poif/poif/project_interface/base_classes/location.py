from dataclasses import dataclass
from typing import Dict
from poif.typing import URL, UrlParams
import requests


@dataclass
class DataLocation:
    pass


@dataclass
class HttpLocation(DataLocation):
    url: URL
    params: UrlParams

    def get(self):
        r = requests.get(self.url, params=self.params)
