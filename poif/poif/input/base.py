from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from poif.tagged_data.base import TaggedData
from typing import List


@dataclass
class DataSetObject:
    data: TaggedData = None
    objects: List['DataSetObject'] = field(default_factory=list)


class Image(DataSetObject):
    width: int = None
    height: int = None


class Point(DataSetObject):
    x: float = None
    y: float = None


class Rectangle(DataSetObject):
    x: float
    y: float
    w: float
    h: float


class Input(DataSetObject, ABC):
    @abstractmethod
    def output(self):
        pass