import cv2
import numpy as np

from poif.parser.base import Parser


class ImageParser(Parser):
    approved_extensions = ["jpg", "png", "jpeg"]

    @staticmethod
    def parse(to_parse: bytes) -> np.ndarray:
        np_buf = np.frombuffer(to_parse, np.uint8)
        # TODO check if correct with all formats eg black and white img
        img_bgr = cv2.imdecode(np_buf, cv2.IMREAD_COLOR)
        img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)

        return img_rgb
