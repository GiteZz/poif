from poif.git.repo import GitRepo
from poif.tests import create_standard_folder_structure, get_temp_path


def test_repo():
    base_dir = create_standard_folder_structure()

    repo = GitRepo(base_dir=base_dir, init=True)
    repo.commit("Dummy message")
    latest_hash = repo.get_latest_hash()

    assert len(latest_hash) == 40


def test_has_remote():
    base_dir = get_temp_path()
    repo = GitRepo(base_dir=base_dir, init=True)
    assert not repo.has_remote()
    repo.add_remote("hello.world")
    assert repo.has_remote()
