import random

from poif.dataset.detection.detection import detection_collection_to_coco_dict
from poif.dataset.tests.test_tagged_data import MockTaggedData
from poif.input.detection import  DetectionAnnotation, DetectionInput
from poif.tests import get_img


def get_random_annotation(img_width=1280, img_height=720, amount_of_classes=3):
    min_width = img_width // 8
    min_height = img_height // 8

    class_id = random.randint(0, amount_of_classes - 1)
    x = random.randint(0, img_width - 1 - min_width) / img_width
    y = random.randint(0, img_height - 1 - min_height) / img_height
    w = random.randint(0, img_width - x) / img_width
    h = random.randint(0, img_height - y) / img_height

    return DetectionAnnotation(category_id=class_id, x=x, y=y, w=w, h=h)


def detection_collection(image_count=3,
                                  max_annotations_per_image=5,
                                  img_width=1280,
                                  img_height=720,
                                  amount_of_classes=3
                                  ):
    images = [DetectionInput(image=MockTaggedData(f'{i}.jpg', get_img()), img_width=img_width, img_height=img_height) for i in range(image_count)]
    for image in images:
        for _ in range(random.randint(0, max_annotations_per_image - 1)):
            image.add_annotation(get_random_annotation(img_width=img_width,
                                                       img_height=img_height,
                                                       amount_of_classes=amount_of_classes)
                                 )


    return images

def test_coco():
    coco_dict = detection_collection_to_coco_dict(images)
    MockTaggedData