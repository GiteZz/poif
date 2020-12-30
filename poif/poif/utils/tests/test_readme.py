from pathlib import Path

from poif.utils.readme import ReadmeSection, FileTreeSection


def test_readme():
    ds_folder = Path('/home/gilles/datasets/pneunomia')
    data_folders = ['train', 'test', 'val']

    readme = ReadmeSection(title='Pneunomia dataset')
    file_trees_section = ReadmeSection(title='Data directories')
    readme.add_section(file_trees_section)

    for data_folder in data_folders:
        base_dir = ds_folder / data_folder
        single_file_tree = FileTreeSection(base_dir)
        file_trees_section.add_section(single_file_tree)

    readme.write_to_file(ds_folder / 'README.md')