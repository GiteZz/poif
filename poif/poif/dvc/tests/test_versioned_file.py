import json
import tempfile
from pathlib import Path

import pytest

from poif.dvc.file import VersionedFile
from poif.dvc.utils import hash_object
from poif.tests import get_img_file, write_image_in_file


def test_rel_file():
    base_dir = Path('/home/user/datasets')
    file_path = Path('/home/user/datasets/name/train/01.jpg')

    file = VersionedFile(base_dir=base_dir, file_path=file_path)
    assert file.relative_path == 'name/train/01.jpg'

    base_dir = Path('/home/user/datasets/')

    file = VersionedFile(base_dir=base_dir, file_path=file_path)
    assert file.relative_path == 'name/train/01.jpg'


temp_dir = Path(tempfile.mkdtemp())
img_folder = temp_dir / 'image'
img_folder.mkdir(exist_ok=True)
img_path = img_folder / '01.jpg'

write_image_in_file(img_path)
img_hash = hash_object(img_path)


def test_writing():
    vfile = temp_dir / 'test.vfile'
    file = VersionedFile(base_dir=temp_dir, file_path=img_path)
    file.write_vfile(vfile)

    with open(vfile, 'r') as f:
        vfile_contents = json.load(f)

    assert vfile_contents['tag'] == img_hash
    assert vfile_contents['path'] == 'image/01.jpg'
