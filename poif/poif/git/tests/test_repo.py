from poif.git.repo import GitRepo
from poif.tests import create_standard_folder_structure


def test_repo():
    base_dir = create_standard_folder_structure()

    repo = GitRepo(base_dir=base_dir, init=True)
    repo.commit("Dummy message")
    latest_hash = repo.get_latest_hash()

    assert len(latest_hash) == 40
