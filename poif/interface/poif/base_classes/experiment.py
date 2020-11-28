from dataclasses import dataclass
from typing import Callable, List, Set
from poif.base_classes.parameters import Parameters
from poif.base_classes.output import Output
from poif.base_classes.resource import Resource
from poif.base_classes.data_query import DataQuery


# Should provide functions for accessing the data
@dataclass
class Experiment:
    name: str = None
    parameters: Parameters = None
    entry_point: Callable[['Experiment'], Output] = None
    data_query: DataQuery = None
    external_resources: Set[Resource] = None