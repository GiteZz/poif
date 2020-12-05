from dataclasses import dataclass, field
from typing import Dict, Any, List, Union
from pathlib import Path

# from poif.project_interface.base_classes.transform import Transform
from poif.project_interface.base_classes.location import DataLocation


class Input:
    meta_data = None
    future_transforms = None
    data_locations = {}

    def __init__(self, meta_data: Dict, future_transforms: List[Any]=None, data_locations: Union[DataLocation, Dict[str, DataLocation]] = None):
        self.meta_data = meta_data
        self.future_transforms = future_transforms
        self.data_locations = data_locations

    def __getattr__(self, item):
        print(f'get short {item}')
        if item == 'data':
            if isinstance(self.data_locations, DataLocation):
                return self.data_locations
            else:
                return DictToClass(self)
        else:
            return self.meta_data[item]

    def __setattr__(self, key, value):
        if hasattr(self, key):
            print(f'Existing attribute key: {key}, value: {value}')
            super(Input, self).__setattr__(key, value)
            return
        print(f'set short {key} {value}')
        if 'item' == 'data':
            self.data_locations = value
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
            print(f'Existing attribute key: {key}, value: {value}')
            super(DictToClass, self).__setattr__(key, value)
            return
        if self.input.data_locations is None:
            self.input.data_locations = {}
        self.input.data_locations[key] = value
