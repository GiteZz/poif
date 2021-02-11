import time
from multiprocessing import Process
from pathlib import Path
from stat import S_IFDIR
from typing import Dict, List, Union

from fuse import FUSE

from poif.file_system.base import DataSetFileSystem
from poif.file_system.file import File
from poif.tagged_data.base import BinaryData, StringBinaryData
from poif.typing import RelFilePath


class Directory:
    def __init__(self, contents: Dict[str, Union["Directory", "File"]] = None):
        if contents is None:
            self.contents = {}
        else:
            self.contents = contents

        self.add_data("__test_file", StringBinaryData(""))

    def mkdir(self, path: str):
        levels_to_create = path.split("/")
        new_level = levels_to_create[0]

        if new_level not in self.contents:
            self.contents[new_level] = Directory()

        if len(levels_to_create) > 1:
            self.contents[new_level].mkdir("/".join(levels_to_create[1:]))

    def add_file(self, folders: List[str], file_name: str, data: BinaryData):
        if len(folders) == 0:
            self.contents[file_name] = File(name=file_name, data=data)
            return
        new_folder_name = folders[0]

        if new_folder_name not in self.contents:
            self.contents[new_folder_name] = Directory()

        self.contents[new_folder_name].add_file(folders[1:], file_name, data)

    def add_data(self, rel_path: RelFilePath, data: BinaryData):
        levels = rel_path.split("/")
        file_name = levels[-1]
        folders = levels[:-1]

        self.add_file(folders=folders, file_name=file_name, data=data)

    def get_attr(self):
        return dict(st_mode=(S_IFDIR | 0o555), st_nlink=2)

    def setup_as_filesystem(self, system_path: Path, daemon=False):
        file_system = DataSetFileSystem(root_dir=self)

        p = Process(target=setup_filesystem, args=(file_system, system_path), daemon=daemon)
        p.start()

        while not (system_path / "__test_file").exists():
            print("Wait")
            time.sleep(0.02)

        return p


def setup_filesystem(filesystem: DataSetFileSystem, system_path: Path):
    fuse_handler = FUSE(
        filesystem,
        str(system_path),
        foreground=True,
        allow_other=False,
    )
