from poif.base_classes.parameters import Parameters
from dataclasses import dataclass
from typing import List
from poif.operations.combine import combine_parameters, combine_data_queries, combine_experiments


def test_parameters():
    @dataclass
    class TestParameters(Parameters):
        value: int = None
        name: str = None
        dependencies: List[str] = None
        tag: str = None

    base_parameters = TestParameters(value=5, name='base_test', dependencies=['a', 'b'], tag='aa')
    override_parameters = TestParameters(value=3, name='overrride_test')

    new_parameters = combine_parameters(base_parameters, override_parameters)

    assert new_parameters.value == override_parameters.value
    assert new_parameters.name == override_parameters.name
    assert new_parameters.dependencies == base_parameters.dependencies
    assert new_parameters.tag == base_parameters.tag

    assert base_parameters.value == 5
    assert base_parameters.name == 'base_test'
    assert base_parameters.dependencies == ['a', 'b']
    assert base_parameters.tag == 'aa'