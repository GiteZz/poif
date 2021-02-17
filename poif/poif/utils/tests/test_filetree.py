from poif.tests import create_standard_folder_structure
from poif.utils.filetree import FileTree


def test_filetree():
    base_dir = create_standard_folder_structure()

    tree = FileTree(base_dir)

    expected_lines = [
        base_dir.parts[-1],
        "  - test",
        "    - image",
        "      - 00.jpg",
        "      - 01.jpg",
        "      - ...",
        "    - mask",
        "      - 00.jpg",
        "      - 01.jpg",
        "      - ...",
        "    - test_meta.json",
        "  - train",
        "    - image",
        "      - 00.jpg",
        "      - 01.jpg",
        "      - ...",
        "    - mask",
        "      - 00.jpg",
        "      - 01.jpg",
        "      - ...",
        "    - train_meta.json",
        "  - val",
        "    - image",
        "      - 00.jpg",
        "      - 01.jpg",
        "      - ...",
        "    - mask",
        "      - 00.jpg",
        "      - 01.jpg",
        "      - ...",
        "    - val_meta.json",
        "  - meta.json",
    ]

    for line, expected_line in zip(tree.get_lines(), expected_lines):
        assert line == expected_line


if __name__ == "__main__":
    test_filetree()
