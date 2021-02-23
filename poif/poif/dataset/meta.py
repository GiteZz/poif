from dataclasses import dataclass, fields
from typing import Dict, Optional

import numpy as np


@dataclass
class MetaCollection:
    index_to_label: Optional[Dict[int, str]] = None
    label_to_index: Optional[Dict[str, int]] = None
    normalisation: Optional[np.ndarray] = None

    def __add__(self, other: "MetaCollection") -> "MetaCollection":
        new_collection = MetaCollection()
        field_names = [field.name for field in fields(self)]
        for field_name in field_names:
            first_value = getattr(self, field_name)
            second_value = getattr(other, field_name)

            if first_value is None and second_value is None:
                new_value = None
            elif first_value is not None and second_value is None:
                new_value = first_value
            elif second_value is not None and first_value is None:
                new_value = second_value
            else:
                new_value = first_value

            setattr(new_collection, field_name, new_value)

        return new_collection
