from typing import List, Dict
from pathlib import Path
from collections import defaultdict
import uuid
from poif.data_interface.tools.cli import s3_input
from poif.data_interface.tools.minio import upload_datasets_images
from poif.data_interface.tools.config import DatasetConfig
from poif.data_interface.tools import folder_list_to_pathlib, get_url
import subprocess
img_extensions = ['.png', '.jpg', '.jpeg']


def collect_images(data_folders: List[Path]) -> Dict[str, List[Path]]:
    # Folder as key, with path to file as value
    image_files = defaultdict(list)
    for data_folder in data_folders:
        for img_extension in img_extensions:
            for img in data_folder.rglob(f'*{img_extension}'):
                image_files[str(img.parent)].append(img)

    return image_files


def create_readme(dataset_config: DatasetConfig, git_add=True, git_commit=False):
    if dataset_config.readme_s3 is None:
        print('Configure S3 for image storage, this host the images placed in the readme and should therefore be publicly accessible.')
        dataset_config.readme_s3 = s3_input(
            default_bucket='datasets-images',
            default_profile=dataset_config.dvc_s3.profile,
            default_endpoint=dataset_config.dvc_s3.endpoint
        )
        dataset_config.save()

    data_folders = dataset_config.data_folders
    print(data_folders)
    images_by_dir = collect_images(folder_list_to_pathlib(data_folders))
    print(images_by_dir)
    s3_images_path = Path(uuid.uuid4().hex)

    image_pairs = []
    markdown_pairs = []
    for image_dir, images in images_by_dir.items():
        selected_images = [images[0]]
        for selected_image in selected_images:
            s3_name = s3_images_path / selected_image.parts[-1]

            image_pairs.append((selected_image, s3_name))
            s3_endpoint = get_url(dataset_config.readme_s3.endpoint)
            http_path = f'{s3_endpoint}{dataset_config.readme_s3.bucket}/{s3_images_path}/{selected_image.parts[-1]}'

            markdown_pairs.append((str(selected_image)[len(str(Path.cwd())):], http_path))

    upload_datasets_images(dataset_config.readme_s3, image_pairs)

    with open('README.md', 'w') as f:
        for markdown_pair in markdown_pairs:
            f.write(f'## {markdown_pair[0]} \n')
            f.write(f'![text]({markdown_pair[1]})\n')

    if git_add:
        subprocess.call(['git', 'add', 'README.md'])
    if git_add and git_commit:
        subprocess.call(['git', 'commit', '-m', '"Added README"'])


if __name__ == "__main__":
    imgs = create_readme({'s3_endpoint': 'http://datasets.backend.jhub.be', 's3_bucket': 'daif', 'data_folders': [Path('/home/gilles/test_datasets/dogs_vs_cats/data')]})

