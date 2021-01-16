from poif.data.access.input import Input
from poif.data.transform.combine import CombineByTemplate, SplitByTemplate, DropByTemplate
from poif.data.transform.tools import is_path_match, extract_values, is_template_part, catch_all_to_value, \
    replace_template_with_group
import pytest

def test_matching():
    assert is_path_match('*/mask_*.jpg', 'train/mask_01.jpg')
    assert is_path_match('train/mask_*.jpg', 'train/mask_01.jpg')
    assert not is_path_match('test/mask_*.jpg', 'train/mask_01.jpg')
    assert is_path_match('{{dataset_type}}/mask_{{img_id}}', 'train/mask_01.jpg')

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

    assert extract_values(
        '{{dataset_type}}/mask_{{img_id}}', 'train/mask_01.jpg'
    ) == {'dataset_type': 'train', 'img_id': '01.jpg'}


def test_is_template_part():
    assert is_template_part('{{test}}')
    assert is_template_part('{{ test }}')
    assert not is_template_part('{test}')
    assert not is_template_part('test')


def test_catch_all_to_value():
    assert catch_all_to_value('*/*') == '{{0}}/{{1}}'
    assert catch_all_to_value('*') == '{{0}}'
    assert catch_all_to_value('test') == 'test'


def test_replace_template_with_group():
    template = '{{ dataset_type }}/{{ data_type }}/*'
    new_template, groups = replace_template_with_group(template)
    assert groups == ['dataset_type', 'data_type']
    assert new_template == '(.*)/(.*)/*'

    template = '{{ dataset_type }}/mask_{{ data_type }}/*'
    new_template, groups = replace_template_with_group(template)
    assert groups == ['dataset_type', 'data_type']
    assert new_template == '(.*)/mask_(.*)/*'

    template = '{{ dataset_type }}/mask_01.jpg'
    new_template, groups = replace_template_with_group(template)
    assert groups == ['dataset_type']
    assert new_template == '(.*)/mask_01.jpg'

@pytest.fixture
def mask_inputs():
    inputs = []
    for subset_name in ['train', 'test', 'val']:
        for img_type in ['mask', 'image']:
            for img_index in range(10):
                metadata = {
                    'data': f'{subset_name}{img_index}',
                    'relative_path': f'{subset_name}/{img_type}/{img_index}.jpg'
                }
                inputs.append(Input(metadata))

    return inputs


def test_pair_collecter(mask_inputs):
    match_template = {
        'mask': '*/mask/*.jpg',
        'image': '*/image/*.jpg'
    }

    collected_inputs = CombineByTemplate(match_template)(mask_inputs)

    for new_input in collected_inputs:
        assert new_input.image.data == new_input.mask.data

    assert len(mask_inputs) == 2 * len(collected_inputs)


def test_split_by_template(mask_inputs):
    dataset_type_splitter = SplitByTemplate('{{ dataset_type }}/{{ data_type }}/*', subset_tag='dataset_type')
    data_type_splitter = SplitByTemplate('{{ dataset_type }}/{{ data_type }}/*', subset_tag='data_type')

    for input in mask_inputs:
        assert input.relative_path.split('/')[0] == dataset_type_splitter(input)
        assert input.relative_path.split('/')[1] == data_type_splitter(input)

def test_drop_by_template(mask_inputs):
    dataset_dropper = DropByTemplate('*/mask/*.jpg')

    for ds_input in mask_inputs:
        if 'mask' in ds_input.relative_path:
            assert dataset_dropper(ds_input) == []
        else:
            assert dataset_dropper(ds_input) == ds_input

