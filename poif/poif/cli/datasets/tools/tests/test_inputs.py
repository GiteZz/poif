import pytest

from poif.cli.datasets.tools.cli import (MaxTriesReachedException,
                                         in_list_validation,
                                         input_with_possible_default,
                                         multi_input, yes)
from poif.tests import MonkeyPatchSequence


def test_monkey_patch_sequence(monkeypatch):
    input_returns = MonkeyPatchSequence(['tree', 'lamp'])
    monkeypatch.setattr('builtins.input', input_returns)

    assert input() == 'tree'
    assert input() == 'lamp'


def test_input_with_possible_default(monkeypatch):
    monkeypatch.setattr('builtins.input', lambda: '')
    assert input_with_possible_default(default='tree') == 'tree'

    monkeypatch.setattr('builtins.input', lambda: 'desk')
    assert input_with_possible_default() == 'desk'

    with pytest.raises(MaxTriesReachedException):
        input_with_possible_default(validation_function=lambda x: x == 'lamp')

    input_with_possible_default(validation_function=lambda x: x == 'desk')

    input_with_possible_default(validation_function=in_list_validation(['desk', 'fridge']))

    with pytest.raises(MaxTriesReachedException):
        input_with_possible_default(validation_function=in_list_validation(['tree', 'fridge']))

    input_returns = MonkeyPatchSequence(['lamp', 'tree'])
    monkeypatch.setattr('builtins.input', input_returns)
    assert input_with_possible_default(validation_function=in_list_validation(['tree', 'fridge'])) == 'tree'


def test_multi_input(monkeypatch):
    input_returns = MonkeyPatchSequence(['lamp', 'tree', ''])
    monkeypatch.setattr('builtins.input', input_returns)
    assert multi_input('TestTile') == ['lamp', 'tree']

    input_returns = MonkeyPatchSequence(['lamp', 'tree', ''])
    monkeypatch.setattr('builtins.input', input_returns)
    assert multi_input('TestTile', empty_allowed=True) == ['lamp', 'tree']

    input_returns = MonkeyPatchSequence(['', 'lamp', 'tree', ''])
    monkeypatch.setattr('builtins.input', input_returns)
    assert multi_input('TestTile', empty_allowed=True) == []

    input_returns = MonkeyPatchSequence(['', 'lamp', 'tree', ''])
    monkeypatch.setattr('builtins.input', input_returns)
    assert multi_input('TestTile', empty_allowed=False) == ['lamp', 'tree']

def test_yes(monkeypatch):
    valid_yesses = ['y', 'yes', 'YES', 'Y', 'YeS']
    for valid_yes in valid_yesses:
        monkeypatch.setattr('builtins.input', lambda: valid_yes)
        assert yes()

    valid_noos = ['n', 'no', 'NO', 'N', 'No']
    for valid_no in valid_noos:
        monkeypatch.setattr('builtins.input', lambda: valid_no)
        assert not yes()

    monkeypatch.setattr('builtins.input', lambda: '')
    assert yes(default=True)