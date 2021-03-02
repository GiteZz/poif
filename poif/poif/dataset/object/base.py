from typing import Any, Dict, List, Optional, Tuple

import numpy as np

from poif.cache.base import CacheManager
from poif.dataset.object.annotations import DataSetAnnotation
from poif.dataset.object.meta_info import MetaInfoMixin
from poif.dataset.object.output import DataSetObjectOutputFunction
from poif.dataset.object.transform.base import DataTransform
from poif.tagged_data.base import TaggedData, TaggedPassthrough


class DataSetObject(TaggedPassthrough, MetaInfoMixin):
    """
    A DataSetObject is essentially a TaggedData object with additional meta information. On piece of additional meta
    is the addition of a label and tags. These attributes don't have to have a value and are initiated as None. The
    other additional meta_information is the annotation list. An annotation could be anything but a the moment
    common objects such as a BoundingBox, Point etc. are provided. These two additional types of information allow
    for transforming a piece of data into a useful dataset object.

    The class also defines the output function, this function takes as input the object itself and then returns
    how it should be presented. An example of this is the classification output which return the parsed data and
    the associated label combined in a tuple.
    """

    def __init__(
        self,
        tagged_data: TaggedData,
        output_function: Optional[DataSetObjectOutputFunction] = None,
    ):
        super().__init__(tagged_data)

        self.annotations: List[DataSetAnnotation] = []
        self.named_annotations: Dict[str, DataSetAnnotation] = {}

        self.output_function = output_function

        self.cache_manager: Optional[CacheManager] = None

        self._height: Optional[int] = None
        self._width: Optional[int] = None

    def output(self) -> Any:
        if self.output_function is not None:
            return self.output_function(self)

        parsed_output = self.get_parsed()
        return parsed_output

    def add_cache_manager(self, cache_manager: CacheManager):
        self.cache_manager = cache_manager

    def get(self) -> bytes:
        if self.cache_manager is not None:
            cache_content = self.cache_manager.get(self.tag)
            if cache_content is None:
                parsed_content = self.parse_file(super(DataSetObject, self).get(), self.extension)
                self.cache_manager.write(parsed_content=parsed_content, tag=self.tag, extension=self.extension)

            cache_content = self.cache_manager.get(self.tag)
            if cache_content is not None:
                return cache_content
            raise Exception("Caching failed")

        return super(DataSetObject, self).get()

    def set_wh_from_data(self) -> Tuple[int, int]:
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

        return w, h

    @property
    def width(self) -> int:
        if self._width is None:
            w, _ = self.set_wh_from_data()
        else:
            w = self._width
        return w

    @property
    def height(self) -> int:
        if self._height is None:
            _, h = self.set_wh_from_data()
        else:
            h = self._height
        return h

    def add_annotation(self, annotation: DataSetAnnotation):
        self.annotations.append(annotation)


class TransformedDataSetObject(DataSetObject):
    """
    This class is a DataSetObject with an added transformation. This means that this class has a pointer to
    its parent_object. When the get_parsed() function is called the parent is parsed and then the operation is
    executed on that parsed parent. An example of this is transforming a detection dataset to a classification
    dataset. In this example the parent would be the original detection image and the transformation would be
    the crop.
    """

    def __init__(
        self, parent_object: DataSetObject, transformation: DataTransform, output_function: DataSetObjectOutputFunction
    ):
        # TODO fix the duplication, ideally DataSetObject should not be TaggedData but keep some the interface
        super().__init__(parent_object, output_function=output_function)
        self.parent_object = parent_object
        self.transformation = transformation

    def tag(self):
        parent_tag = super().tag

        return f"{parent_tag} - {self.transformation.tag}"

    def get_parsed(self) -> Any:
        parent_parsed = super().get_parsed()
        return self.transformation(parent_parsed)

    def add_cache_manager(self, cache_manager: CacheManager):
        super().add_cache_manager(cache_manager)
        self.parent_object.add_cache_manager(cache_manager)
