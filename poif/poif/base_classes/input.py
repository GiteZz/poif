from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class MetaInput:
    name: str
    meta_data: Dict


@dataclass
class DataInput(MetaInput):
    data: Any = None
    tag: str = None  # TODO check moment of calculation
