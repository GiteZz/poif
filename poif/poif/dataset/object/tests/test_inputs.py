import numpy as np

from poif.dataset.base import Dataset
from poif.dataset.object.annotations import Mask
from poif.dataset.object.base import DataSetObject
from poif.dataset.object.output import single_mask_output
from poif.tagged_data.tests.mock import MockTaggedData
from poif.tests import get_img


def test_mask():
    img = get_img()
    mask = get_img()

    image_data = MockTaggedData("", img)
    mask_data = MockTaggedData("", mask)

    image_ds_object = DataSetObject(image_data, output_function=single_mask_output)
    image_ds_object.annotations.append(Mask(mask_data))

    ds = Dataset()
    ds.form_from_ds_objects([image_ds_object])

    img_output, mask_output = ds[0]

    assert np.all(img_output == img)
    assert np.all(mask_output == mask)


def test_image():
    rgb_img = get_img(width=300, height=200)
    rgb_tagged_data = MockTaggedData("", rgb_img)

    image_ds_object_01 = DataSetObject(rgb_tagged_data)

    assert image_ds_object_01.width == 300
    assert image_ds_object_01.height == 200

    bw_img = get_img(width=300, height=200, bw=True)
    bw_tagged_data = MockTaggedData("", bw_img)

    image_ds_object_03 = DataSetObject(bw_tagged_data)

    assert image_ds_object_03.width == 300
    assert image_ds_object_03.height == 200
