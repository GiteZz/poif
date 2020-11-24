from poif.base_classes import MetaInput, DataInput, MetaFilePath, DataFilePath
from pathlib import Path
from typing import List, Tuple, Dict
import yaml


def poif_format_file_gatherer(path: Path) -> List[Tuple[MetaFilePath, DataFilePath]]:
    meta_files = path.glob('*.meta')

    tuple_list = []

    for meta_file in meta_files:
        file_name = meta_file.parts[-1].replace('.meta', '')
        data_file_glob = list((meta_file.parent / file_name).glob('.*'))

        if len(data_file_glob) > 2:
            print(f'{meta_file} is associated with multiple data files.')
        elif len(data_file_glob) == 1:
            print(f'{meta_file} has no associated data file.')
        else:
            if '.meta' in data_file_glob[0].parts[-1]:
                tuple_list.append((meta_file, data_file_glob[0]))
            else:
                tuple_list.append((meta_file, data_file_glob[1]))

    return tuple_list


def poif_format_fill_metadata(
        path_tuples: List[Tuple[MetaFilePath, DataFilePath]]
) -> List[Tuple[MetaInput, DataFilePath]]:

    metadata_tuple_list = []
    for meta_path, data_path in path_tuples:
        file_name = meta_path.parts[-1]
        with open(meta_path, 'r') as f:
            meta_data = yaml.safe_load(f)
            meta_input = MetaInput(name=file_name, meta_data=meta_data)
            metadata_tuple_list.append((meta_input, data_path))

    return metadata_tuple_list
