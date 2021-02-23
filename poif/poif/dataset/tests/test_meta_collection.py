from poif.dataset.meta import MetaCollection


def test_adding():
    meta1 = MetaCollection()
    meta2 = MetaCollection()

    index_to_label = {1: "a", 2: "b", 3: "c"}
    label_to_index = {"a": 1, "b": 2, "c": 3}

    meta1.index_to_label = index_to_label
    meta2.label_to_index = label_to_index

    combined_meta = meta1 + meta2

    assert combined_meta.index_to_label == index_to_label
    assert combined_meta.label_to_index == label_to_index

    meta3 = MetaCollection()
    meta4 = MetaCollection()

    index_to_label1 = {1: "a", 2: "b", 3: "c"}
    index_to_label2 = {1: "a", 2: "b", 3: "c"}

    meta3.index_to_label = index_to_label1
    meta4.index_to_label = index_to_label2

    combined_meta = meta3 + meta4

    assert combined_meta.index_to_label == index_to_label1
    assert combined_meta.label_to_index is None
