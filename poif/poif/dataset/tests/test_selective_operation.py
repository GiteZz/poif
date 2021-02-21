from poif.dataset.base import MultiDataset
from poif.dataset.object.output import classification_output
from poif.dataset.operation import SelectiveSubsetOperation
from poif.dataset.operation.split.template import SplitByTemplate
from poif.dataset.operation.transform.sampler import LimitSamplesByBin
from poif.dataset.operation.transform.template import ClassificationByTemplate
from poif.tagged_data.tests.mock import MockTaggedData


def test_selective_operation():
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

    limit_train = LimitSamplesByBin(sample_limit=50, bin_creator=lambda x: x.label)
    limit_val = LimitSamplesByBin(sample_limit=10, bin_creator=lambda x: x.label)

    limit_both = SelectiveSubsetOperation({"train": limit_train, "val": limit_val})

    operations = [split_into_subset, add_label, limit_both]
    ds = MultiDataset(operations=operations, output_function=classification_output)
    ds.form(ds_tagged_data)

    assert len(ds.train) == 50 * 10
    assert len(ds.val) == 10 * 10
