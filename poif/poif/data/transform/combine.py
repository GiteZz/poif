from collections import defaultdict
from typing import Dict, List, Union

from poif.data.access.input import Input
from poif.data.transform.tools import extract_values, catch_all_to_value, is_path_match
from poif.data.transform.base import DataSetTransformation, DataPointSplitter, DataPointTransformation
from poif.typing import path_template


class CombineByTemplate(DataSetTransformation):
    def __init__(self, match_templates: Dict[str, path_template], input_item='relative_path'):
        self.match_templates = match_templates
        self.input_item = input_item

    def __call__(self, dataset: List[Input]) -> List[Input]:
        value_templates = {template_name: catch_all_to_value(template)
                           for template_name, template in self.match_templates.items()
                           }
        value_bins = defaultdict(dict)
        for ds_input in dataset:
            for template_name, template in value_templates.items():
                if not is_path_match(template, ds_input[self.input_item]):
                    continue
                values = extract_values(template=template, path=ds_input[self.input_item])
                hashable_values = tuple(sorted(values.items()))
                value_bins[hashable_values][template_name] = ds_input

        new_inputs = []
        for bin in value_bins.values():
            new_input = Input()
            for template_name, template_input in bin.items():
                new_input[template_name] = template_input
            new_inputs.append(new_input)

        return new_inputs


class SplitByTemplate(DataPointSplitter):
    def __init__(self, template: str, input_item='relative_path', subset_tag='subset'):
        self.template = template
        self.input_item = input_item
        self.subset_tag = subset_tag

    def __call__(self, datapoint: Input) -> str:
        values = extract_values(self.template, datapoint[self.input_item])
        return values[self.subset_tag]


class DropByTemplate(DataPointTransformation):
    def __init__(self, template: str, input_item='relative_path'):
        self.template = template
        self.input_item = input_item

    def __call__(self, datapoint: Input) -> Union[Input, List[Input]]:
        if is_path_match(self.template, datapoint[self.input_item]):
            return []
        else:
            return datapoint