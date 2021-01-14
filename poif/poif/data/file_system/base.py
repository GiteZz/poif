import copy
from typing import Union

from fuse import FUSE, Operations, FuseOSError

from poif.data.file_system.io import Directory, File
from poif.data.file_system.partial import PartialGetWrapper
from poif.data.versioning.dataset import VersionedCollection, RepoVersionedCollection

import errno


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
            self.root_dir.add_tagged_data(PartialGetWrapper(data_point))

    def path_to_object(self, path: str) -> Union[Directory, File]:
        path_parts = path.split('/')
        while len(path_parts) > 0 and len(path_parts[0]) == 0:
            path_parts.pop(0)

        if len(path_parts) == 0:
            # root dir
            return self.root_dir

        try:
            current_object = self.root_dir
            for access_name in path_parts:
                current_object = current_object.contents[access_name]
        except:
            raise FuseOSError(errno.ENOENT)

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
        print("creating")
        return 0

    def write(self, path, buf, size, offset, fip):
        print("writing")
        return 0

    def read(self, path, size, offset, fh):
        print(f'read on path: {path}, size: {size}, offset: {offset}, fh: {fh}')

        if 'autorun.inf' in path:
            return
        if '.' == path[1]:
            return

        object_pointer = self.path_to_object(path)
        return object_pointer.partial_read(offset, size)

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

    git_url = 'https://github.ugent.be/gballege/minimal_pneumonia.git'
    git_commit = '85d749fd6422af1a178013c45c304576939d3b4c'

    fuse = FUSE(
        DataSetFileSystem(
            root_dir=root_dir,
            collection=RepoVersionedCollection(git_url, git_commit)
        ),
        '/home/gilles/fuse_test',
        foreground=True,
        allow_other=False
    )
