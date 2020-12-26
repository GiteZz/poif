from dataclasses import dataclass
from typing import Callable, Dict, List, Set

from poif.project_interface.classes.data import DataQuery
from poif.project_interface.classes.output import Output
from poif.project_interface.classes.parameters import Parameters
from poif.project_interface.classes.resource import Resource

EntryPoint = Callable[['Experiment'], Output]

# Should provide functions for accessing the data
@dataclass
class Experiment:
    name: str = None
    parameters: Parameters = None
    entry_point: EntryPoint = None
    data_query: DataQuery = None
    external_resources: Dict[str, Resource] = None