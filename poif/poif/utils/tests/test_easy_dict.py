from poif.utils.easy_dict import EasyDict


def test_easy_dict():
    data_collection = EasyDict()

    # data_collection.a = 5
    # assert data_collection.a == 5

    data_collection.b.c = 6
    assert data_collection.b.c == 6