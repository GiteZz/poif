from stat import S_IFDIR
from typing import Dict, List, Union

from poif.file_system.file import File
from poif.tagged_data.base import BinaryData
from poif.typing import RelFilePath


class Directory:
    def __init__(self, contents: Dict[str, Union["Directory", "File"]] = None):
        if contents is None:
            self.contents = {}
        else:
            self.contents = contents

    def mkdir(self, path: str):
        """
        Allow for creation of directories, creates relevant subdirectories
        """
        levels_to_create = path.split("/")
        new_level = levels_to_create[0]

        if new_level not in self.contents:
            self.contents[new_level] = Directory()

        if len(levels_to_create) > 1:
            next_dir = self.contents[new_level]
            if isinstance(next_dir, Directory):
                next_dir.mkdir("/".join(levels_to_create[1:]))
            else:
                raise Exception("Can't create directory while file exists with the same name.")

    def add_file(self, folders: List[str], file_name: str, data: BinaryData):
        if len(folders) == 0:
            self.contents[file_name] = File(name=file_name, data=data)
            return
        new_folder_name = folders[0]

        if new_folder_name not in self.contents:
            self.contents[new_folder_name] = Directory()

        folder_to_add_in = self.contents[new_folder_name]
        if isinstance(folder_to_add_in, Directory):
            folder_to_add_in.add_file(folders[1:], file_name, data)
        else:
            raise Exception("Can't add content to file")

    def add_data(self, rel_path: RelFilePath, data: BinaryData):
        levels = rel_path.split("/")
        file_name = levels[-1]
        folders = levels[:-1]

        self.add_file(folders=folders, file_name=file_name, data=data)

    def get_attr(self):
        return dict(st_mode=(S_IFDIR | 0o555), st_nlink=2)
