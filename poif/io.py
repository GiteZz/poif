from dataclasses import dataclass
from typing import Dict, List, Tuple


ImageHash: str
Label: str


@dataclass
class Experiment:
    experiment_name: str
    git_hash: str
    parameters: 'Parameters'
    data_query: 'DataQuery'


@dataclass
class Input:
    pass


@dataclass
class Output:
    run_time: float = None


@dataclass
class ClassificationOutput(Output):
    result: List[Tuple[ImageHash, Label, List[Label]]]


@dataclass
class Parameters:
    pass


@dataclass
class DataQuery:
    pass


@dataclass
class Sample:
    file_hash: ImageHash
    meta_data: Dict
