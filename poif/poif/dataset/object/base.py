from typing import Any, Dict, List, Optional

import numpy as np

from poif.dataset.object.annotations import DataSetAnnotation
from poif.dataset.object.data_transform.base import DataTransform
from poif.dataset.object.meta_info import MetaInfoMixin
from poif.tagged_data.base import TaggedData, TaggedPassthrough


class DataSetObject(TaggedPassthrough, MetaInfoMixin):
    def __init__(self, tagged_data: TaggedData):
        super().__init__(tagged_data)

        self.annotations: List[DataSetAnnotation] = []
        self.named_annotations: Dict[str, DataSetAnnotation] = {}

        self.future_transforms: List[DataTransform] = []

    def output(self) -> Any:
        parsed_output = self.get_parsed()
        return parsed_output


class TransformedDataSetObject(DataSetObject):
    def __init__(self, tagged_data: TaggedData, transformation: DataTransform):
        super().__init__(tagged_data)
        self.transformation = transformation

    def tag(self):
        parent_tag = super().tag

        return f"{parent_tag} - {self.transformation.tag}"

    def get_parsed(self) -> Any:
        parent_parsed = self.get_parsed()
        return self.transformation(parent_parsed)


class Image(DataSetObject):
    def __init__(self, tagged_data: TaggedData, width: Optional[int] = None, height: Optional[int] = None):
        super().__init__(tagged_data)

        self._height = height
        self._width = width

    def set_wh_from_data(self):
        np_img = self.get_parsed()

        assert isinstance(np_img, np.ndarray)
        if len(np_img.shape) == 3:
            h, w, c = np_img.shape
        elif len(np_img.shape) == 2:
            h, w = np_img.shape
        else:
            raise Exception("Image dimension not as expected. Expected 2 or 3 values in image shape.")

        self._width = w
        self._height = h

    @property
    def width(self) -> int:
        if self._width is None:
            self.set_wh_from_data()
        return self._width

    @property
    def height(self) -> int:
        if self._height is None:
            self.set_wh_from_data()
        return self._height


class ClassificationInput(DataSetObject):
    def output(self):
        return self.get_parsed(), self.label
