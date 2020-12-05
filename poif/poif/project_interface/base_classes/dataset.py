from poif.project_interface.base_classes.resource import DataFilePath
from poif.project_interface.base_classes.input import Input
from poif.project_interface.data_handlers.disk_loader.load_functions import load
from poif.project_interface.base_classes.parameters import Parameters
from typing import List, Tuple, Union, Callable, Dict, Any
from collections import defaultdict
import logging


OutputFilter = Callable[[Input], Any]

logger = logging.getLogger(__name__)

# Resizing: Easy
# class <-> index: Need access to entire ds after


class BaseDataset:
    def __init__(self,
                 meta_list: List[Tuple[Input, DataFilePath]],
                 output_filter: OutputFilter = None):

        self.meta_list = meta_list
        self.output_filter = output_filter

    def __len__(self):
        return len(self.meta_list)

    def __getitem__(self, item) -> Input:
        data = load(self.meta_list[item][1])
        meta_input = self.meta_list[item][0]

        data_input = DataInput(meta_data=meta_input.meta_data, data=data, tag=meta_input.tag)
        if self.output_filter is not None:
            return self.output_filter(data_input)
        else:
            return data_input

    def get_meta_files(self) -> List[Input]:
        return [meta_data_tuple[0] for meta_data_tuple in self.meta_list]


class Dataset(BaseDataset):
    def __init__(self,
                 meta_list: List[Tuple[Input, DataFilePath]],
                 parameters: Parameters = None,
                 output_filter: OutputFilter = None,
                 ):

        # Make sure self.metadata_processors is always a list.
        super().__init__(meta_list, output_filter)
        if metadata_processors is not None and type(metadata_processors) != list:
            self.metadata_processors = [metadata_processors]
        else:
            self.metadata_processors = metadata_processors
        self.run_metadata_processor()

        self.dataset_filter = dataset_filer
        self.datapoint_filter = datapoint_filter

        if self.dataset_filter is not None and self.datapoint_filter is not None:
            logger.warning("Both dataset filter and datapoint filter are defined. Continuing with dataset_filter.")
            self.split_by_dataset_filter()
        elif self.dataset_filter is not None:
            self.split_by_dataset_filter()
        elif self.datapoint_filter is not None:
            self.split_by_point_filter()

    def split_by_dataset_filter(self):
        self.splits = self.dataset_filter(self.get_meta_files())

    def split_by_point_filter(self):
        dataset_split = defaultdict(list)
        for info_tuple in self.meta_list:
            dataset_split[self.datapoint_filter(info_tuple[0])].append(info_tuple)

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