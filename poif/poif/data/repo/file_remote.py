from poif.data.datapoint.base import TaggedData
from poif.data.remote.base import FileRemote
from poif.data.repo.base import TaggedRepo


class FileRemoteTaggedRepo(TaggedRepo):
    remote: FileRemote
    data_folder: str

    def get_remote_name(self, data: TaggedData):
        return f'{self.data_folder}/{data.tag[:2]}/{data.tag[2:]}'

    def get(self, data: TaggedData) -> bytes:
        return self.remote.download(self.get_remote_name(data))

    def get_object_size(self, data: TaggedData):
        return self.remote.get_object_size(self.get_remote_name(data))

    def upload(self, data: TaggedData):
        self.remote.upload(data.get(), self.get_remote_name(data))