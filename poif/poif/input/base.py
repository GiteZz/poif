from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List

from poif.input.annotations import DataSetAnnotation
from poif.input.meta_info import MetaInfoMixin
from poif.tagged_data.base import TaggedData, TaggedPassthrough


class DataSetObject(TaggedPassthrough, MetaInfoMixin, ABC):
    name: str = None
    annotations: List[DataSetAnnotation] = field(default_factory=list)
    named_annotations: Dict[str, DataSetAnnotation] = field(default_factory=dict)

    def __init__(self, tagged_data: TaggedData):
        super().__init__(tagged_data)

    @abstractmethod
    def output(self):
        pass


@dataclass
class Image(DataSetObject, ABC):
    width: int = None
    height: int = None


class ClassificationInput(DataSetObject):
    def output(self):
        return self.get_parsed(), self.label
