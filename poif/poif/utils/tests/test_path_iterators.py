import tempfile
from pathlib import Path

from poif.utils import (
    CombinedIterator,
    DirectoryIterator,
    FileIterator,
    InOrderPathIterator,
    RecursiveDirectoryIterator,
    RecursiveFileIterator,
)

t = tempfile.mkdtemp()
temp_dir = Path(t)

folder_names = ["a", "b", "c"]
file_names = ["01", "02", "03"]


for file_name in file_names:
    (temp_dir / file_name).touch()

for folder in folder_names:
    (temp_dir / folder).mkdir(exist_ok=True)
    for file_name in file_names:
        (temp_dir / folder / file_name).touch()
    for level2 in folder_names:
        (temp_dir / folder / level2).mkdir(exist_ok=True)


def test_file_iterator():
    count = 0
    for file in FileIterator(temp_dir):
        assert file.parts[-1] in file_names
        count += 1

    assert count == len(file_names)


def test_recursive_file_iterator():
    count = 0
    for file in RecursiveFileIterator(temp_dir):
        assert file.parts[-1] in file_names
        count += 1

    assert count == len(file_names) + len(file_names) * len(folder_names)


def test_folder_iterator():
    count = 0
    for folder in DirectoryIterator(temp_dir):
        assert folder.parts[-1] in folder_names
        count += 1

    assert count == len(folder_names)


def test_recursive_folder_iterator():
    count = 0
    for folder in RecursiveDirectoryIterator(temp_dir):
        assert folder.parts[-1] in folder_names
        count += 1

    assert count == len(folder_names) + len(folder_names) * len(folder_names)


def test_in_order_iterator():
    for folder in InOrderPathIterator(temp_dir):
        print(folder)


def test_combined_iterator():
    iter = CombinedIterator()
    # iter.prepend(FileIterator(temp_dir))
    # iter.append(DirectoryIterator(temp_dir))
    #
    # count = 0
    # for item in iter:
    #     count += 1
    #     if count <= len(file_names):
    #         assert item.is_file()
    #     else:
    #         assert item.is_dir()
    #
    # assert count == len(file_names) + len(folder_names)

    iter.append(DirectoryIterator(temp_dir))
    iter.prepend("test")

    for index, item in enumerate(iter):
        if index == 0:
            assert item == "test"
        else:
            assert item.is_dir()


if __name__ == "__main__":
    test_in_order_iterator()
