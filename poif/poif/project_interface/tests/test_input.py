from poif.project_interface.classes.input import Input
from poif.project_interface.classes.location import StringLocation

def test_setting_data():
    meta_data = {
        'file_name': '01.jpg',
        'rel_file_path': 'test/img_rgb'
    }
    new_input = Input(meta_data)

    img = "Image"
    mask = "Mask"

    img_location = StringLocation(data_tag='aa', data_str=img)
    mask_location = StringLocation(data_tag='bb', data_str=mask)

    new_input.data.image = img_location
    new_input.data.mask = mask_location

    assert new_input.data.image == img_location
    assert new_input.data.mask == mask_location

    input2 = Input(meta_data)
    input2.data = img_location

    assert input2.data == img_location