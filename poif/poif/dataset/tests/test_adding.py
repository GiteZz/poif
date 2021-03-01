from poif.dataset.base import Dataset
from poif.dataset.object.output import classification_output
from poif.dataset.operation.split.template import SplitByTemplate
from poif.tagged_data.tests.mock import MockTaggedData


def test_adding():
    ds_tagged_data = []
    for subset in ["train", "val"]:
        for img_index in range(100):

            new_object = MockTaggedData(relative_path=f"{subset}/{img_index}.png", data=f"{subset}/{img_index}.png")

            ds_tagged_data.append(new_object)

    template = "{{subset}}/*.png"
    split_into_subset = SplitByTemplate(template=template)

    operations = [split_into_subset]
    ds = Dataset(operations=operations, output_function=classification_output)
    ds.form(ds_tagged_data)

    assert len(ds) == len(ds.train + ds.val)

    assert set(ds.objects) == set((ds.train + ds.val).objects)
