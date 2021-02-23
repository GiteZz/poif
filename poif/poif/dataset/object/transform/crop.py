from dataclasses import dataclass

import numpy as np

from poif.dataset.object.transform.base import DataTransform


@dataclass
class Crop(DataTransform):
    x: int
    y: int
    w: int
    h: int

    def __post_init__(self):
        self.supported_type = np.ndarray

    def transform(self, input_object: np.ndarray) -> np.ndarray:
        return input_object[self.y : self.y + self.h, self.x : self.x + self.w]

    def get_tag(self) -> str:
        return f"crp{self.x}{self.y}{self.w}{self.h}"
