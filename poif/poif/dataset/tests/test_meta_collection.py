import pytest

from poif.dataset.meta import MetaCollection


def test_meta_collection():
    meta = MetaCollection()
    meta["value1"] = "value1"
    assert meta.value1 == "value1"


def test_adding():
    meta1 = MetaCollection()
    meta2 = MetaCollection()

    for i in range(5):
        meta1[f"value{i}"] = f"value{i}"

    for i in range(5, 10):
        meta2[f"value{i}"] = f"value{i}"

    combined_meta = meta1 + meta2
    for i in range(10):
        assert combined_meta[f"value{i}"] == f"value{i}"

    for i in range(5, 10):
        with pytest.raises(KeyError):
            meta1[f"value{i}"]

    for i in range(5):
        with pytest.raises(KeyError):
            meta2[f"value{i}"]
