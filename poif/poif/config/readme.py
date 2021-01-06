from poif.cli.datasets.tools.cli import yes_with_question
from poif.config.base import Config
from poif.config.remote import RemoteConfig


class ReadmeConfig(Config):
    enable: bool
    enable_filetree: bool
    enable_image_gallery: bool
    image_remote: RemoteConfig = None

    @classmethod
    def get_default_name(cls) -> str:
        return 'readme_config.json'

    @classmethod
    def prompt(cls, default_readme: 'ReadmeConfig' = None) -> 'ReadmeConfig':
        # given readme config has priority
        if default_readme is None:
            default_readme = cls.get_default()

        # If the version loaded from disk is still not loaded
        if default_readme is None:
            default_remote = RemoteConfig.get_default()
        else:
            default_remote = default_readme.image_remote

        default_enable = None if default_readme is None else default_readme.enable
        default_enable_filetree = None if default_readme is None else default_readme.enable_filetree
        default_enable_gallery = None if default_readme is None else default_readme.enable_image_gallery

        enable = yes_with_question("Create readme?", default=default_enable)
        if not enable:
            return ReadmeConfig(enable=False, enable_filetree=False, enable_image_gallery=False)

        enable_filetree = yes_with_question('Add filetree?', default=default_enable_filetree)
        enable_image_gallery = yes_with_question('Add image galley?', default=default_enable_gallery)

        if enable_image_gallery:
            print('Remote for storing the gallery images.')
            image_remote = RemoteConfig.prompt(default_remote)
        else:
            image_remote = None

        return ReadmeConfig(enable=enable,
                            enable_filetree=enable_filetree,
                            enable_image_gallery=enable_image_gallery,
                            image_remote=image_remote
                            )