from abc import ABC, abstractmethod
from dataclasses import field
from typing import Dict, List, Optional

from poif.input.annotations import DataSetAnnotation
from poif.input.meta_info import MetaInfoMixin
from poif.tagged_data.base import TaggedData, TaggedPassthrough


class DataSetObject(TaggedPassthrough, MetaInfoMixin, ABC):
    name: Optional[str] = None
    annotations: List[DataSetAnnotation] = field(default_factory=list)
    named_annotations: Dict[str, DataSetAnnotation] = field(default_factory=dict)

    def __init__(self, tagged_data: TaggedData):
        super().__init__(tagged_data)

    @abstractmethod
    def output(self):
        pass


class Image(DataSetObject, ABC):
    def __init__(self, tagged_data: TaggedData, width: Optional[int] = None, height: Optional[int] = None):
        super().__init__(tagged_data)

        self.height = height
        self.width = width


class ClassificationInput(DataSetObject):
    def output(self):
        return self.get_parsed(), self.label
