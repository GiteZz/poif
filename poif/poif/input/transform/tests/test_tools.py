import pytest

from poif.input.tagged_data import TaggedDataInput
from poif.input.transform.template import DropByTemplate, MaskByTemplate, MaskTemplate
from poif.input.transform.tools import (
    catch_all_to_value,
    extract_values,
    is_path_match,
    is_template_part,
    replace_template_with_regex_group,
)
from poif.tagged_data.tests.mock import MockTaggedData


def test_matching():
    assert is_path_match("*/mask_*.jpg", "train/mask_01.jpg")
    assert is_path_match("train/mask_*.jpg", "train/mask_01.jpg")
    assert not is_path_match("test/mask_*.jpg", "train/mask_01.jpg")
    assert is_path_match("{{dataset_type}}/mask_{{img_id}}", "train/mask_01.jpg")


def test_extracting():
    assert extract_values("{{ dataset_type }}/*/*.jpg", "train/image/01.jpg") == {"dataset_type": "train"}
    assert extract_values("{{dataset_type }}/*/*.jpg", "train/image/01.jpg") == {"dataset_type": "train"}
    assert extract_values("{{dataset_type}}/*/*.jpg", "train/image/01.jpg") == {"dataset_type": "train"}

    assert extract_values("{{ dataset_type }}/{{image_type}}/*.jpg", "train/image/01.jpg") == {
        "dataset_type": "train",
        "image_type": "image",
    }

    assert extract_values("{{ dataset_type }}/{{image_type}}/*.jpg", "test/mask/01.jpg") == {
        "dataset_type": "test",
        "image_type": "mask",
    }

    assert extract_values("{{ dataset_type }}/{{image_type}}/*.png", "test/mask/01.jpg") == {}

    assert extract_values("{{dataset_type}}/mask_{{img_id}}", "train/mask_01.jpg") == {
        "dataset_type": "train",
        "img_id": "01.jpg",
    }


def test_is_template_part():
    assert is_template_part("{{test}}")
    assert is_template_part("{{ test }}")
    assert not is_template_part("{test}")
    assert not is_template_part("test")


def test_catch_all_to_value():
    assert catch_all_to_value("*/*") == "{{0}}/{{1}}"
    assert catch_all_to_value("*") == "{{0}}"
    assert catch_all_to_value("test") == "test"


def test_replace_template_with_group():
    template = "{{ dataset_type }}/{{ data_type }}/*"
    new_template, groups = replace_template_with_regex_group(template)
    assert groups == ["dataset_type", "data_type"]
    assert new_template == "(.*)/(.*)/*"

    template = "{{ dataset_type }}/mask_{{ data_type }}/*"
    new_template, groups = replace_template_with_regex_group(template)
    assert groups == ["dataset_type", "data_type"]
    assert new_template == "(.*)/mask_(.*)/*"

    template = "{{ dataset_type }}/mask_01.jpg"
    new_template, groups = replace_template_with_regex_group(template)
    assert groups == ["dataset_type"]
    assert new_template == "(.*)/mask_01.jpg"

    template = "{{ dataset_type }}/mask_{{}}"
    new_template, groups = replace_template_with_regex_group(template)
    assert groups == ["dataset_type", "_0"]
    assert new_template == "(.*)/mask_(.*)"

    template = "{{}}/mask_{{}}"
    new_template, groups = replace_template_with_regex_group(template)
    assert groups == ["_0", "_1"]
    assert new_template == "(.*)/mask_(.*)"


@pytest.fixture
def mask_inputs():
    inputs = []
    for subset_name in ["train", "test", "val"]:
        for img_type in ["mask", "image"]:
            for img_index in range(10):
                tagged_data = MockTaggedData(
                    relative_path=f"{subset_name}/{img_type}/{img_index}.jpg",
                    data="{subset_name}{img_index}",
                )
                inputs.append(TaggedDataInput(data=tagged_data))

    return inputs


def test_pair_collecter(mask_inputs):
    collected_inputs = MaskByTemplate(MaskTemplate(image="{{}}/image/{{}}.jpg", mask="{{}}/mask/{{}}.jpg"))(
        mask_inputs
    )

    for new_input in collected_inputs:
        image, mask = new_input.output()
        assert image == mask

    assert len(mask_inputs) == 2 * len(collected_inputs)


def test_split_by_template(mask_inputs):
    dataset_type_splitter = SplitByTemplate("{{ dataset_type }}/{{ data_type }}/*", subset_tag="dataset_type")
    data_type_splitter = SplitByTemplate("{{ dataset_type }}/{{ data_type }}/*", subset_tag="data_type")

    for input in mask_inputs:
        assert input.relative_path.split("/")[0] == dataset_type_splitter(input)
        assert input.relative_path.split("/")[1] == data_type_splitter(input)


def test_drop_by_template(mask_inputs):
    dataset_dropper = DropByTemplate("*/mask/*.jpg")

    for ds_input in mask_inputs:
        if "mask" in ds_input.relative_path:
            assert dataset_dropper(ds_input) == []
        else:
            assert dataset_dropper(ds_input) == ds_input
