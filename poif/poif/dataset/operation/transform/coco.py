from typing import List

from poif.dataset.object.annotations import BoundingBox
from poif.dataset.object.base import DataSetObject
from poif.dataset.object.output import detection_output
from poif.dataset.operation.transform.base import Transformation
from poif.typing import RelFilePath
from poif.utils.dataset import tagged_data_to_rel_file_mapping


class SingleCoco(Transformation):
    def __init__(self, annotation_file: RelFilePath, data_folder: RelFilePath):
        self.annotation_file = annotation_file
        self.data_folder = data_folder

    def transform_object_list(self, inputs: List[DataSetObject]) -> List[DataSetObject]:
        mapping = tagged_data_to_rel_file_mapping(inputs)

        annotation_data = mapping[self.annotation_file].get_parsed()

        img_id_to_new_input = {}
        not_found_count = 0
        for image_info in annotation_data["images"]:
            img_id = image_info["id"]

            # The coco annotation file only contains the image name and not the folder, tagged data however
            # includes this data, therefore we need to add it.
            original_filename = self.data_folder
            if self.data_folder != "":
                original_filename += "/"
            original_filename += f'{image_info["file_name"]}'

            if original_filename in mapping:
                img_id_to_new_input[img_id] = DataSetObject(
                    tagged_data=mapping[original_filename], output_function=detection_output
                )

                # TODO find a better solution in the future
                img_id_to_new_input[img_id]._width = int(image_info["width"])
                img_id_to_new_input[img_id]._height = int(image_info["height"])
            else:
                not_found_count += 1

        if not_found_count > 0:
            print(
                f'WARNING: {not_found_count} out of {len(annotation_data["images"])} were not found on disk but '
                f"found in annotation file!"
            )

        for annotation in annotation_data["annotations"]:
            img_id = annotation["image_id"]
            if img_id not in img_id_to_new_input:
                continue
            current_input = img_id_to_new_input[img_id]
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

        return list(img_id_to_new_input.values())
