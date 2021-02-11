from typing import List, Union

from poif.dataset.base import BaseDataset, MultiDataset
from poif.input.base import DataSetObject
from poif.input.split.base import Splitter
from poif.input.tagged_data import TaggedDataInput
from poif.input.transform.base import Transformation
from poif.tagged_data.base import TaggedData

Operation = Union[Transformation, Splitter]


class TaggedDataDataset(MultiDataset):
    def __init__(self, operations: List[Operation] = None):

        self.operations = operations
        self.inputs = None
        self.splits = {}

    def form(self, data: List[TaggedData]):
        inputs = self.get_inputs(data)
        self.form_from_inputs(inputs)

    def form_from_inputs(self, inputs: List[DataSetObject]):
        self.inputs = inputs
        self.next_operation()

    def next_operation(self):
        if self.operations is None or len(self.operations) == 0:
            return
        current_operation = self.operations.pop(0)
        self.apply_operation(current_operation)

    def apply_operation(self, operation: Operation):
        if self.is_splitter(operation):
            self.apply_splitter(operation)
        elif self.is_tranformation(operation):
            self.apply_transformation(operation)
        else:
            raise Exception("Unknown type of operation")
        self.next_operation()

    def is_splitter(self, operation: Operation) -> bool:
        return isinstance(operation, Splitter)

    def is_tranformation(self, operation: Operation) -> bool:
        return isinstance(operation, Transformation)

    def apply_splitter(self, splitter: Splitter):
        splitter_dict = splitter(self.inputs)

        self.add_splitter_dict(splitter_dict)

    def add_splitter_dict(self, splitter_dict):
        for subset_name, inputs in splitter_dict.items():
            new_dataset = TaggedDataDataset(operations=self.operations)
            new_dataset.form_from_inputs(inputs)

            self.splits[subset_name] = new_dataset

    def apply_transformation(self, transformation: Transformation):
        self.inputs = transformation(self.inputs)

    def get_inputs(self, data: List[TaggedData]) -> List[DataSetObject]:
        return [TaggedDataInput(tagged_data) for tagged_data in data]

    def get_sub_dataset(self, key: str) -> BaseDataset:
        return self.splits[key]

    @property
    def available_sub_datasets(self):
        if self.splits is None:
            return []
        else:
            return list(self.splits.keys())

    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, idx: int):
        return self.inputs[idx].output()
