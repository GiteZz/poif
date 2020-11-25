from poif.base_classes.resource import DataFilePath
from poif.base_classes.input import MetaInput, DataInput
from poif.data_handlers.disk_loader.load_functions import load
from typing import List, Tuple, Union, Callable, Dict
from collections import defaultdict
from dataclasses import dataclass


class Filter:
    pass


class DatasetFilter(Filter):
    pass


class DataPointFilter(Filter):
    def __init__(self, filter_function: Callable[[MetaInput], str]):
        self.filter = filter_function

    def __call__(self, meta_input: MetaInput) -> str:
        return self.filter(meta_input)

@dataclass
class MetadataProcessor:
    def __init__(self, processor: Callable[[MetaInput], MetaInput]):
        self.processor = processor

    def __call__(self, meta_input: MetaInput) -> MetaInput:
        return self.processor(meta_input)


class BaseDataset:
    def __init__(self, meta_list: List[Tuple[MetaInput, DataFilePath]]):
        self.meta_list = meta_list

    def __len__(self):
        return len(self.meta_list)

    def __getitem__(self, item) -> DataInput:
        data = load(self.meta_list[item][1])
        meta_input = self.meta_list[item][0]

        return DataInput(meta_data=meta_input.meta_data, data=data, tag=meta_input.tag)

    def get_meta_files(self) -> List[MetaInput]:
        return [meta_data_tuple[0] for meta_data_tuple in self.meta_list]

class Dataset(BaseDataset):
    def __init__(self, meta_list: List[Tuple[MetaInput, DataFilePath]],
                 split_filter: Union[DatasetFilter, DataPointFilter] = None,
                 metadata_processors: Union[List[MetadataProcessor], MetadataProcessor] = None):


        # Make sure self.metadata_processors is always a list.
        super().__init__(meta_list)
        if type(metadata_processors) == MetadataProcessor:
            self.metadata_processors = [metadata_processors]
        else:
            self.metadata_processors = metadata_processors
        self.run_metadata_processor()
        self.split_filer = split_filter
        self.splits: Dict[str, List[Tuple[MetaInput, DataFilePath]]]
        self.split_by_filter()

    def split_by_filter(self):
        if self.split_filer is None:
            return
        if type(self.split_filer) == DatasetFilter:
            self.split_by_dataset_filter()
        elif type(self.split_filer) == DataPointFilter:
            self.split_by_point_filter()
        else:
            raise Exception('This type of filter is not supported.')

    def split_by_dataset_filter(self):
        # TODO
        pass

    def split_by_point_filter(self):
        dataset_split = defaultdict(list)
        for info_tuple in self.meta_list:
            dataset_split[self.split_filer(info_tuple[0])].append(info_tuple)

        self.splits = dataset_split

    def run_metadata_processor(self):
        if self.metadata_processors is None:
            return
        for processor in self.metadata_processors:
            for index, (meta_input, data_path) in enumerate(self.meta_list):
                new_meta_input = processor(meta_input)
                self.meta_list[index] = (new_meta_input, data_path)

    def __getattr__(self, item):
        return BaseDataset(self.splits[item])