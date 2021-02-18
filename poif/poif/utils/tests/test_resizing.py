import numpy as np

from poif.utils import get_img_size, resize_img, resize_with_padding


def test_resize_with_padding():
    w = 600
    h = 200
    img = np.ones((h, w, 3))
    resized_img = resize_with_padding(img, new_height=100, new_width=500)

    assert get_img_size(resized_img) == (100, 500)

    assert np.all(resized_img[:, 0:100] == 0)
    assert np.all(resized_img[:, 100:400] == 1)
    assert np.all(resized_img[:, 400:500] == 0)

    w = 200
    h = 600
    img = np.ones((h, w, 3))
    resized_img = resize_with_padding(img, new_height=500, new_width=100)

    assert get_img_size(resized_img) == (500, 100)

    assert np.all(resized_img[0:100, :] == 0)
    assert np.all(resized_img[100:400, :] == 1)
    assert np.all(resized_img[400:500, :] == 0)


def test_resizing():
    w = 200
    h = 600
    img = np.ones((h, w, 3))
    resized1 = resize_img(img, new_width=256, new_height=256)
    assert get_img_size(resized1) == (256, 256)
