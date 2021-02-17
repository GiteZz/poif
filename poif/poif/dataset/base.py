import copy
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Type, Union

from poif.dataset.object.base import DataSetObject
from poif.dataset.object.split.base import Splitter
from poif.dataset.object.transform.base import Transformation
from poif.tagged_data.base import TaggedData

Operation = Union[Transformation, Splitter]


class BaseDataset(ABC):
    def __init__(self):
        self.objects = []

    def create_file_system(self, data_format: str, base_folder: Path):
        raise Exception("File system not supported for this dataset")

    @abstractmethod
    def form(self, data: List[TaggedData]):
        pass

    def __len__(self):
        len(self.objects)

    def __getitem__(self, idx: int):
        return self.objects[idx].output()


class MultiDataset(BaseDataset):
    def __init__(
        self,
        operations: List[Operation] = None,
        input_type: Type[DataSetObject] = DataSetObject,
        continue_splitting_after_splitter: bool = False,
        continue_transformations_after_splitter: bool = True,
    ):

        super().__init__()
        self.splits = {}
        if operations is not None:
            self.operations = copy.deepcopy(operations)
        else:
            self.operations = []

        self.input_type = input_type

        self.continue_splitting_after_splitter = continue_splitting_after_splitter
        self.continue_transformations_after_splitter = continue_transformations_after_splitter

        self.initial_split_performed = False

    def __getattr__(self, item) -> Union[BaseDataset, "MultiDataset"]:
        if item in self.available_sub_datasets:
            return self.splits[item]
        else:
            raise AttributeError

    @property
    def available_sub_datasets(self):
        return list(self.splits.keys())

    def form(self, data: List[TaggedData]):
        inputs = [self.input_type(tagged_data) for tagged_data in data]
        self.form_from_ds_objects(inputs)

    def form_from_ds_objects(self, objects: List[DataSetObject]):
        # TODO maybe remove and integrate into self.form
        self.objects = objects
        self.next_operation()

    def next_operation(self):
        if self.operations is None or len(self.operations) == 0:
            return
        current_operation = self.operations.pop(0)
        self.apply_operation(current_operation)

    def apply_operation(self, operation: Operation):
        stop_splitting = self.initial_split_performed and not self.continue_splitting_after_splitter
        stop_transformation = self.initial_split_performed and not self.continue_transformations_after_splitter

        if self.is_splitter(operation) and not stop_splitting:
            self.apply_splitter(operation)
        elif self.is_tranformation(operation) and not stop_transformation:
            self.apply_transformation(operation)
        elif not stop_splitting or not stop_transformation:
            raise Exception("Unknown type of operation")
        self.next_operation()

    def is_splitter(self, operation: Operation) -> bool:
        return isinstance(operation, Splitter)

    def is_tranformation(self, operation: Operation) -> bool:
        return isinstance(operation, Transformation)

    def apply_splitter(self, splitter: Splitter):
        splitter_dict = splitter(self.objects)

        self.add_splitter_dict(splitter_dict)

        self.initial_split_performed = True

    def add_splitter_dict(self, splitter_dict):
        for subset_name, inputs in splitter_dict.items():
            new_dataset = MultiDataset(operations=copy.deepcopy(self.operations))
            new_dataset.form_from_ds_objects(inputs)

            self.splits[subset_name] = new_dataset

    def apply_transformation(self, transformation: Transformation):
        self.objects = transformation(self.objects)

    def add_transformation(self, operation: Operation):
        self.operations.append(operation)

    def __len__(self):
        return len(self.objects)

    def __getitem__(self, idx: int):
        value = self.objects[idx].output()
        return value
