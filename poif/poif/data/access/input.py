from dataclasses import dataclass
from typing import Any, Dict, List, Union


class Input(dict):
    meta_data = None
    future_transforms = None

    def __init__(self, meta_data: dict = None):
        super().__init__()
        if meta_data is not None:
            for key, value in meta_data.items():
                self[key] = value

    def __getattr__(self, item):
        try:
            return self[item]
        except:
            raise AttributeError()

    def __setattr__(self, key, value):
        self[key] = value


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
