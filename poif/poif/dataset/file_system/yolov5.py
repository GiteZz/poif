from click import Path

from poif.dataset.base import MultiDataset
from poif.dataset.file_system.base import FileSystemCreator
from poif.file_system.directory import Directory


class Yolov5FileSystem(FileSystemCreator):
    def create(self, dataset: MultiDataset, base_dir: Path):
        dataset_dir = Directory()

        data_folder = {"train": base_folder / "images" / "train", "val": base_folder / "images" / "val"}

        label_folder = {"train": base_folder / "labels" / "train", "val": base_folder / "labels" / "val"}

        sorted_ids = self.get_classes_sorted_by_id()
        needed_information = {
            "number_of_classes": len(sorted_ids),
            "classes": sorted_ids,
            "train_folder": str(data_folder["train"]),
            "val_folder": str(data_folder["val"]),
        }

        yolov5_template = get_datasets_template_dir() / "detection" / "yolov5.yaml.jinja2"

        template = Template(open(yolov5_template).read())
        rendered_template = template.render(data=needed_information)

        dataset_dir.add_data("meta.yaml", StringBinaryData(rendered_template))

        for subset in ["train", "val"]:
            for object_index, ds_object in enumerate(self.splits[subset].objects):
                original_extension = ds_object.relative_path.split("/")[-1].split(".")[-1]
                file_name = str(data_folder[subset] / f"{object_index}.{original_extension}")

                dataset_dir.add_data(file_name, StringBinaryData(rendered_template))

                label = detection_input_to_yolo_annotation(ds_object)
                label_name = str(label_folder[subset] / f"{object_index}.txt")
                dataset_dir.add_data(label_name, StringBinaryData(label))

        dataset_dir.setup_as_filesystem(base_folder, daemon=True)
