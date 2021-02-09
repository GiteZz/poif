from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Union

from poif.input.base import DataSetObject
from poif.input.annotations import Mask

from poif.input.mask import MaskInput
from poif.input.tagged_data import TaggedDataInput
from poif.input.transform.tools import extract_values, is_path_match
from poif.input.transform.base import Transformation
from poif.typing import PathTemplate


@dataclass
class MaskTemplate:
    mask: PathTemplate
    image: PathTemplate


class MaskByTemplate(Transformation):
    def __init__(self, template: MaskTemplate):
        self.template = template

    def __call__(self, dataset: List[TaggedDataInput]) -> List[DataSetObject]:

        images = {}
        masks = {}
        for ds_input in dataset:
            if is_path_match(self.template.mask, ds_input.relative_path):
                values = extract_values(template=self.template.mask, path=ds_input.relative_path)
                hashable_values = tuple(sorted(values.items()))
                masks[hashable_values] = ds_input
            elif is_path_match(self.template.image, ds_input.relative_path):
                values = extract_values(template=self.template.image, path=ds_input.relative_path)
                hashable_values = tuple(sorted(values.items()))
                images[hashable_values] = ds_input
            else:
                print(f'WARNING: item with path: {ds_input.relative_path} was not matched')

        new_inputs = []
        for values in set.intersection(set(images.keys()), set(masks.keys())):
            mask_input = DataSetObject(data=masks[values].data)
            mask_input.mask = Mask(data=images[values].data)
        return new_inputs


class DropByTemplate(Transformation):
    def __init__(self, template: str):
        self.template = template

    def transform_single_input(self, ds_input: TaggedDataInput) -> List[DataSetObject]:
        if is_path_match(self.template, ds_input.relative_path):
            return []
        else:
            return [ds_input]


class ClassificationByTemplate(Transformation):
    def __init__(self, template: str, input_item='label'):
        self.template = template
        self.input_item = input_item

    def transform_single_input(self, ds_input: TaggedDataInput) -> List[DataSetObject]:
        values = extract_values(template=self.template, path=ds_input.relative_path)
        label = values[self.input_item]

        return [DataSetObject(data=ds_input.data, label=label)]
