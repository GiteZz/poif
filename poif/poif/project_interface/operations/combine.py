from poif.project_interface.base_classes.experiment import Experiment
from poif.project_interface.base_classes.parameters import Parameters
from poif.project_interface.base_classes.data_query import DataQuery
from copy import deepcopy


def combine_experiments(base_experiment: Experiment, override_experiment: Experiment) -> Experiment:
    new_name = override_experiment.name if override_experiment is not None else base_experiment.name
    new_parameters = combine_parameters(base_experiment.parameters, override_experiment.parameters)
    new_data_query = combine_data_queries(base_experiment.data_query, override_experiment.data_query)

    if base_experiment.external_resources is None:
        new_resources = override_experiment.external_resources
    elif override_experiment.external_resources is not None:
        new_resources = set.union(base_experiment.external_resources, override_experiment.external_resources)
    else:
        new_resources = base_experiment.external_resources

    if override_experiment.entry_point is not None:
        new_entry_point = override_experiment.entry_point
    else:
        new_entry_point = base_experiment.entry_point

    return Experiment(name=new_name,
                      parameters=new_parameters,
                      data_query=new_data_query,
                      external_resources=new_resources,
                      entry_point=new_entry_point
                      )


def combine_parameters(base_parameters: Parameters, override_parameters: Parameters) -> Parameters:
    new_parameters = deepcopy(base_parameters)
    for param_name, param_value in vars(override_parameters).items():
        if param_value is not None:
            new_parameters.__dict__[param_name] = param_value

    return new_parameters


def combine_data_queries(base_query: DataQuery, overrride_query: DataQuery) -> DataQuery:
    pass

