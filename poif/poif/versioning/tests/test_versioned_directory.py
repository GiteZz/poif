import json
import tempfile
from pathlib import Path

from poif.tests import write_image_in_file
from poif.utils import hash_object, hash_string
from poif.versioning.directory import VersionedDirectory

temp_dir = Path(tempfile.mkdtemp())
img_folder = temp_dir / "image"
img_folder.mkdir(exist_ok=True)

img1_path = img_folder / "01.jpg"
img2_path = img_folder / "02.jpg"

write_image_in_file(img1_path)
write_image_in_file(img2_path)

img1_hash = hash_object(img1_path)
img2_hash = hash_object(img2_path)

dir_hash = hash_string(img1_hash + img2_hash)


def test_writing():
    directory = VersionedDirectory(base_dir=temp_dir, data_dir=img_folder)
    vdir_file = directory.write_vdir_to_folder(temp_dir)

    with open(vdir_file, "r") as f:
        vdir_contents = json.load(f)

    assert vdir_contents["data_folder"] == "image"
    assert vdir_contents["tag"] == dir_hash

    mapping_contents = directory.get_parsed()

    assert mapping_contents[img1_hash] == "image/01.jpg"
    assert mapping_contents[img2_hash] == "image/02.jpg"
