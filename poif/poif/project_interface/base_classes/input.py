from dataclasses import dataclass
from typing import Dict, Any, List, Union
from pathlib import Path

from poif.project_interface.base_classes.transform import Transform
from poif.project_interface.base_classes.location import DataLocation


@dataclass
class MetaInput:
    data_loc: DataLocation
    tag: str
    meta_data: Dict
    future_transforms: List[Transform] = None

    def __getattr__(self, item):
        return self.meta_data[item]

    def __setattr__(self, key, value):
        self.meta_data[key] = value


@dataclass
class DataInput(MetaInput):
    data: Any = None
