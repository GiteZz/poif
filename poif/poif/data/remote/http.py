from dataclasses import dataclass

import requests

from poif.data.cache.disk_over_http import GET_FILE_PATH, GET_FILES_PATH

from poif.typing import FileHash


# @dataclass
# class HttpRemote(Remote):
#     datacache_url: str
#     git_url: str
#     git_commit: str
#
#     def get_url_params(self, tag: FileHash):
#         return {
#             'git_commit': self.git_commit,
#             'git_url': self.git_url,
#             'data_tag': tag
#         }
#
#     def get_file(self, tag: FileHash) -> bytes:
#         r = requests.get(f'{self.datacache_url}{GET_FILE_PATH}', params=self.get_url_params(tag))
#         return r.content
#
#     def get_files(self):
#         r = requests.get(f'{self.datacache_url}{GET_FILES_PATH}', params=dvc_origin.to_url_params())
#
#         return r.json()
#
#     def get_object_size(self, tag: FileHash):
#         pass