from poif.dataset.base import MultiDataset, BaseDataset
from collections import defaultdict

from typing import List, Union

from poif.dataset.base import SplitterType, TransformationType
from poif.input.base import Input
from poif.tagged_data.base import TaggedData
from poif.transform.base import (DataPointSplitter,
                                 DataPointTransformation,
                                 DataSetSplitter, DataSetTransformation)


Operation = Union[SplitterType, TransformationType]


class TaggedDataDataset(MultiDataset):
    def __init__(self,
                 operations: List[Operation] = None,
                 output_filter: OutputFilter = None):

        self.operations = operations
        self.output_filter = output_filter
        self.inputs = None
        self.splits = {}

    def form(self, data: List[TaggedData]):
        inputs = self.get_inputs(data)
        self.form_from_inputs(inputs)

    def form_from_inputs(self, inputs: List[Input]):
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
            raise Exception('Unknown type of operation')
        self.next_operation()

    def is_splitter(self, operation: Operation) -> bool:
        return isinstance(operation, DataSetSplitter) or isinstance(operation, DataPointSplitter)

    def is_tranformation(self, operation: Operation) -> bool:
        return isinstance(operation, DataPointTransformation) or isinstance(operation, DataSetTransformation)

    def apply_splitter(self, splitter: SplitterType):
        if isinstance(splitter, DataPointSplitter):
            splitter_dict = defaultdict(list)
            for input_item in self.inputs:
                splitter_dict[splitter(input_item)].append(input_item)
        elif isinstance(splitter, DataSetSplitter):
            splitter_dict = splitter(self.inputs)
        else:
            raise Exception('Unknown splitter type')

        self.add_splitter_dict(splitter_dict)

    def add_splitter_dict(self, splitter_dict):
        for subset_name, inputs in splitter_dict.items():
            new_dataset = TaggedDataDataset(operations=self.operations)
            new_dataset.form_from_inputs(inputs)

            self.splits[subset_name] = new_dataset

    def apply_transformation(self, transformation: TransformationType):
        if isinstance(transformation, DataPointTransformation):
            new_list = []
            for item in self.inputs:
                # The transformation can give back None, one or more meta inputs, therefore we have to
                # take different actions based on the format returned.
                new_item = transformation(item)
                if new_item is None:
                    continue
                if isinstance(new_item, list):
                    new_list.extend(new_item)
                else:
                    new_list.append(new_item)
            transformed_inputs = new_list

        elif isinstance(transformation, DataSetTransformation):
            transformed_inputs = transformation(self.inputs)
        else:
            raise Exception('Unknown type of transformation')

        self.inputs = transformed_inputs

    def get_inputs(self, data: List[TaggedData]) -> List[Input]:
        input_list = []
        for file in data:
            meta_data = {
                'relative_path': file.relative_path,
                'data': file
            }

            input_list.append(Input(meta_data=meta_data))

        return input_list

    def get_sub_dataset(self, key: str) -> BaseDataset:
        return self.splits[key]

    @property
    def available_sub_datasets(self):
        if self.splits is None:
            return []
        else:
            return list(self.splits.keys())
    
    def create_file_system(self, data_format: str):
        pass

    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, idx: int):
        return self.inputs[idx]
