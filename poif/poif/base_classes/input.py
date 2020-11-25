from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class MetaInput:
    tag: str
    meta_data: Dict


@dataclass
class DataInput(MetaInput):
    data: Any = None
