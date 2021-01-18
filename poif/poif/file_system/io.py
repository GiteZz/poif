from stat import S_IFDIR  # Directory type
from stat import S_IFREG  # Regular file type
from time import time
from typing import Dict, Union, List

from poif.tagged_data import TaggedData
from poif.file_system import PartialGetWrapper


class Directory:
    def __init__(self, contents: Dict[str, Union['Directory', 'File']] = None):
        if contents is None:
            self.contents = {}
        else:
            self.contents = contents

    def mkdir(self, path: str):
        levels_to_create = path.split('/')
        new_level = levels_to_create[0]

        if new_level not in self.contents:
            self.contents[new_level] = Directory()

        if len(levels_to_create) > 1:
            self.contents[new_level].mkdir('/'.join(levels_to_create[1:]))

    def add_file(self, folders: List[str], file_name: str, data: TaggedData):
        if len(folders) == 0:
            self.contents[file_name] = File(name=file_name, data=data)
            return
        new_folder_name = folders[0]

        if new_folder_name not in self.contents:
            self.contents[new_folder_name] = Directory()

        self.contents[new_folder_name].add_file(folders[1:], file_name, data)

    def add_tagged_data(self, data: PartialGetWrapper):
        levels = data.relative_path.split('/')
        file_name = levels[-1]
        folders = levels[:-1]

        self.add_file(folders=folders, file_name=file_name, data=data)

    def get_attr(self):
        return dict(st_mode=(S_IFDIR | 0o555), st_nlink=2)


class File:
    def __init__(self, name: str, data: PartialGetWrapper):
        self.name = name
        self.data = data

    def get_attr(self, size=0, change_status_time=time(), modification_time=time(), access_time=time()):
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