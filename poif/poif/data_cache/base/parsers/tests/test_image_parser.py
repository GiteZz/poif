import random
import tempfile

import cv2
import numpy as np
import pytest

from poif.data_cache.base.parsers.image import ImageParser
from poif.tests import get_img


def test_correct_loading():
    original_img = get_img()
    file_by_extension = {}
    img_bgr = cv2.cvtColor(original_img, cv2.COLOR_RGB2BGR)
    h, w, c = original_img.shape

    for extension in ImageParser.approved_extensions:
        img_file = tempfile.mkstemp(suffix=f'.{extension}')[1]

        cv2.imwrite(img_file, img_bgr)

        with open(img_file, 'rb') as f:
            img_bytes = f.read()

        loaded_img = ImageParser.parse(img_bytes)

        file_by_extension[extension] = tempfile.mkstemp(suffix=f'.{extension}')[1]
        # Convert to np.int16 otherwise a difference of -1 is converted to 255
        abs_map = np.abs(original_img.astype(np.int16) - loaded_img.astype(np.int16))
        av_pixel_diff = np.sum(abs_map) / (w * h * 3)
        # some extension are lossy so we can't be sure that the image will be exactly the same
        assert av_pixel_diff < 5