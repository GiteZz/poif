from pathlib import Path
import tempfile
from poif.utils import get_relative_path, FileIterator, FolderIterator


def test_rel_file():
    base_dir = Path('/home/user/datasets')
    file_path = Path('/home/user/datasets/name/train/01.jpg')

    assert get_relative_path(base_dir=base_dir, file=file_path) == 'name/train/01.jpg'

    base_dir = Path('/home/user/datasets/')

    assert get_relative_path(base_dir=base_dir, file=file_path) == 'name/train/01.jpg'

    destination_dir = Path('/home/user/datasets/images')

    assert get_relative_path(base_dir=base_dir, file=destination_dir) == 'images'

    destination_dir = Path('/home/user/datasets/images/')

    assert get_relative_path(base_dir=base_dir, file=destination_dir) == 'images'