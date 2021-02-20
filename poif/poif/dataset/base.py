import copy
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional, Union

from poif.dataset.meta import MetaCollection
from poif.dataset.object.base import DataSetObject
from poif.dataset.object.output import DataSetObjectOutputFunction
from poif.dataset.operation.meta_provider.base import MetaProvider
from poif.dataset.operation.meta_provider.coco import CocoMetaProvider
from poif.dataset.operation.split.base import Splitter
from poif.dataset.operation.transform.base import Transformation
from poif.dataset.operation.transform_and_split.base import TransformAndSplit
from poif.tagged_data.base import TaggedData

Operation = Union[Transformation, Splitter, TransformAndSplit, MetaProvider]


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
        output_function: Optional[DataSetObjectOutputFunction] = None,
        continue_splitting_after_splitter: bool = False,
        continue_transformations_after_splitter: bool = True,
    ):

        super().__init__()
        self.splits = {}
        if operations is not None:
            self.operations = copy.deepcopy(operations)
        else:
            self.operations = []

        self.output_function = output_function

        self.continue_splitting_after_splitter = continue_splitting_after_splitter
        self.continue_transformations_after_splitter = continue_transformations_after_splitter

        self.initial_split_performed = False

        self.meta = MetaCollection()

    def __getattr__(self, item) -> Union[BaseDataset, "MultiDataset"]:
        if item in self.available_sub_datasets:
            return self.splits[item]
        else:
            raise AttributeError

    @property
    def available_sub_datasets(self):
        return list(self.splits.keys())

    def form(self, data: List[TaggedData]):
        inputs = [DataSetObject(tagged_data, output_function=self.output_function) for tagged_data in data]
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
        self.next_operation()

    def apply_operation(self, operation: Operation):
        stop_splitting = self.initial_split_performed and not self.continue_splitting_after_splitter
        stop_transformation = self.initial_split_performed and not self.continue_transformations_after_splitter

        if self.is_splitter(operation) and not stop_splitting:
            self.apply_splitter(operation)
        elif self.is_tranformation(operation) and not stop_transformation:
            self.apply_transformation(operation)
        elif isinstance(operation, MetaProvider):
            self.apply_meta_provider(operation)
        elif not stop_splitting or not stop_transformation:
            raise Exception("Unknown type of operation")

    def is_splitter(self, operation: Operation) -> bool:
        return isinstance(operation, Splitter) or isinstance(operation, TransformAndSplit)

    def is_tranformation(self, operation: Operation) -> bool:
        return isinstance(operation, Transformation)

    def apply_meta_provider(self, meta_provider: MetaProvider):
        new_meta_information = meta_provider.provide_meta(self.objects)
        for meta_name, meta_value in new_meta_information:
            self.meta[meta_name] = meta_value

    def apply_splitter(self, splitter: Splitter):
        splitter_dict = splitter(self.objects)

        self.add_splitter_dict(splitter_dict)

        self.initial_split_performed = True

    def add_splitter_dict(self, splitter_dict):
        for subset_name, inputs in splitter_dict.items():
            # TODO make a bit more transparent, if new attributes are added these should be also added here which is
            # not that clean
            new_dataset = MultiDataset(operations=copy.deepcopy(self.operations), output_function=self.output_function)
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

    def __add__(self, other: "MultiDataset") -> "MultiDataset":
        total_objects = self.objects + other.objects
        new_ds = MultiDataset()
        new_ds.objects = total_objects

        new_meta = self.meta + other.meta
        new_ds.meta = new_meta

        return new_ds


if __name__ == "__main__":
    from poif.dataset.operation.transform.detection import DetectionToClassification
    from poif.dataset.operation.transform.sampler import LimitSamplesByBin
    from poif.dataset.operation.transform_and_split.coco import MultiCoco
    from poif.tagged_data.disk import DiskData

    ds_loc = Path("/home/gilles/datasets/retail_product_checkout")
    tagged_data = DiskData.from_folder(ds_loc)

    annotation_files = {
        "train": "instances_train2019.json",
        "val": "instances_val2019.json",
        "test": "instances_test2019.json",
    }

    data_folders = {"train": "train2019", "val": "val2019", "test": "test2019"}
    add_index_mapping = CocoMetaProvider(annotation_file=annotation_files["train"])
    coco_transform = MultiCoco(annotation_files=annotation_files, data_folders=data_folders)
    limiter = LimitSamplesByBin(sample_limit=10, bin_creator=lambda x: x.label)
    operations = [add_index_mapping, coco_transform, DetectionToClassification(), limiter]
    ds = MultiDataset(operations=operations)
    ds.form(tagged_data)

    ds.train[0]

    print(len(ds))
    print(len(ds.train))
    print(len(ds.val))
    print(len(ds.test))
    print(ds.meta.index_to_label)
