from poif.project_interface.base_classes.input import MetaInput
from poif.project_interface.base_classes.data_query import DataQuery
from poif.typing import FileHash, RelFilePath
from typing import List, Dict
from pathlib import Path


def remote_file_list_to_meta_inputs(query: DataQuery, file_list: Dict[FileHash, RelFilePath]) -> List[MetaInput]:
    meta_input_list = []
    for file_hash, rel_file in file_list.items():
        file_name = Path(rel_file).parts[-1]
        rel_file_path = '/'.join(Path(rel_file).parts[:-1])
        meta_input = MetaInput()
