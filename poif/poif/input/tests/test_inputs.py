from poif.dataset.base import MultiDataset
from poif.input.annotations import Mask
from poif.input.base import DataSetObject
from poif.input.mask import SingleMaskObject
from poif.tagged_data.tests.mock import MockTaggedData
from poif.tests import get_img

import numpy as np


def test_mask():
    img = get_img()
    mask = get_img()

    image_data = MockTaggedData('', img)
    mask_data = MockTaggedData('', mask)

    image_ds_object = SingleMaskObject(image_data)
    image_ds_object.annotations.append(Mask(mask_data))

    ds = MultiDataset(input_type=SingleMaskObject)
    ds.form_from_ds_objects([image_ds_object])

    img_output, mask_output = ds[0]

    assert np.all(img_output == img)
    assert np.all(mask_output == mask)