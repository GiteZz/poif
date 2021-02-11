from poif.tests.integration.gitlab.start import GitlabConfig
from poif.tests.integration.gitlab.tools import create_repo, delete_all_projects

delete_all_projects(GitlabConfig())

print(create_repo(GitlabConfig(), "test"))
