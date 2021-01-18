from collections import defaultdict
from dataclasses import dataclass
from typing import Dict, List, Union

from poif.input.base import Input
from poif.input.classification import ClassificationInput
from poif.input.detection import DetectionInput
from poif.input.mask import MaskInput
from poif.input.tagged_data import TaggedDataInput
from poif.input.transform.tools import extract_values, catch_all_to_value, is_path_match
from poif.input.transform.base import Transformation
from poif.typing import PathTemplate, SubSetName


@dataclass
class MaskTemplate:
    mask: PathTemplate
    image: PathTemplate


class MaskByTemplate(Transformation):
    def __init__(self, template: MaskTemplate):
        self.template = template

    def __call__(self, dataset: List[TaggedDataInput]) -> List[MaskInput]:

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
            new_inputs.append(MaskInput(mask=masks[values].tagged_data, image=images[values].tagged_data))
        return new_inputs


class DropByTemplate(Transformation):
    def __init__(self, template: str):
        self.template = template

    def transform_single_input(self, ds_input: TaggedDataInput) -> List[Input]:
        if is_path_match(self.template, ds_input.relative_path):
            return []
        else:
            return [ds_input]


class ClassificationByTemplate(Transformation):
    def __init__(self, template: str, input_item='label'):
        self.template = template
        self.input_item = input_item

    def transform_single_input(self, ds_input: TaggedDataInput) -> List[Input]:
        values = extract_values(template=self.template, path=ds_input.relative_path)
        label = values[self.input_item]

        return [ClassificationInput(tagged_data=ds_input.tagged_data, label=label)]
