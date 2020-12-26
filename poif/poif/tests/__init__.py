import random
import tempfile

import cv2
import numpy as np


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


def get_img_file():
    img = get_img()
    img_file = tempfile.mkstemp(suffix='.png')[1]

    cv2.imwrite(img_file, img)

    return img_file


def assert_image_nearly_equal(original_img: np.ndarray, new_img: np.ndarray):
    h, w, c = original_img.shape
    abs_map = np.abs(original_img.astype(np.int16) - new_img.astype(np.int16))
    av_pixel_diff = np.sum(abs_map) / (w * h * 3)
    # some extension are lossy so we can't be sure that the image will be exactly the same
    assert av_pixel_diff < 5