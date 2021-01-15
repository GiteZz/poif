from typing import Any, Dict, List, Union

from poif.data.access.input import Input
from poif.data.transform.transform import (DataPointSplitter,
                                           DataPointTransformation,
                                           DataSetSplitter, DataSetTransformation,
                                           OutputFilter)

SplitterType = Union[DataPointSplitter, DataSetSplitter]
TransformationType = Union[DataPointTransformation, DataSetTransformation]


class BaseDataset:
    def __init__(self,
                 inputs: List[Input],
                 output_filter: OutputFilter = None):

        self.inputs = inputs
        self.output_filter = output_filter

    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, idx) -> Any:
        input_item = self.inputs[idx]

        if self.output_filter is not None:
            return self.output_filter(input_item)
        else:
            return input_item


class Dataset(BaseDataset):
    def __init__(self,
                 inputs: List[Input],
                 dataset_splits: Dict[str, List[Input]] = None,
                 output_filter=None
                 ):

        # Make sure self.metadata_processors is always a list.
        super().__init__(inputs, output_filter)
        self.dataset_splits = dataset_splits
        self.output_filter = output_filter

    def __getattr__(self, item):
        try:
            if item in self.dataset_splits:
                return BaseDataset(self.dataset_splits[item], output_filter=self.output_filter)
            else:
                raise AttributeError()
        except:
            raise AttributeError()