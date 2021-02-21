from typing import Union

from poif.dataset.operation.meta_provider.base import MetaProvider
from poif.dataset.operation.selective import SelectiveSubsetOperation
from poif.dataset.operation.split.base import Splitter
from poif.dataset.operation.transform.base import Transformation
from poif.dataset.operation.transform_and_split.base import TransformAndSplit

Operation = Union[Transformation, Splitter, TransformAndSplit, MetaProvider, SelectiveSubsetOperation]
