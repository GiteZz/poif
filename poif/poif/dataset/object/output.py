from typing import TYPE_CHECKING, Any, Callable, List, Tuple, Union

import numpy as np

from poif.dataset.object.annotations import Mask

if TYPE_CHECKING:
    from poif.dataset.object.base import DataSetObject

DataSetObjectOutputFunction = Callable[["DataSetObject"], Any]


def classification_output(ds_object: "DataSetObject") -> Tuple[Any, Union[str, int]]:
    return ds_object.get_parsed(), ds_object.label


def single_mask_output(ds_object: "DataSetObject") -> Tuple[Any, np.ndarray]:
    assert len(ds_object.annotations) == 1
    assert isinstance(ds_object.annotations[0], Mask)

    return ds_object.get_parsed(), ds_object.annotations[0].output()


def detection_output(ds_object: "DataSetObject") -> Tuple[Any, List[int]]:
    return ds_object.get_parsed(), [annotation.output() for annotation in ds_object.annotations]
