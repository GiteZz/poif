import tempfile

import cv2

from poif.parser.image import ImageParser
from poif.tests import assert_image_nearly_equal, get_img


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
        assert_image_nearly_equal(original_img, loaded_img)