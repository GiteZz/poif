from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any

from poif.data.origin.base import Origin
from poif.data.parser.base import ParseMixin
from poif.data.versioning.base import Tagged


@dataclass
class DataPoint(Tagged, ParseMixin):
    origin: Origin

    @property
    def size(self) -> int:
        return self.get_size()

    @property
    def extension(self) -> str:
        return self.origin.get_extension(self.tag)

    def get(self) -> Any:
        datapoint_bytes = self.origin.get_file(self.tag)

        return self.parse_file(datapoint_bytes, self.extension)

    def get_size(self) -> int:
        return self.origin.get_file_size(self.tag)
