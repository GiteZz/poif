from poif.file_system import Directory
from poif.versioning.dataset import GitRepoCollection

git_url = 'https://github.ugent.be/gballege/minimal_pneumonia'
git_commit = '59384bc93c29feaf775c051d6421ead9d76388f7'

collection = GitRepoCollection(git_url, git_commit)
data_points = collection.get_files()

root_dir = Directory()

for data_point in data_points:
    # self.root_dir.add_tagged_data(data_point)
    print(data_point.size)

a = 5


