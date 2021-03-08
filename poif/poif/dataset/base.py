import copy
from abc import ABC, abstractmethod
from typing import List, Optional, Union

from poif.dataset.meta import MetaCollection
from poif.dataset.object.base import DataSetObject
from poif.dataset.object.output import DataSetObjectOutputFunction
from poif.dataset.operation.base import Operation
from poif.dataset.operation.meta_provider.base import MetaProvider
from poif.dataset.operation.selective import SelectiveSubsetOperation
from poif.dataset.operation.split.base import Splitter
from poif.dataset.operation.transform.base import Transformation
from poif.dataset.operation.transform_and_split.base import TransformAndSplit
from poif.tagged_data.base import TaggedData


class BaseDataset(ABC):
    """
    Provide base dataset functionality similarly to torch.utils.data.Dataset. The __getitem__ wil return the
    result of the .output() function on the DataSetObject at that index. This class is used as an interface,
    not intended to be instantiated.
    """

    def __init__(self):
        self.objects = []

    @abstractmethod
    def form(self, data: List[TaggedData]):
        pass

    def __len__(self):
        len(self.objects)

    def __getitem__(self, idx: int):
        return self.objects[idx].output()


class Dataset(BaseDataset):
    def __init__(
        self, operations: List[Operation] = None, output_function: Optional[DataSetObjectOutputFunction] = None
    ):

        super().__init__()
        self.splits = {}
        if operations is not None:
            self.operations = copy.deepcopy(operations)
        else:
            self.operations = []

        self.output_function = output_function

        self.initial_split_performed = False

        self._meta = MetaCollection()

    def __getattr__(self, item) -> Union[BaseDataset, "Dataset"]:
        if item in self.available_sub_datasets:
            return self.splits[item]
        else:
            raise AttributeError

    @property
    def meta(self) -> MetaCollection:
        return self._meta

    @property
    def available_sub_datasets(self) -> List[str]:
        return list(self.splits.keys())

    def form(self, data: List[TaggedData]):
        inputs = [DataSetObject(tagged_data, output_function=self.output_function) for tagged_data in data]
        self.form_from_ds_objects(inputs)

    def _set_ds_objects(self, objects: List[DataSetObject]):
        self.objects = objects

    def form_from_ds_objects(self, objects: List[DataSetObject]):
        # TODO maybe remove and integrate into self.form
        self.objects = objects
        self._next_operation()

    def _next_operation(self):
        if self.operations is None or len(self.operations) == 0:
            return
        current_operation = self.operations.pop(0)
        self.apply_operation(current_operation)
        self._next_operation()

    def apply_operation(self, operation: Operation):
        if len(self.splits) != 0:
            if isinstance(operation, SelectiveSubsetOperation):
                for subset, sub_ds in self.splits.items():
                    if subset in operation.subsets:
                        sub_ds.apply_operation(operation[subset])
                    else:
                        sub_ds.apply_operation(operation)
            else:
                for sub_ds in self.splits.values():
                    sub_ds.apply_operation(operation)
        else:
            operation.set_meta(self.meta)
            if self._is_splitter(operation):
                self._apply_splitter(operation)
            elif self._is_tranformation(operation):
                self._apply_transformation(operation)
            elif isinstance(operation, MetaProvider):
                self._apply_meta_provider(operation)
            else:
                raise Exception("Unknown type of operation")

    def _is_splitter(self, operation: Operation) -> bool:
        return isinstance(operation, Splitter) or isinstance(operation, TransformAndSplit)

    def _is_tranformation(self, operation: Operation) -> bool:
        return isinstance(operation, Transformation)

    def _apply_meta_provider(self, meta_provider: MetaProvider):
        new_meta = meta_provider.provide_meta(self.objects, self._meta)
        self._meta = new_meta

    def _apply_splitter(self, splitter: Splitter):
        splitter_dict = splitter(self.objects)

        self._add_splitter_dict(splitter_dict)

        self.initial_split_performed = True

    def _create_child_dataset(self) -> "Dataset":
        new_ds = Dataset()
        new_ds.output_function = self.output_function
        new_ds._meta = self._meta

        return new_ds

    def _add_splitter_dict(self, splitter_dict):
        for subset_name, objects in splitter_dict.items():
            new_dataset = self._create_child_dataset()
            new_dataset._set_ds_objects(objects)

            self.splits[subset_name] = new_dataset

    def _apply_transformation(self, transformation: Transformation):
        self.objects = transformation(self.objects)

    def __len__(self):
        return len(self.objects)

    def __getitem__(self, idx: int):
        value = self.objects[idx].output()
        return value

    def __add__(self, other: "Dataset") -> "Dataset":
        total_objects = self.objects + other.objects
        new_ds = Dataset()
        new_ds.objects = total_objects

        new_meta = self._meta + other._meta
        new_ds._meta = new_meta

        return new_ds
