from abc import ABC, abstractmethod
from typing import List

from attr import dataclass

from poif.input.meta_info import MetaInfoMixin
from poif.tagged_data.base import TaggedData


class DataSetAnnotation(MetaInfoMixin, ABC):
    @abstractmethod
    def output(self):
        pass


@dataclass
class Mask(DataSetAnnotation):
    data: TaggedData = None

    def output(self):
        return self.label, self.data.get_parsed()


class Point(DataSetAnnotation):
    x: float = None
    y: float = None

    def output(self):
        return self.label, self.x, self.y


class BoundingBox(DataSetAnnotation):
    # TODO fix with inheritance such that the meta input values should not be used here
    def __init__(self, x: float, y: float, w: float, h: float, label: str = None, tags: List[str] = None):
        super().__init__(label=label, tags=tags)

        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def output(self):
        return [self.label] + self.as_list()

    def as_list(self) -> List[float]:
        return [self.x, self.y, self.w, self.h]

    def int_bbox(self, img_width, img_height) -> List[int]:
        return [int(self.x * img_width), int(self.y * img_height), int(self.w * img_width), int(self.h * img_height)]

    def coco_bbox(self, img_width, img_height) -> str:

        int_bbox = self.int_bbox(img_width, img_height)
        return ' '.join(str(value) for value in int_bbox)