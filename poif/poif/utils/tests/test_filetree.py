from poif.tests import create_standard_folder_structure
from poif.utils.filetree import FileTree


def test_filetree():
    base_dir = create_standard_folder_structure()

    tree = FileTree(base_dir)

    for line in tree.get_lines():
        print(line)

if __name__ == "__main__":
    test_filetree()