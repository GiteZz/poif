from typing import Dict, List

from poif.dataset.detection.base import DetectionDataset
from poif.dataset.object.annotations import BoundingBox
from poif.dataset.object.detection import DetectionInput
from poif.tagged_data.base import TaggedData
from poif.typing import DatasetType, RelFilePath


class CocoDetectionDataset(DetectionDataset):
    def __init__(
        self,
        annotation_files: Dict[DatasetType, RelFilePath] = None,
        data_folders: Dict[DatasetType, RelFilePath] = None,
    ):
        super().__init__()

        self.annotation_files = annotation_files
        self.data_folders = data_folders

    def get_rel_file_mapping(self, inputs: List[TaggedData]) -> Dict[RelFilePath, TaggedData]:
        mapping = {}
        for tagged_data in inputs:
            mapping[tagged_data.relative_path] = tagged_data

        return mapping

    def parse_annotation_file(
        self, dataset_type: str, inputs: List[TaggedData], data_folder: str
    ) -> List[DetectionInput]:
        """
        data
        """
        mapping = self.get_rel_file_mapping(inputs)

        annotation_data = mapping[self.annotation_files[dataset_type]].get_parsed()

        new_inputs = {}
        not_found_count = 0
        for image_info in annotation_data["images"]:
            img_id = image_info["id"]

            # The coco annotation file only contains the image name and not the folder, tagged data however
            # includes this data, therefore we need to add it.
            original_filename = self.data_folders[dataset_type]
            if data_folder != "":
                original_filename += "/"
            original_filename += f'{image_info["file_name"]}'

            if original_filename in mapping:
                new_inputs[img_id] = DetectionInput(
                    tagged_data=mapping[original_filename],
                    width=int(image_info["width"]),
                    height=int(image_info["height"]),
                )
            else:
                not_found_count += 1
                #
        if not_found_count > 0:
            print(
                f'WARNING: {not_found_count} out of {len(annotation_data["images"])} were not found on disk but '
                f"found in annotation file!"
            )
        for annotation in annotation_data["annotations"]:
            img_id = annotation["image_id"]
            if img_id not in new_inputs:
                continue
            current_input = new_inputs[img_id]
            x, y, w, h = annotation["bbox"]

            category_id = annotation["category_id"]

            current_input.add_bounding_box(
                BoundingBox(
                    label=category_id,
                    x=int(x) / current_input.width,
                    y=int(y) / current_input.height,
                    w=int(w) / current_input.width,
                    h=int(h) / current_input.height,
                )
            )

        # class 'dict'>: {'supercategory': 'person', 'id': 1, 'name': 'person'}

        for category in annotation_data["categories"]:
            self.category_mapping[category["id"]] = category["name"]

        return new_inputs.values()

    def form(self, data: List[TaggedData]):
        sub_dataset_names = list(self.annotation_files.keys())

        for subset in sub_dataset_names:
            new_objects = self.parse_annotation_file(subset, data, self.data_folders[subset])
            self.objects.extend(new_objects)
            self.splits[subset] = new_objects

        self.next_operation()


def detection_collection_to_coco_dict(inputs: List[DetectionInput]) -> Dict:
    coco_dict = {}
    coco_dict["images"] = []
    coco_dict["annotations"] = []
    for index, detection_input in enumerate(inputs):
        coco_dict["images"].append(
            {
                "file_name": detection_input.data.relative_path,
                "id": index,
                "width": detection_input.width,
                "height": detection_input.height,
            }
        )
        for bbox in detection_input.annotations:
            coco_dict["annotations"].append(
                {
                    "image_id": index,
                    "bbox": bbox.coco_bbox(detection_input.width, detection_input.height),
                    "category_id": bbox.label,
                }
            )

    return coco_dict
