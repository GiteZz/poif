import json
import random
import tempfile
from pathlib import Path
from typing import List

import cv2
import numpy as np

from poif.git.file import FileCreatorMixin
from poif.remote.base import FileRemote
from poif.repo.file_remote import FileRemoteTaggedRepo
from poif.typing import RelFilePath


def get_img(height: int = 200, width: int = 200, bw: bool = False) -> np.ndarray:
    middle_x = width // 2
    middle_y = height // 2

    if not bw:
        img = np.zeros((height, width, 3)).astype(np.uint8)

        random_rgb = lambda: [random.randint(0, 255) for _ in range(3)]

        img[:middle_y, :middle_x] = random_rgb()
        img[middle_y:, :middle_x] = random_rgb()
        img[:middle_y, middle_x:] = random_rgb()
        img[middle_y:, middle_x:] = random_rgb()

        return img
    else:
        img = np.zeros((height, width)).astype(np.uint8)

        random_bw = lambda: random.randint(0, 255)

        img[:middle_y, :middle_x] = random_bw()
        img[middle_y:, :middle_x] = random_bw()
        img[:middle_y, middle_x:] = random_bw()
        img[middle_y:, middle_x:] = random_bw()

        return img


def get_img_file() -> Path:
    img_file = Path(tempfile.mkstemp(suffix=".png")[1])
    write_image_in_file(img_file)

    return img_file


def write_image_in_file(file: Path):
    img = get_img()
    cv2.imwrite(str(file), img)


def write_json_in_file(file: Path):
    json_content = {"test": "test"}

    with open(file, "w") as f:
        json.dump(json_content, f)


def create_data_folder(folder: Path):
    folder.mkdir(exist_ok=True, parents=True)

    for i in range(10):
        write_image_in_file(folder / (str(i) + ".png"))


def assert_image_nearly_equal(original_img: np.ndarray, new_img: np.ndarray):
    h, w, c = original_img.shape
    abs_map = np.abs(original_img.astype(np.int16) - new_img.astype(np.int16))
    av_pixel_diff = np.sum(abs_map) / (w * h * 3)
    # some extension are lossy so we can't be sure that the image will be exactly the same
    assert av_pixel_diff < 5


def get_standard_folder_template() -> List[RelFilePath]:
    files = [f"0{i}.jpg" for i in range(10)]
    base_folders = ["train", "val", "test"]
    sub_folders = ["image", "mask"]

    files_to_create = []

    additional_files = [
        "meta.json",
        "train/train_meta.json",
        "val/val_meta.json",
        "test/test_meta.json",
    ]

    for base_folder in base_folders:
        for sub_folder in sub_folders:
            for file in files:
                files_to_create.append(f"{base_folder}/{sub_folder}/{file}")

    for file in additional_files:
        files_to_create.append(file)

    return files_to_create


def create_standard_folder_structure():
    t = tempfile.mkdtemp()
    temp_dir = Path(t)

    template = get_standard_folder_template()
    for file in template:
        file_path = temp_dir / file
        file_path.parent.mkdir(exist_ok=True, parents=True)
        file_path.touch()

    return temp_dir


def get_temp_path() -> Path:
    return Path(tempfile.mkdtemp())


def get_temp_file() -> Path:
    return Path(tempfile.mkstemp()[1])


class MonkeyPatchSequence:
    def __init__(self, values: list):
        self.values = values

    def __call__(self):
        return self.values.pop(0)


class MockFileRemote(FileRemote):
    def __init__(self):
        self.uploaded_files = []
        self.downloaded_files = []

    def download(self, remote_source: str) -> bytes:
        self.downloaded_files.append(remote_source)
        return bytes("Hello")

    def get_object_size(self, file_name: str):
        return 0

    def upload(self, source: bytes, remote_dest: str):
        self.uploaded_files.append(remote_dest)


class MockTaggedRepo(FileRemoteTaggedRepo):
    def __init__(self):
        self.remote = MockFileRemote()
        self.data_folder = "data"


class MockGitRepo:
    def __init__(self, base_dir: str, init=True):
        self.tracked_files = []

    def add_files(self, files: List[Path]):
        for file in files:
            self.tracked_files.append(file)

    def add_remote(self, remote: str):
        pass

    def commit(self, message: str):
        pass

    def push(self):
        pass

    def add_file_creator(self, creator: FileCreatorMixin):
        pass
