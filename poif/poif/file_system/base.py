from typing import Union, TYPE_CHECKING

from fuse import FUSE, Operations, FuseOSError

if TYPE_CHECKING:
    from poif.file_system.directory import Directory
    from poif.file_system.file import File


import errno


class DataSetFileSystem(Operations):
    """
    A read only http/https/ftp filesystem.
    """

    def __init__(self, root_dir: 'Directory'):
        self.root_dir = root_dir

    def path_to_object(self, path: str) -> Union['Directory', 'File']:
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