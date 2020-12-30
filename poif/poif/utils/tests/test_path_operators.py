from pathlib import Path

from poif.tests import get_temp_path
from poif.utils import (files_by_extension, get_extension_from_path,
                        is_more_populated, get_file_name_from_path)


def test_get_extension():
    f1 = Path('/test/dataset/file.jpg')
    f2 = Path('/hello/home/test_long_name.png')

    assert get_extension_from_path(f1) == 'jpg'
    assert get_extension_from_path(f2) == 'png'


def test_get_filename():
    f1 = Path('/test/dataset/file.jpg')
    f2 = Path('/hello/home/test_long_name.png')

    assert get_file_name_from_path(f1) == 'file'
    assert get_file_name_from_path(f2) == 'test_long_name'


def test_extension_bins():
    temp_path = get_temp_path()

    jpg_files = [f'{i}.jpg' for i in range(10)]
    png_files = [f'{i}.png' for i in range(10)]
    exif_files = [f'{i}.exif' for i in range(10)]

    all_files = jpg_files + png_files + exif_files

    for file in all_files:
        (temp_path / file).touch()

    extension_bins = files_by_extension(temp_path)

    assert len(extension_bins['jpg']) == 10
    assert len(extension_bins['png']) == 10
    assert len(extension_bins['exif']) == 10

    assert set(extension_bins['jpg']) == {temp_path / jpg_file for jpg_file in jpg_files}

    extension_bins = files_by_extension(temp_path, limit=20)

    assert len(extension_bins['jpg']) == 10
    assert len(extension_bins['png']) == 10
    assert len(extension_bins['exif']) == 10

    limit = 2
    extension_bins = files_by_extension(temp_path, limit=limit)

    assert len(extension_bins['jpg']) == limit
    assert len(extension_bins['png']) == limit
    assert len(extension_bins['exif']) == limit


def test_is_more_populated():
    temp_path = get_temp_path()

    jpg_files = [f'{i}.jpg' for i in range(10)]

    for file in jpg_files:
        (temp_path / file).touch()

    assert not is_more_populated(temp_path, 11)
    assert not is_more_populated(temp_path, 10)
    assert is_more_populated(temp_path, 9)


