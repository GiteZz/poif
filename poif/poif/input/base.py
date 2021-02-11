from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List

from poif.input.annotations import DataSetAnnotation
from poif.input.meta_info import MetaInfoMixin
from poif.tagged_data.base import TaggedData


@dataclass
class DataSetObject(MetaInfoMixin, ABC):
    data: TaggedData = None
    name: str = None
    annotations: List[DataSetAnnotation] = field(default_factory=list)
    named_annotations: Dict[str, DataSetAnnotation] = field(default_factory=dict)

    @abstractmethod
    def output(self):
        pass


@dataclass
class Image(DataSetObject, ABC):
    width: int = None
    height: int = None


class ClassificationInput(DataSetObject):
    def output(self):
        return self.data.get_parsed(), self.label
