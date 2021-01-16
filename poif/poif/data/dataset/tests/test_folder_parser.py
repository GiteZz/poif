import re
from collections import defaultdict
from typing import List, Dict

from poif.data.access.input import Input
from poif.data.datapoint.base import TaggedData
from poif.typing import path_template


def test_matching():
    assert is_path_match('*/mask_*.jpg', 'train/mask_01.jpg')
    assert is_path_match('train/mask_*.jpg', 'train/mask_01.jpg')
    assert not is_path_match('test/mask_*.jpg', 'train/mask_01.jpg')


def test_extracting():
    assert extract_values('{{ dataset_type }}/*/*.jpg', 'train/image/01.jpg') == {'dataset_type': 'train'}
    assert extract_values('{{dataset_type }}/*/*.jpg', 'train/image/01.jpg') == {'dataset_type': 'train'}
    assert extract_values('{{dataset_type}}/*/*.jpg', 'train/image/01.jpg') == {'dataset_type': 'train'}

    assert extract_values(
        '{{ dataset_type }}/{{image_type}}/*.jpg',
        'train/image/01.jpg'
    ) == {
               'dataset_type': 'train',
               'image_type': 'image'
           }

    assert extract_values(
        '{{ dataset_type }}/{{image_type}}/*.jpg',
        'test/mask/01.jpg'
    ) == {
               'dataset_type': 'test',
               'image_type': 'mask'
           }

    assert extract_values(
        '{{ dataset_type }}/{{image_type}}/*.png',
        'test/mask/01.jpg'
    ) == {}


def test_is_template_part():
    assert is_template_part('{{test}}')
    assert is_template_part('{{ test }}')
    assert not is_template_part('{test}')
    assert not is_template_part('test')


def test_catch_all_to_value():
    assert catch_all_to_value('*/*') == '{{0}}/{{1}}'
    assert catch_all_to_value('*') == '{{0}}'
    assert catch_all_to_value('test') == 'test'


def test_pair_collecter():
    inputs = []
    for subset_name in ['train', 'test', 'val']:
        for img_type in ['mask', 'image']:
            for img_index in range(10):
                metadata = {
                    'data': f'{subset_name}{img_index}',
                    'relative_path': f'{subset_name}/{img_type}/{img_index}.jpg'
                }
                inputs.append(Input(metadata))

    match_template = {
        'mask': '*/mask/*.jpg',
        'image': '*/image/*.jpg'
    }

    collected_inputs = pair_collecter(match_template, inputs)

    for new_input in collected_inputs:
        assert new_input.image.data == new_input.mask.data




def is_template_part(part: str):
    return re.match('\{\{[^\/]*\}\}', part)


def get_template_str(part: str):
    return part.replace('{', '').replace('}', '').replace(' ', '')


def template_to_regex(template: str):
    return template.replace('.', '[.]').replace('*', '.*')


def is_path_match(template: str, path: str) -> bool:
    template_parts = template.split('/')
    path_parts = path.split('/')

    if len(template_parts) != len(path_parts):
        return False

    for template_part, path_part in zip(template_parts, path_parts):
        if is_template_part(template_part):
            continue

        regex_pattern = template_to_regex(template_part)
        if not re.match(regex_pattern, path_part):
            return False

    return True


def extract_values(template: str, path: str) -> Dict[str, str]:
    if not is_path_match(template, path):
        return {}

    template_parts = template.split('/')
    path_parts = path.split('/')

    value_dict = {}
    for template_part, path_part in zip(template_parts, path_parts):
        if is_template_part(template_part):
            value_dict[get_template_str(template_part)] = path_part

    return value_dict


def catch_all_to_value(template: str):
    """
    */*.jpg -> {{1}}/{{2}}.jpg
    """
    new_template = ""
    parts = template.split('*')
    if len(parts) == 1:
        return template

    for index, part in enumerate(parts[:-1]):
        new_template += part + "{{" + str(index) + "}}"
    new_template += parts[-1]

    return new_template


def pair_collecter(match_templates: Dict[str, path_template], inputs: List[Input], input_item='relative_path'):
    value_templates = {template_name: catch_all_to_value(template)
                       for template_name, template in match_templates.items()
                       }
    value_bins = defaultdict(dict)
    for ds_input in inputs:
        for template_name, template in value_templates.items():
            values = extract_values(template=template, path=ds_input[input_item])
            hashable_values = tuple(sorted(values.items()))
            value_bins[hashable_values][template_name] = ds_input

    new_inputs = []
    for bin in value_bins.values():
        new_input = Input()
        for template_name, template_input in bin.items():
            new_input[template_name] = template_input
        new_inputs.append(new_input)

    return new_inputs


def split_by_folder_template(templates: List[str]):
    pass