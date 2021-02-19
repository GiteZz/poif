from typing import List

from poif.dataset.object.annotations import BoundingBox
from poif.dataset.object.base import DataSetObject, TransformedDataSetObject

# Used for splitting the dataset, used for train/val/test split
from poif.dataset.object.data_transform.crop import Crop
from poif.dataset.object.output import classification_output
from poif.dataset.operation.transform.base import Transformation


class DetectionToClassification(Transformation):
    def transform_single_object(self, dataset_object: DataSetObject) -> List[DataSetObject]:
        new_objects = []
        for annotation in dataset_object.annotations:
            if isinstance(annotation, BoundingBox):
                transformation = Crop(x=annotation.x, y=annotation.y, w=annotation.w, h=annotation.h)
                new_object = TransformedDataSetObject(
                    dataset_object, transformation, output_function=classification_output
                )
                new_object.label = annotation.label
                new_objects.append(new_object)
        return new_objects
