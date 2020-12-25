import hashlib
from pathlib import Path
from typing import Dict, List, Tuple

import yaml

from poif.project_interface.classes.input import Input
from poif.project_interface.classes.resource import DataFilePath, MetaFilePath


def poif_format_file_gatherer(path: Path) -> List[Input]:
    meta_files = path.rglob('*.meta')

    meta_input_list = []

    for meta_file in meta_files:
        file_name = meta_file.parts[-1].replace('.meta', '')
        data_file_glob = list(meta_file.parent.glob(f'{file_name}.*'))

        if len(data_file_glob) > 2:
            print(f'{meta_file} is associated with multiple data files.')
        elif len(data_file_glob) == 1:
            print(f'{meta_file} has no associated data file.')
        else:
            if '.meta' in data_file_glob[0].parts[-1]:
                data_path = data_file_glob[1]
            else:
                data_path = data_file_glob[0]

            file_hash = hashlib.md5(open(data_path, 'rb').read()).hexdigest()

            with open(meta_file, 'r') as f:
                meta_data = yaml.safe_load(f)
                if meta_data is None:
                    print(f'Error with {meta_file}')
                    continue
                meta_data['file_name'] = file_name
                meta_data['rel_file_path'] = str(meta_file.parent)[len(str(path)) + 1:]
                meta_input = Input(meta_data=meta_data, tag=file_hash, data_loc=data_path)

                meta_input_list.append(meta_input)

    return meta_input_list


def file_gatherer(path: Path, extensions: List[str]) -> List[Input]:
    meta_input_list = []
    file_list = []
    # Remove the leading point from all extensions.
    parsed_extensions = [ext[1:] if ext[0] == '.' else ext for ext in extensions]

    for extension in parsed_extensions:
        file_list.extend(list(path.rglob(f'*.{extension}')))

    for file in file_list:
        file_hash = hashlib.md5(open(file, 'rb').read()).hexdigest()
        meta_data = {}
        file_name = file.parts[-1].split('.')[0]

        meta_data['file_name'] = file_name
        meta_data['rel_file_path'] = str(file.parent)[len(str(path)) + 1:]
        meta_input = Input(meta_data=meta_data, tag=file_hash, data_loc=file)

        meta_input_list.append(meta_input)

    return meta_input_list


if __name__ == "__main__":
    ds_path = Path('/home/gilles/test_daif/dogs_vs_cats/data')
    collected_tuples = poif_format_file_gatherer(ds_path)

    ds_path = Path('/home/datasets/pneunomia')
    file_tuples = file_gatherer(ds_path, ['.jpeg'])
    a = 5