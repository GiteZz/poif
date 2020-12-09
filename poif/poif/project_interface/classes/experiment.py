from dataclasses import dataclass
from typing import Callable, List, Set
from poif.project_interface.classes.parameters import Parameters
from poif.project_interface.classes.output import Output
from poif.project_interface.classes.resource import Resource
from poif.project_interface.classes.data import DataQuery


# Should provide functions for accessing the data
@dataclass
class Experiment:
    name: str = None
    parameters: Parameters = None
    entry_point: Callable[['Experiment'], Output] = None
    data_query: DataQuery = None
    external_resources: Set[Resource] = None