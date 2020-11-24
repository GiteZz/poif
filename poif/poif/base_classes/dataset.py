from poif.base_classes import DataFilePath, MetaInput, DataInput
from poif.data_handler.disk_loader.load_functions import load
from typing import List, Tuple
import hashlib


class Dataset:
    def __init__(self, meta_list: List[Tuple[MetaInput, DataFilePath]]):
        self.meta_list = meta_list

    def __len__(self):
        return len(self.meta_list)

    def __getitem__(self, item) -> DataInput:
        data = load(self.meta_list[item][0])
        meta_input = self.meta_list[item][1]
        file_hash = hashlib.md5(open(self.meta_list[item][0], 'rb').read()).hexdigest()  # TODO combine with load function to avoid loading twice

        return DataInput(name=meta_input.name, meta_data=meta_input.meta_data, data=data, tag=file_hash)
