from stat import S_IFREG
from time import time

from poif.file_system.partial import PartialGetWrapper
from poif.tagged_data.base import BinaryData


class File:
    def __init__(self, name: str, data: BinaryData):
        self.name = name
        self.data = PartialGetWrapper(data)

    def get_attr(
        self,
        size=0,
        change_status_time=time(),
        modification_time=time(),
        access_time=time(),
    ):
        # Info from here: https://man7.org/linux/man-pages/man2/stat.2.html
        return dict(
            st_mode=(S_IFREG | 0o644),  # Contains file type and mode
            st_nlink=1,  # Number of hard links to file
            st_size=self.data.size,  # Size of file in bytes
            st_ctime=change_status_time,  # Time of last status change
            st_mtime=modification_time,  # Time of last modification
            st_atime=access_time,  # Time of last access
        )

    def partial_read(self, offset: int, length: int):
        return self.data.get_partial(offset, length)

    @staticmethod
    def get_empty_attr():
        return dict(
            st_mode=(S_IFREG | 0o644),  # Contains file type and mode
            st_nlink=1,  # Number of hard links to file
            st_size=0,  # Size of file in bytes
            st_ctime=0,  # Time of last status change
            st_mtime=0,  # Time of last modification
            st_atime=0,  # Time of last access
        )
