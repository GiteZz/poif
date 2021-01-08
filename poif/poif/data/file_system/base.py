import copy
from typing import Union

from fuse import FUSE, Operations

from poif.data.file_system.io import Directory, File
from poif.data.versioning.dataset import VersionedCollection, RepoVersionedCollection


class DataSetFileSystem(Operations):
    """
    A read only http/https/ftp filesystem.
    """

    def __init__(self, root_dir: Directory, collection: VersionedCollection):
        f = open("/home/gilles/datasets/pneunomia/test/NORMAL/IM-0001-0001.jpeg", "rb")
        num = bytearray(f.read())

        self.file = num

        self.root_dir = root_dir

        data_points = collection.get_files()

        for data_point in data_points:
            self.root_dir.add_tagged_data(data_point)

    def path_to_object(self, path: str) -> Union[Directory, File]:
        path_parts = path.split('/')
        while len(path_parts) > 0 and len(path_parts[0]) == 0:
            path_parts.pop(0)

        if len(path_parts) == 0:
            # root dir
            return self.root_dir

        current_object = self.root_dir
        for access_name in path_parts:
            current_object = current_object.contents[access_name]

        return current_object

    def readdir(self, path, fh):
        print(f'Read path: {path}')
        object_pointer = self.path_to_object(path)

        return ['.', '..'] + list(object_pointer.contents.keys())

    def getattr(self, path, fh=None):
        print(f'getattr on path {path}')

        object_pointer = self.path_to_object(path)
        return object_pointer.get_attr()

    def unlink(self, path):
        return 0

    def create(self, path, mode, fi=None):
        return 0

    def write(self, path, buf, size, offset, fip):
        return 0

    def read(self, path, size, offset, fh):
        print(f'read on path: {path}, size: {size}, offset: {offset}, fh: {fh}')

        if 'autorun.inf' in path:
            return
        if '.' == path[1]:
            return
        if path == '/Hello':
            return bytes(self.file[offset: offset + size])

    def destroy(self, path):
        return 0


if __name__ == "__main__":
    # img_dir = Directory({'01.jpg': File(), '02.jpg': File()})
    # mask_dir = Directory({'03.jpg': File(), '04.jpg': File()})
    #
    # train_dir = Directory({'mask': mask_dir, 'image': img_dir})
    #
    # root_dir = Directory({'train': train_dir, 'val': copy.deepcopy(train_dir)})

    root_dir = Directory()

    git_url = 'https://github.ugent.be/gballege/minimal_pneumonia'
    git_commit = '59384bc93c29feaf775c051d6421ead9d76388f7'

    fuse = FUSE(
        DataSetFileSystem(
            root_dir=root_dir,
            collection=RepoVersionedCollection(git_url, git_commit)
        ),
        '/home/gilles/fuse_test',
        foreground=True,
        allow_other=False
    )
