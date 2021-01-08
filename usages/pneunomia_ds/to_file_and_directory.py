from poif.data.datapoint.base import TaggedData
from poif.data.file_system.io import Directory, File
from poif.data.versioning.dataset import RepoVersionedCollection
from collections import defaultdict
from typing import List, Union

git_url = 'https://github.ugent.be/gballege/minimal_pneumonia'
git_commit = '59384bc93c29feaf775c051d6421ead9d76388f7'

collection = RepoVersionedCollection(git_url, git_commit)
data_points = collection.get_files()

root_dir = Directory()

for data_point in data_points:
    root_dir.add_tagged_data(data_point)

a = 5


