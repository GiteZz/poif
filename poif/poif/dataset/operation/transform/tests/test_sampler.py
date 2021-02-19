from poif.dataset.object.tests.mock import MockDataSetObject
from poif.dataset.operation.transform.sampler import LimitSamplesByBin


def test_limit_sampler():
    limiter = LimitSamplesByBin(sample_limit=10, bin_creator=lambda x: x.label)

    ds_objects = []
    label_count = 25
    items_per_label = 15
    for label in range(label_count):
        for item_index in range(items_per_label):
            ds_object = MockDataSetObject(rel_path="", data=f"{label} - {item_index}")
            ds_object.label = label

            ds_objects.append(ds_object)

    transformed_objects = limiter(ds_objects)

    assert len(transformed_objects) == 10 * label_count
    for label in range(label_count):
        items_per_label = [ds_object for ds_object in transformed_objects if ds_object.label == label]
        assert len(items_per_label) == 10
