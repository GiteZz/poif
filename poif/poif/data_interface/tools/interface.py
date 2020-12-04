import jinja2
from pathlib import Path
from poif.data_interface.tools.config import DatasetConfig
import subprocess


def create_interface(dataset_config: DatasetConfig, git_add=True, git_commit=False):
    template_path = Path(__file__).parents[1] / 'templates' / 'project_interface'

    jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_path))

    for file in template_path.glob('**/*.jinja2'):
        rel_file = str(file)[len(str(template_path)) + 1:]
        rendered_file = jinja_env.get_template(rel_file).render(data=dataset_config.to_dict())
        new_file_loc = Path.cwd() / 'project_interface' / rel_file[:-7]
        new_file_loc.parent.mkdir(exist_ok=True, parents=True)

        with open(new_file_loc, 'w') as f:
            f.write(rendered_file)

    if git_add:
        subprocess.call(['git', 'add', '--all', 'project_interface/'])

    if git_commit:
        subprocess.call(['git', 'commit', '-m', '"Added project_interface"'])