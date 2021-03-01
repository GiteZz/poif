from collections import defaultdict

from poif.dataset.file_system.base import setup_as_filesystem
from poif.file_system.base import DataSetFileSystem
from poif.file_system.directory import Directory
from poif.tagged_data.base import BinaryData
from poif.tests import get_standard_folder_template, get_temp_path


class MockBinary(BinaryData):
    def __init__(self, data: str):
        self.data = data

    @property
    def size(self) -> int:
        return len(self.data)

    def get(self) -> bytes:
        return bytes(self.data.encode("utf-8"))


def test_without_fuse():
    files = get_standard_folder_template()
    contents_by_folder = defaultdict(set)
    contents_by_folder[""].add("__test_file")
    for file in files:
        file_parts = file.split("/")
        contents_by_folder[""].add(file_parts[0])

        for content_index in range(1, len(file_parts)):
            folder = "/".join(file_parts[:content_index])
            contents_by_folder[folder].add(file_parts[content_index])

    disk_loc = get_temp_path()
    print(disk_loc)

    root_dir = Directory()

    for file in files:
        root_dir.add_data(file, MockBinary(file))

    file_system = DataSetFileSystem(root_dir)

    for folder, folder_contents in contents_by_folder.items():
        assert folder_contents | {".", ".."} == set(file_system.readdir(folder, None))


def test_filesystem_creation():
    files = get_standard_folder_template()

    disk_loc = get_temp_path()
    print(disk_loc)

    root_dir = Directory()

    for file in files:
        root_dir.add_data(file, MockBinary(file))

    p = setup_as_filesystem(root_dir, disk_loc, daemon=True)

    for file in files:
        assert (disk_loc / file).is_file()

    p.terminate()


def test_conversion():
    pass
