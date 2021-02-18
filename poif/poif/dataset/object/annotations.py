from abc import ABC, abstractmethod
from typing import List, Optional, Union

from poif.dataset.object.meta_info import MetaInfoMixin
from poif.tagged_data.base import TaggedData, TaggedPassthrough


class DataSetAnnotation(MetaInfoMixin, ABC):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def output(self):
        pass


class Mask(TaggedPassthrough, DataSetAnnotation):
    def __init__(self, tagged_data: TaggedData):
        super().__init__(tagged_data)

    def output(self):
        if self.label is not None:
            return self.label, self.get_parsed()
        else:
            return self.get_parsed()


class Point(DataSetAnnotation):
    x: Optional[float] = None
    y: Optional[float] = None

    def output(self):
        return self.label, self.x, self.y


class BoundingBox(DataSetAnnotation):
    # TODO fix with inheritance such that the meta object values should not be used here
    def __init__(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        label: Optional[Union[str, int]] = None,
        tags: List[str] = None,
    ):
        super().__init__()
        self.label = label
        self.tags = tags

        self.x = x
        self.y = y
        self.w = w
        self.h = h

    def output(self):
        return [self.label] + self.as_list()

    def as_list(self) -> List[float]:
        return [self.x, self.y, self.w, self.h]

    def int_bbox(self, img_width, img_height) -> List[int]:
        return [
            int(self.x * img_width),
            int(self.y * img_height),
            int(self.w * img_width),
            int(self.h * img_height),
        ]

    def coco_bbox(self, img_width, img_height) -> list:

        int_bbox = self.int_bbox(img_width, img_height)
        return int_bbox

    def yolo_label(self):
        yolo_x = self.x + self.w / 2
        yolo_y = self.y + self.h / 2

        return f"{self.label} {yolo_x} {yolo_y} {self.w} {self.h}"
