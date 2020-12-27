from stat import S_IFDIR  # Directory type
from stat import S_IFREG  # Regular file type
from time import time
from typing import Dict, Union


class Directory:
    def __init__(self, contents: Dict[str, Union['Directory', 'File']]):
        self.contents = contents

    def get_attr(self):
        return dict(st_mode=(S_IFDIR | 0o555), st_nlink=2)

class File:
    name: str

    def get_attr(self, size=0, change_status_time=time(), modification_time=time(), access_time=time()):
        # Info from here: https://man7.org/linux/man-pages/man2/stat.2.html
        return dict(
            st_mode=(S_IFREG | 0o644),  # Contains file type and mode
            st_nlink=1,  # Number of hard links to file
            st_size=size,  # Size of file in bytes
            st_ctime=change_status_time,  # Time of last status change
            st_mtime=modification_time,  # Time of last modification
            st_atime=access_time,  # Time of last access
        )