from poif.config.collection import DataCollectionConfig


def strip_jinja_extension(file_name: str):
    file_name_without_jinja = file_name[:-7]

    return file_name_without_jinja


def render_template_path(path: str, collection_config: DataCollectionConfig):
    without_jinja = strip_jinja_extension(path)
    adjusted_ds_name = without_jinja.replace("_dataset_name_", collection_config.name)

    return adjusted_ds_name
