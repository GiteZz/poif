from poif.cli.commands.init import init
from poif.config.tests.test_prompts import get_repo_sequence
from poif.tests import (
    MockGitRepo,
    MockTaggedRepo,
    MonkeyPatchSequence,
    create_data_folder,
    get_temp_path,
    write_image_in_file,
)


def test_init(monkeypatch):
    temp_dir = get_temp_path()

    sequence, config = get_repo_sequence()
    monkeypatch.setattr("builtins.input", MonkeyPatchSequence(sequence + ["git_url"]))

    for data_folder in config.collection.folders:
        create_data_folder(temp_dir / data_folder)

    for file in config.collection.files:
        write_image_in_file(temp_dir / file)

    mock_repo = MockTaggedRepo()
    # mock_git = MockGitRepo(None, None)

    monkeypatch.setattr(
        "poif.cli.commands.init.get_remote_repo_from_config",
        lambda x: mock_repo,
    )
    monkeypatch.setattr("poif.cli.commands.init.GitRepo", MockGitRepo)

    init([str(temp_dir)])
