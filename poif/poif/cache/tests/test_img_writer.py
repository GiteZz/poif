from poif.cache.base import CacheManager
from poif.dataset.object.base import DataSetObject
from poif.tagged_data.tests.mock import ImageMockTaggedData
from poif.tests import get_temp_path


def test_png_img_writer():
    base_dir = get_temp_path()
    manager = CacheManager(base_dir)

    tagged_data = ImageMockTaggedData(relative_path="img.png")

    assert manager.get(tagged_data.tag) is None

    ds_object = DataSetObject(tagged_data)
    ds_object.add_cache_manager(manager)
    object_bytes = ds_object.get()  # This load the object into the cache
    assert manager.get(ds_object.tag) == object_bytes


def test_jpg_img_writer():
    base_dir = get_temp_path()
    manager = CacheManager(base_dir)

    tagged_data = ImageMockTaggedData(relative_path="img.jpg")

    assert manager.get(tagged_data.tag) is None

    ds_object = DataSetObject(tagged_data)
    ds_object.add_cache_manager(manager)
    object_bytes = ds_object.get()  # This load the object into the cache
    assert manager.get(ds_object.tag) == object_bytes
