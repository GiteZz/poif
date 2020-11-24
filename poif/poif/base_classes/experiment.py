from dataclasses import dataclass
from typing import Callable
from poif.base_classes import Parameters


# Should provide functions for accessing the data
@dataclass
class Experiment:
    parameters: Parameters
    entry_point: Callable