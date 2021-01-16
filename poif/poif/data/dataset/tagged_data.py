from poif.data.dataset.base import MultiDataset, BaseDataset
from collections import defaultdict

from dataclasses import dataclass
from typing import List, Union, Dict, Any

from poif.data.dataset.base import SplitterType, TransformationType
from poif.data.access.input import Input
from poif.data.datapoint.base import TaggedData
from poif.data.transform.transform import (DataPointSplitter,
                                           DataPointTransformation,
                                           DataSetSplitter, DataSetTransformation,
                                           OutputFilter)


class TaggedDataBaseDataset(BaseDataset):
    def create_file_system(self, data_format: str):
        pass

    def __init__(self,
                 transformations: Union[TransformationType, List[TransformationType]] = None,
                 output_filter: OutputFilter = None
                 ):

        self.transformations = transformations
        self.output_filter = output_filter

        if self.transformations is not None and (
                isinstance(self.transformations,
                           DataSetTransformation) or
                isinstance(self.transformations,
                           DataPointTransformation)
        ):
            self.transformations = [self.transformations]
        elif self.transformations is None:
            self.transformations = []

        self.inputs = None

    def __len__(self):
        return len(self.inputs)

    def __getitem__(self, idx) -> Any:
        input_item = self.inputs[idx]

        if self.output_filter is not None:
            return self.output_filter(input_item)
        else:
            return input_item

    def form(self, data: List[TaggedData]):
        inputs = self.get_inputs(data)
        self.inputs = self.transform_inputs(inputs)

    def get_inputs(self, data: List[TaggedData]) -> List[Input]:
        input_list = []
        for file in data:
            meta_data = {
                'relative_path': file.relative_path,
                'data': file
            }

            input_list.append(Input(meta_data=meta_data))

        return input_list

    def transform_inputs(self, input_list: List[Input]) -> List[Input]:
        current_list = input_list
        for transformation in self.transformations:
            if isinstance(transformation, DataPointTransformation):
                new_list = []
                for item in current_list:
                    # The transformation can give back None, one or more meta inputs, therefore we have to
                    # take different actions based on the format returned.
                    new_item = transformation(item)
                    if new_item is None:
                        continue
                    if isinstance(new_item, list):
                        new_list.extend(new_item)
                    else:
                        new_list.append(new_item)
                current_list = new_list

            elif isinstance(transformation, DataSetTransformation):
                current_list = transformation(current_list)
        return current_list


class TaggedDataDataset(TaggedDataBaseDataset, MultiDataset):

    def __init__(self, splitters: Union[SplitterType, List[SplitterType]] = None,
                 transformations: Union[TransformationType, List[TransformationType]] = None,
                 output_filter: OutputFilter = None):

        super().__init__(transformations, output_filter)

        self.splitters = splitters
        self.splits = None

        if self.splitters is not None and (
                isinstance(self.splitters, DataSetSplitter) or isinstance(self.splitters, DataPointSplitter)
        ):
            self.splitters = [self.splitters]
        elif self.splitters is None:
            self.splitters = []

    def form(self, data: List[TaggedData]):
        super().form(data)

        self.splits = self.split_inputs(self.inputs)

    def get_sub_dataset(self, key: str) -> BaseDataset:
        return self.splits[key]

    @property
    def available_sub_datasets(self):
        if self.splits is None:
            return []
        else:
            return list(self.splits.keys())

    def split_inputs(self, input_list: List[Input]) -> Dict[str, List[Input]]:
        list_split_dicts = []
        for splitter in self.splitters:
            if isinstance(splitter, DataPointSplitter):
                splitter_dict = defaultdict(list)
                for input_item in input_list:
                    splitter_dict[splitter(input_item)].append(input_item)
                list_split_dicts.append(splitter_dict)
            elif isinstance(splitter, DataSetSplitter):
                list_split_dicts.append(splitter(input_list))

        collect_dicts = defaultdict(set)
        for split_dict in list_split_dicts:
            for key, input_list in split_dict.items():
                collect_dicts[key].update(input_list)

        return {key: list(value) for key, value in collect_dicts.items()}