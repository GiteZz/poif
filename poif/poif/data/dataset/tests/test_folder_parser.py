import re
from typing import List, Dict


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


def split_by_folder_template(templates: List[str]):
    pass