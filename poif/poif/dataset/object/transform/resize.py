from dataclasses import dataclass

import numpy as np

from poif.dataset.object.transform.base import DataTransform
from poif.utils import ResizeMethod, resize_img


@dataclass
class Resize(DataTransform):
    width: int
    height: int
    resize_method: ResizeMethod = ResizeMethod.PAD

    def __post_init__(self):
        self.supported_type = np.ndarray

    def transform(self, input_object: np.ndarray) -> np.ndarray:
        return resize_img(input_object, new_height=self.height, new_width=self.width, resize_method=self.resize_method)

    def get_tag(self) -> str:
        return f"rsz{self.width}{self.height}m{self.resize_method}"
