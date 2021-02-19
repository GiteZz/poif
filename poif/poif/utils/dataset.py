from typing import List

from poif.tagged_data.base import TaggedData


def tagged_data_to_rel_file_mapping(tagged_datas: List[TaggedData]):
    mapping = {}
    for tagged_data in tagged_datas:
        mapping[tagged_data.relative_path] = tagged_data

    return mapping
