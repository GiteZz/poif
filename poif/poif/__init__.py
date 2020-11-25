from typing import Optional, Callable, List

from poif.base_classes.experiment import Experiment
from poif.base_classes.parameters import Parameters
from poif.base_classes.output import Output
from poif.base_classes.resource import Resource
from poif.base_classes.data_query import DataQuery
from poif.base_classes.run_environment import RunEnvironment

def run(run_name: str,
        test_experiment: Experiment,
        default_experiment: Experiment,
        experiments: List[Experiment],
        run_environment: RunEnvironment):
    pass