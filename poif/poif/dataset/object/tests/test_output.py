import numpy as np

from poif.dataset.object.base import DataSetObject
from poif.dataset.object.output import classification_output
from poif.tagged_data.tests.mock import MockTaggedData
from poif.tests import get_img


def test_classification_output():
    img = get_img()

    image_data = MockTaggedData("", img)

    image_ds_object = DataSetObject(image_data, output_function=classification_output)
    image_ds_object.label = 5

    img_output, label = image_ds_object.output()

    assert np.all(img_output == img)
    assert label == 5
