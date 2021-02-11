from poif.config.readme import ReadmeConfig
from poif.config.remote.base import RemoteConfig

possible_args = {"remote": RemoteConfig, "readme": ReadmeConfig}


def default(args):
    if args[0] not in possible_args.keys():
        print(
            f"Argument not valid. Valid arguments are: {list(possible_args.keys())}, current argument: {args[0]}"
        )

    config_class = possible_args[args[0]]

    config = config_class.prompt()
    config.save_default()
