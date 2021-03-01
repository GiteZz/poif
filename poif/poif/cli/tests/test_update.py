from poif.cli.commands.init import configured_init
from poif.cli.commands.update import configured_update
from poif.config.package import PackageConfig
from poif.config.readme import ReadmeConfig
from poif.config.repo import DataRepoConfig
from poif.config.tests.test_remote_config import get_dummy_remote_config
from poif.packaging import PackageOptions
from poif.tagged_data.repo import RepoData
from poif.tests import MockTaggedRepo, write_image_in_file
from poif.tests.repo import create_data_collection
from poif.typing import FileHash, RelFilePath
from poif.utils import FileIterator
from poif.versioning.dataset import ResourceDirCollection


def test_update(monkeypatch):
    base_dir, collection_config = create_data_collection(get_dummy_remote_config())

    files_in_base_dir = list(FileIterator(base_dir))

    readme_config = ReadmeConfig(
        enable=True,
        enable_filetree=True,
        enable_image_gallery=False,
        image_remote=None,
    )

    package_config = PackageConfig(type=PackageOptions.python_package)

    repo_config = DataRepoConfig(collection=collection_config, readme=readme_config, package=package_config)

    mock_repo = MockTaggedRepo()
    # mock_git = MockGitRepo(None, None)

    monkeypatch.setattr(
        "poif.cli.commands.update.get_remote_repo_from_config",
        lambda x: mock_repo,
    )
    monkeypatch.setattr(
        "poif.cli.commands.init.get_remote_repo_from_config",
        lambda x: mock_repo,
    )

    configured_init(base_dir, repo_config, "")

    count_before_update = len(mock_repo.remote.uploaded_files)
    assert count_before_update > len(files_in_base_dir)

    class MonkeyResourceDirCollection(ResourceDirCollection):
        def create_repo_file(self, relative_path: RelFilePath, tag: FileHash) -> RepoData:
            data = super().create_repo_file(relative_path, tag)
            data.repo = mock_repo
            return data

    monkeypatch.setattr(
        "poif.cli.commands.update.ResourceDirCollection",
        lambda x: MonkeyResourceDirCollection(x),
    )

    monkeypatch.setattr(
        "poif.cli.commands.update.get_remote_repo_from_config",
        lambda x: mock_repo,
    )

    configured_update(base_dir)

    count_after_update = len(mock_repo.remote.uploaded_files)

    assert count_before_update == count_after_update

    write_image_in_file(base_dir / "train" / "mask" / "00.jpg")

    configured_update(base_dir)

    count_after_one_file_change = len(mock_repo.remote.uploaded_files)

    assert count_after_one_file_change == count_after_update + 2

    with open(base_dir / "meta.json", "w") as f:
        f.write("[1]")

    configured_update(base_dir)

    count_after_two_file_changes = len(mock_repo.remote.uploaded_files)

    assert count_after_one_file_change + 1 == count_after_two_file_changes
