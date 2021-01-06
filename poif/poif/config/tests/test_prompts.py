from poif.config import ReadmeConfig, RemoteConfig, S3Config
from poif.tests import MonkeyPatchSequence


def test_s3_prompt(monkeypatch):
    input_returns = MonkeyPatchSequence(['bucket', 'url', 'profile'])
    monkeypatch.setattr('builtins.input', input_returns)
    config1 = S3Config.prompt()

    assert config1.bucket == 'bucket'
    assert config1.url == 'url'
    assert config1.profile == 'profile'

    input_returns = MonkeyPatchSequence(['', '', ''])
    monkeypatch.setattr('builtins.input', input_returns)
    config2 = S3Config.prompt(default=config1)

    assert config2.bucket == 'bucket'
    assert config2.url == 'url'
    assert config2.profile == 'profile'


def test_remote_config(monkeypatch):
    input_returns = MonkeyPatchSequence(['S3', 'bucket', 'url', 'profile'])
    monkeypatch.setattr('builtins.input', input_returns)
    config1 = RemoteConfig.prompt()

    assert config1.remote_type == 'S3'
    assert config1.config.bucket == 'bucket'
    assert config1.config.url == 'url'
    assert config1.config.profile == 'profile'


    input_returns = MonkeyPatchSequence(['S3', '', '', ''])
    monkeypatch.setattr('builtins.input', input_returns)
    config2 = RemoteConfig.prompt(default=config1)

    assert config2.remote_type == 'S3'
    assert config2.config.bucket == 'bucket'
    assert config2.config.url == 'url'
    assert config2.config.profile == 'profile'


