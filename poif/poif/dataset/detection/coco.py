from typing import Dict, List, Optional

from poif.dataset.detection.base import DetectionDataset
from poif.dataset.object.annotations import BoundingBox
from poif.dataset.object.base import DataSetObject
from poif.dataset.object.output import detection_output
from poif.tagged_data.base import TaggedData
from poif.typing import DatasetType, RelFilePath


class CocoDetectionDataset(DetectionDataset):
    def __init__(
        self,
        annotation_file: Optional[RelFilePath] = None,
        data_folder: Optional[RelFilePath] = None,
        annotation_files: Optional[Dict[DatasetType, RelFilePath]] = None,
        data_folders: Optional[Dict[DatasetType, RelFilePath]] = None,
    ):
        super().__init__()

        self._single_input = annotation_file is not None and data_folder is not None
        self._multi_input = annotation_files is not None and data_folders is not None

        if annotation_file is not None and data_folder is None:
            raise Exception("Only the annotation_file is provided, the data_folder is missing")

        if annotation_file is not None and data_folder is None:
            raise Exception("Only the data_folder is provided, the annotation_file is missing")

        if annotation_files is not None and data_folders is None:
            raise Exception("Only the annotation_files is provided, the data_folders is missing")

        if annotation_files is not None and data_folders is None:
            raise Exception("Only the data_folders is provided, the annotation_files is missing")

        if self._single_input and self._multi_input:
            raise Exception(
                "Either supply single dataset information (annotation_file and data_folder) or multi dataset information (annotation_files and data_folders)"
            )

        self.annotation_file = annotation_file
        self.data_folder = data_folder

        self.annotation_files = annotation_files
        self.data_folders = data_folders

    def get_rel_file_mapping(self, inputs: List[TaggedData]) -> Dict[RelFilePath, TaggedData]:
        mapping = {}
        for tagged_data in inputs:
            mapping[tagged_data.relative_path] = tagged_data

        return mapping

    def parse_annotation_file(
        self, annotation_file: str, data_folder: str, inputs: List[TaggedData]
    ) -> List[DataSetObject]:
        """
        data
        """
        mapping = self.get_rel_file_mapping(inputs)

        annotation_data = mapping[annotation_file].get_parsed()

        new_inputs = {}
        not_found_count = 0
        for image_info in annotation_data["images"]:
            img_id = image_info["id"]

            # The coco annotation file only contains the image name and not the folder, tagged data however
            # includes this data, therefore we need to add it.
            original_filename = data_folder
            if data_folder != "":
                original_filename += "/"
            original_filename += f'{image_info["file_name"]}'

            if original_filename in mapping:
                new_inputs[img_id] = DataSetObject(
                    tagged_data=mapping[original_filename], output_function=detection_output
                )

                # TODO find a better solution in the future
                new_inputs[img_id]._width = int(image_info["width"])
                new_inputs[img_id]._height = int(image_info["height"])
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

            current_input.add_annotation(
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

        return list(new_inputs.values())

    def form(self, data: List[TaggedData]):
        if self._single_input:
            assert self.annotation_file is not None and self.data_folder is not None
            new_objects = self.parse_annotation_file(self.annotation_file, self.data_folder, data)
            self.objects = new_objects
        elif self._multi_input:
            assert self.annotation_files is not None
            sub_dataset_names = list(self.annotation_files.keys())

            for subset in sub_dataset_names:
                annotation_file = self.annotation_files[subset]
                data_folder = self.data_folders[subset]
                new_objects = self.parse_annotation_file(annotation_file, data_folder, data)

                self.objects.extend(new_objects)
                self.splits[subset] = new_objects

        self.next_operation()


def detection_collection_to_coco_dict(inputs: List[DataSetObject], label_mapping: Dict[int, str]) -> Dict:
    coco_dict = {}
    coco_dict["images"] = []
    coco_dict["annotations"] = []
    coco_dict["categories"] = []
    for index, detection_input in enumerate(inputs):
        coco_dict["images"].append(
            {
                "file_name": detection_input.relative_path,
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
