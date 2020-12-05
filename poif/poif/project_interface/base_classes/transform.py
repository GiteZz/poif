from dataclasses import dataclass, field
from pathlib import Path
import requests

from typing import List, Tuple, Union, Callable, Dict, Any, Optional
from poif.project_interface.base_classes.input import Input
from poif.project_interface.data_handlers.disk_loader.gather_functions import file_gatherer
from poif.typing import FileHash, RelFilePath
from poif.project_interface.base_classes.location import HttpLocation

ZeroOrMoreMetaInput = Optional[Union[Input, List[Input]]]
CallableDataPointTransformation = Callable[[Input], ZeroOrMoreMetaInput]
CallableDataSetTransformation = Callable[[List[Input]], List[Input]]


# Used for splitting the dataset, used for train/val/test split
CallableDataSetSplitter = Callable[[List[Input]], Dict[str, List[Input]]]
CallableDataPointSplitter = Callable[[Input], str]

Transform = Any


class DataSetSplitter:
    def __init__(self, split_function: CallableDataSetSplitter):
        self.function = split_function

    def __call__(self, dataset: List[Input]) -> Dict[str, List[Input]]:
        return self.function(dataset)


class DataPointSplitter:
    def __init__(self, split_function: CallableDataPointSplitter):
        self.function = split_function

    def __call__(self, datapoint: Input) -> str:
        return self.function(datapoint)


class DataPointTransformation:
    def __init__(self, transformation: CallableDataPointTransformation):
        self.function = transformation

    def __call__(self, datapoint: Input) -> Union[Input, List[Input]]:
        return self.function(datapoint)


class DataSetTransformation:
    def __init__(self, transformation: CallableDataSetTransformation):
        self.function = transformation

    def __call__(self, dataset: List[Input]) -> List[Input]:
        return self.function(dataset)
