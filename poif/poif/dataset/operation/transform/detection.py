from typing import List

from poif.dataset.object.annotations import BoundingBox
from poif.dataset.object.base import DataSetObject, TransformedDataSetObject
from poif.dataset.object.output import classification_output
from poif.dataset.object.transform.crop import Crop
from poif.dataset.operation.transform.base import Transformation


class DetectionToClassification(Transformation):
    def transform_single_object(self, dataset_object: DataSetObject) -> List[DataSetObject]:
        new_objects = []
        for annotation in dataset_object.annotations:
            if isinstance(annotation, BoundingBox):
                transformation = Crop(
                    x=int(annotation.x * dataset_object.width),
                    y=int(annotation.y * dataset_object.height),
                    w=int(annotation.w * dataset_object.width),
                    h=int(annotation.h * dataset_object.height),
                )
                new_object = TransformedDataSetObject(
                    dataset_object, transformation, output_function=classification_output
                )
                new_object.label = annotation.label
                new_objects.append(new_object)
        return new_objects
