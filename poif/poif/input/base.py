from typing import Any, Dict, List, Optional

from poif.input.annotations import DataSetAnnotation
from poif.input.meta_info import MetaInfoMixin
from poif.tagged_data.base import TaggedData, TaggedPassthrough


class DataSetObject(TaggedPassthrough, MetaInfoMixin):
    def __init__(self, tagged_data: TaggedData):
        super().__init__(tagged_data)

        self.annotations: List[DataSetAnnotation] = []
        self.named_annotations: Dict[str, DataSetAnnotation] = {}

    def output(self) -> Any:
        parsed_output = self.get_parsed()
        return parsed_output


class Image(DataSetObject):
    def __init__(self, tagged_data: TaggedData, width: Optional[int] = None, height: Optional[int] = None):
        super().__init__(tagged_data)

        self.height = height
        self.width = width


class ClassificationInput(DataSetObject):
    def output(self):
        return self.get_parsed(), self.label
