from abc import ABC, abstractmethod
from typing import Any

from dataclasses import dataclass

from poif.data.origin.base import Origin
from poif.data.parser.base import ParseMixin
from poif.typing import FileHash


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
class DataPoint(ParseMixin):
    tag: FileHash
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


# @dataclass
# class DvcDataPoint(DataPoint):
#     # TODO change to tag
#     tag: FileHash
#     origin: DvcOrigin
#
#     def to_url_params(self):
#         return {
#             'git_url': self.origin.git_url,
#             'git_commit': self.origin.git_commit,
#             'data_tag': self.data_tag
#         }
#
#     @staticmethod
#     def from_origin(dvc_origin: DvcOrigin, data_tag: FileHash) -> 'DvcDataPoint':
#         return DvcDataPoint(data_tag=data_tag,
#                             origin=dvc_origin
#                             )
#
#     def get(self) -> Any:
#         datapoint_bytes = self.origin.get_file(self.tag)
#         original_extension = self.origin.get_extension(self.tag)
#
#         return self.parse_file(datapoint_bytes, original_extension)
#
#     def get_size(self) -> int:
#         return self.origin.get_file_size(self.tag)
#
