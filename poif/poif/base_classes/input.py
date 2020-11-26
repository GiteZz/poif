from dataclasses import dataclass
from typing import Dict, Any, List, Union
from pathlib import Path

from poif.base_classes.transform import Transform


@dataclass
class MetaInput:
    data_loc: Union[Path]
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
