from poif.tagged_data.base import BinaryData


class MockBinary(BinaryData):
    def __init__(self, data: str):
        self.data = data

    @property
    def size(self) -> int:
        return len(self.data)

    def get(self) -> bytes:
        return bytes(self.data.encode("utf-8"))


# def test_filesystem_creation():
#     files = get_standard_folder_template()
#
#     disk_loc = get_temp_path()
#     print(disk_loc)
#
#     root_dir = Directory()
#
#     for file in files:
#         root_dir.add_data(file, MockBinary(file))
#
#     p = root_dir.setup_as_filesystem(disk_loc)
#
#     for file in files:
#         assert (disk_loc / file).is_file()
#
#     p.terminate()


def test_conversion():
    pass
