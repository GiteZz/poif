from dataclasses import dataclass
from typing import List

from poif.dataset.object.annotations import Mask
from poif.dataset.object.base import DataSetObject
from poif.dataset.operation.transform.base import Transformation
from poif.typing import PathTemplate
from poif.utils.template import extract_values, is_path_match


@dataclass
class MaskTemplate:
    mask: PathTemplate
    image: PathTemplate


class MaskByTemplate(Transformation):
    def __init__(self, template: MaskTemplate):
        self.template = template

    def is_mask_match(self, relative_path: str) -> bool:
        return is_path_match(self.template.mask, relative_path)

    def is_image_match(self, relative_path: str) -> bool:
        return is_path_match(self.template.image, relative_path)

    def __call__(self, dataset: List[DataSetObject]) -> List[DataSetObject]:
        images = {}
        masks = {}
        for ds_input in dataset:
            if self.is_mask_match(ds_input.relative_path):
                values = extract_values(template=self.template.mask, path=ds_input.relative_path)
                hashable_values = tuple(sorted(values.items()))
                masks[hashable_values] = ds_input
            elif self.is_image_match(ds_input.relative_path):
                values = extract_values(template=self.template.image, path=ds_input.relative_path)
                hashable_values = tuple(sorted(values.items()))
                images[hashable_values] = ds_input
            else:
                print(f"WARNING: item with path: {ds_input.relative_path} was not matched")

        new_inputs = []
        for intersected_values in set.intersection(set(images.keys()), set(masks.keys())):
            mask_input = masks[intersected_values]
            image_input = images[intersected_values]

            image_input.annotations.append(Mask(mask_input))
            new_inputs.append(image_input)
        return new_inputs


class DropByTemplate(Transformation):
    def __init__(self, template: str):
        self.template = template

    def transform_single_object(self, ds_input: DataSetObject) -> List[DataSetObject]:
        if is_path_match(self.template, ds_input.relative_path):
            return []
        else:
            return [ds_input]


class ClassificationByTemplate(Transformation):
    def __init__(self, template: str, input_item="label", drop_if_no_match=True):
        self.template = template
        self.input_item = input_item
        self.drop_if_no_match = drop_if_no_match

    def transform_single_object(self, ds_input: DataSetObject) -> List[DataSetObject]:
        values = extract_values(template=self.template, path=ds_input.relative_path)
        if self.input_item in values:
            label = values[self.input_item]

            ds_input.label = label

            return [ds_input]
        elif self.drop_if_no_match:
            return []
        else:
            return [ds_input]
