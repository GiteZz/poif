from typing import Optional, Callable, List
from poif.base_classes import Parameters, DataQuery, Experiment, Output, RunEnvironment


def run(
        experiment_name: str,
        entry_point: Callable[[Experiment], Output],
        default_parameters: Parameters,
        default_data_query: DataQuery,
        test_run: Experiment,
        experiments: List[Experiment],
        run_environment: RunEnvironment):
    pass