from poif.config.collection import DataCollectionConfig
from poif.tests import create_standard_folder_structure
from poif.utils.readme import DatasetReadme


def test_readme():
    base_dir = create_standard_folder_structure()

    collection_config = DataCollectionConfig(
        name="dummy", files=[], folders=["train", "test", "val"], data_remote=None
    )
    readme = DatasetReadme(base_dir=base_dir, config=collection_config)

    readme.write_to_folder(base_dir)
