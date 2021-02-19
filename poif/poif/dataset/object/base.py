from typing import Any, Dict, List, Optional

import numpy as np

from poif.cache.base import CacheManager
from poif.dataset.object.annotations import DataSetAnnotation
from poif.dataset.object.data_transform.base import DataTransform
from poif.dataset.object.meta_info import MetaInfoMixin
from poif.dataset.object.output import DataSetObjectOutputFunction
from poif.tagged_data.base import TaggedData, TaggedPassthrough


class DataSetObject(TaggedPassthrough, MetaInfoMixin):
    def __init__(
        self,
        tagged_data: TaggedData,
        output_function: Optional[DataSetObjectOutputFunction] = None,
        cache: bool = True,
        cache_manager: Optional[CacheManager] = None,
    ):
        super().__init__(tagged_data)

        self.annotations: List[DataSetAnnotation] = []
        self.named_annotations: Dict[str, DataSetAnnotation] = {}

        self.future_transforms: List[DataTransform] = []

        self.output_function = output_function

        self.cache = cache
        self.cache_manager = cache_manager

        self._height: Optional[int] = None
        self._width: Optional[int] = None

    def output(self) -> Any:
        if self.output_function is not None:
            return self.output_function(self)

        parsed_output = self.get_parsed()
        return parsed_output

    def get(self) -> bytes:
        if self.cache_manager is not None and self.cache:
            cache_content = self.cache_manager.get(self.tag)
            if cache_content is None:
                parsed_content = self.parse_file(super(DataSetObject, self).get(), self.extension)
                self.cache_manager.write(parsed_content=parsed_content, tag=self.tag, extension=self.extension)

            cache_content = self.cache_manager.get(self.tag)
            if cache_content is not None:
                return cache_content
            raise Exception("Caching failed")

        return super(DataSetObject, self).get()

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

    def add_annotation(self, annotation: DataSetAnnotation):
        self.annotations.append(annotation)


class TransformedDataSetObject(DataSetObject):
    def __init__(
        self, tagged_data: TaggedData, transformation: DataTransform, output_function: DataSetObjectOutputFunction
    ):
        super().__init__(tagged_data, output_function=output_function)
        self.transformation = transformation

    def tag(self):
        parent_tag = super().tag

        return f"{parent_tag} - {self.transformation.tag}"

    def get_parsed(self) -> Any:
        parent_parsed = self.get_parsed()
        return self.transformation(parent_parsed)
