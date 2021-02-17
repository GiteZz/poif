import typing
from dataclasses import dataclass

from tqdm import tqdm

from poif.repo.base import TaggedRepo

if typing.TYPE_CHECKING:
    from poif.config.remote.base import RemoteConfig
    from poif.remote.base import FileRemote
    from poif.tagged_data import TaggedData
    from poif.versioning.dataset import VersionedCollection


@dataclass
class FileRemoteTaggedRepo(TaggedRepo):
    remote: "FileRemote"
    data_folder: str

    def get_remote_name(self, tag: str):
        remote_name = f"{self.data_folder}/{tag[:2]}/{tag[2:]}"
        return remote_name

    def get_from_tag(self, tag: str):
        return self.remote.download(self.get_remote_name(tag))

    def get_object_size_from_tag(self, tag: str):
        return self.remote.get_object_size(self.get_remote_name(tag))

    def upload(self, data: "TaggedData"):
        self.remote.upload(data.get(), self.get_remote_name(data.tag))

    def upload_collection(self, collection: "VersionedCollection"):
        for tagged_data in tqdm(collection.get_tagged_data(), desc="Uploading files"):
            self.upload(tagged_data)


def get_remote_repo_from_config(remote_config: "RemoteConfig"):
    remote = remote_config.config.get_configured_remote()

    return FileRemoteTaggedRepo(remote=remote, data_folder=remote_config.data_folder)
