import random
import tempfile
from pathlib import Path

import cv2
import numpy as np
import pytest


def get_img():
    img_width = 200
    img_height = 200

    middle_x = img_width // 2
    middle_y = img_height // 2

    img = np.zeros((img_height, img_width, 3)).astype(np.uint8)

    random_rgb = lambda: [random.randint(0, 255) for _ in range(3)]

    img[:middle_y, :middle_x] = random_rgb()
    img[middle_y:, :middle_x] = random_rgb()
    img[:middle_y, middle_x:] = random_rgb()
    img[middle_y:, middle_x:] = random_rgb()

    return img


def get_img_file() -> Path:
    img_file = Path(tempfile.mkstemp(suffix='.png')[1])
    write_image_in_file(img_file)

    return img_file


def write_image_in_file(file: Path):
    img = get_img()
    cv2.imwrite(str(file), img)


def assert_image_nearly_equal(original_img: np.ndarray, new_img: np.ndarray):
    h, w, c = original_img.shape
    abs_map = np.abs(original_img.astype(np.int16) - new_img.astype(np.int16))
    av_pixel_diff = np.sum(abs_map) / (w * h * 3)
    # some extension are lossy so we can't be sure that the image will be exactly the same
    assert av_pixel_diff < 5


def create_standard_folder_structure():
    t = tempfile.mkdtemp()
    temp_dir = Path(t)

    files = [f'0{i}.jpg' for i in range(10)]
    base_folders = ['train', 'val', 'test']
    sub_folders = ['image', 'mask']

    additional_files = [
        'meta.json',
        'train/train_meta.json',
        'val/val_meta.json',
        'test/test_meta.json',
    ]

    for base_folder in base_folders:
        for sub_folder in sub_folders:
            for file in files:
                file_path = temp_dir / base_folder / sub_folder / file
                file_path.parent.mkdir(parents=True, exist_ok=True)
                file_path.touch()

    for file in additional_files:
        (temp_dir / file).touch()

    return temp_dir

def get_temp_path() -> Path:
    return Path(tempfile.mkdtemp())


class MonkeyPatchSequence:
    def __init__(self, values: list):
        self.values = values

    def __call__(self):
        return self.values.pop(0)
