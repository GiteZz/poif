from typing import Dict, List

from poif.dataset.object.annotations import BoundingBox
from poif.dataset.object.base import DataSetObject


def detection_collection_to_coco_dict(inputs: List[DataSetObject], label_mapping: Dict[int, str]) -> Dict:
    coco_dict: Dict[str, list] = {}
    coco_dict["images"] = []
    coco_dict["annotations"] = []
    coco_dict["categories"] = []
    for index, detection_input in enumerate(inputs):
        coco_dict["images"].append(
            {
                "file_name": detection_input.relative_path.split("/")[-1],
                "id": index,
                "width": detection_input.width,
                "height": detection_input.height,
            }
        )
        for object_annotation in detection_input.annotations:
            if isinstance(object_annotation, BoundingBox):
                coco_dict["annotations"].append(
                    {
                        "image_id": index,
                        "bbox": object_annotation.coco_bbox(detection_input.width, detection_input.height),
                        "category_id": object_annotation.label,
                    }
                )

    for label_id, label_name in label_mapping.items():
        coco_dict["categories"].append({"id": label_id, "name": label_name})

    return coco_dict
