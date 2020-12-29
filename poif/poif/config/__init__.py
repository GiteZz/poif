from pathlib import Path

poif_config_folder = Path.home() / '.poif'
poif_config_folder.mkdir(exist_ok=True)

datasets_default_config_file = poif_config_folder / 'config.json'