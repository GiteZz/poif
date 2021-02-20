from poif.dataset.base import MultiDataset
from poif.dataset.object.output import classification_output
from poif.dataset.operation.meta_provider.label_to_index import LabelToIndex
from poif.dataset.operation.split.template import SplitByTemplate
from poif.dataset.operation.transform.template import ClassificationByTemplate
from poif.tagged_data.tests.mock import MockTaggedData


def test_meta_provider():
    ds_tagged_data = []
    for subset in ["train", "val"]:
        for category_index in range(10):
            for img_index in range(100):

                new_object = MockTaggedData(
                    relative_path=f"{subset}/cat{category_index}/{img_index}.png", data=category_index
                )

                ds_tagged_data.append(new_object)

    template = "{{subset}}/{{label}}/*.png"
    add_label = ClassificationByTemplate(template=template)
    split_into_subset = SplitByTemplate(template=template)
    label_to_index = LabelToIndex()

    operations = [split_into_subset, add_label, label_to_index]
    ds = MultiDataset(operations=operations, output_function=classification_output)
    ds.form(ds_tagged_data)

    ds_mapping = ds.meta.index_to_label

    for label, value in ds.train:
        assert f"cat{value}" == ds_mapping[label]
