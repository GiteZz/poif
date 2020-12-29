from pathlib import Path
import tempfile
from poif.utils import FileIterator, FolderIterator, RecursiveFileIterator, RecursivePathOperator, \
    RecursiveFolderIterator

t = tempfile.mkdtemp()
temp_dir = Path(t)

folder_names = ['a', 'b', 'c']
file_names = ['01', '02', '03']


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
    for folder in FolderIterator(temp_dir):
        assert folder.parts[-1] in folder_names
        count += 1

    assert count == len(folder_names)

def test_recursive_folder_iterator():
    count = 0
    for folder in RecursiveFolderIterator(temp_dir):
        assert folder.parts[-1] in folder_names
        count += 1

    assert count == len(folder_names) + len(folder_names) * len(folder_names)