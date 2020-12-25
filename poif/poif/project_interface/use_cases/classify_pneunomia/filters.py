from copy import deepcopy

from poif.base_classes import DataInput, DatasetOutput, MetaInput


def add_pneumonia(meta_input: MetaInput) -> MetaInput:
    categorie = meta_input.rel_file_path.split('/')[1]
    new_meta_input = deepcopy(meta_input)
    new_meta_input.label = categorie.lower()

    return new_meta_input


def ds_splitter(meta_input: MetaInput) -> str:
    ds_split = meta_input.rel_file_path.split('/')[0]
    return ds_split


def output_filter(data_input: DataInput) -> DatasetOutput:
    return data_input.data, data_input.label
