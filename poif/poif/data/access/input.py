from dataclasses import dataclass
from typing import Any, Dict, List, Union


class Input:
    meta_data = None
    future_transforms = None

    def __init__(self, meta_data: Dict, future_transforms: List[Any]=None):
        self.meta_data = meta_data
        self.future_transforms = future_transforms

    def __getattr__(self, item):
        try:
            return self.meta_data[item]
        except:
            raise AttributeError()

    def __setattr__(self, key, value):
        if hasattr(self, key):
            super(Input, self).__setattr__(key, value)
            return
        else:
            self.meta_data[key] = value


@dataclass
class DictToClass:
    input = None

    def __init__(self, or_input: Input):
        self.input = or_input

    def __getattr__(self, item):
        try:
            return self.input.data_locations[item]
        except:
            raise AttributeError('')

    def __setattr__(self, key, value):
        if hasattr(self, key):
            super(DictToClass, self).__setattr__(key, value)
            return
        if self.input.data_locations is None:
            self.input.data_locations = {}
        self.input.data_locations[key] = value
