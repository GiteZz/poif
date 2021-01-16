from abc import ABC, abstractmethod
from typing import Any, Callable, Dict, List, Optional, Union

from poif.data.access.input import Input

ZeroOrMoreMetaInput = Optional[Union[Input, List[Input]]]
CallableDataPointTransformation = Callable[[Input], ZeroOrMoreMetaInput]
CallableDataSetTransformation = Callable[[List[Input]], List[Input]]


# Used for splitting the dataset, used for train/val/test split
CallableDataSetSplitter = Callable[[List[Input]], Dict[str, List[Input]]]
CallableDataPointSplitter = Callable[[Input], str]

CallableOutputFilter = Callable[[Input], Any]


class DataSetSplitter:
    @abstractmethod
    def __call__(self, dataset: List[Input]) -> Dict[str, List[Input]]:
        pass


class MethodDataSetSplitter(DataSetSplitter):
    def __init__(self, split_function: CallableDataSetSplitter):
        self.function = split_function

    def __call__(self, dataset: List[Input]) -> Dict[str, List[Input]]:
        return self.function(dataset)


class DataPointSplitter(ABC):
    @abstractmethod
    def __call__(self, datapoint: Input) -> str:
        pass


class MethodDataPointSplitter(DataPointSplitter):
    def __init__(self, split_function: CallableDataPointSplitter):
        self.function = split_function

    def __call__(self, datapoint: Input) -> str:
        return self.function(datapoint)


class DataPointTransformation:
    @abstractmethod
    def __call__(self, datapoint: Input) -> Union[Input, List[Input]]:
        pass


class MethodDataPointTransformation(DataPointTransformation):
    def __init__(self, transformation: CallableDataPointTransformation):
        self.function = transformation

    def __call__(self, datapoint: Input) -> Union[Input, List[Input]]:
        return self.function(datapoint)


class DataSetTransformation(ABC):
    @abstractmethod
    def __call__(self, dataset: List[Input]) -> List[Input]:
        pass


class MethodDataSetTransformation(DataSetTransformation):
    def __init__(self, transformation: CallableDataSetTransformation):
        self.function = transformation

    @abstractmethod
    def __call__(self, dataset: List[Input]) -> List[Input]:
        return self.function(dataset)


class OutputFilter:
    def __init__(self, filter: CallableOutputFilter):
        self.function = filter

    def __call__(self, datapoint: Input) -> Any:
        return self.function(datapoint)
