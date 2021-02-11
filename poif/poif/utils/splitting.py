import random
from collections import defaultdict
from typing import Any, Dict, List

from poif.typing import SubSetName


def random_split(objects: List[Any], percentage_dict: Dict[SubSetName, float]):
    key_ordening = list(percentage_dict.keys())

    max_gates = list(percentage_dict.values())

    for gate_index in range(1, len(max_gates)):
        max_gates[gate_index] += max_gates[gate_index - 1]

    max_gates.insert(0, 0.0)

    split_dict = defaultdict(list)

    for current_object in objects:
        random_value = random.random()

        for index, key in enumerate(key_ordening):
            # double <= is strictly not correct but at least insures that all values are included
            if max_gates[index] <= random_value <= max_gates[index + 1]:
                split_dict[key].append(current_object)

    return split_dict
