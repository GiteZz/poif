from typing import List, Dict
from pathlib import Path
from collections import defaultdict
import uuid
from datasets.tools.minio import upload_datasets_images
img_extensions = ['.png', '.jpg', '.jpeg']


def collect_images(data_folders: List[Path]) -> Dict[str, List[Path]]:
    # Folder as key, with path to file as value
    image_files = defaultdict(list)
    for data_folder in data_folders:
        for img_extension in img_extensions:
            for img in data_folder.glob(f'*{img_extension}'):
                image_files[str(img.parent)].append(img)

    return image_files


def create_readme(options):
    data_folders = options['data_folders']
    images_by_dir = collect_images(data_folders)
    s3_images_path = Path(uuid.uuid4().hex)

    image_pairs = []
    markdown_pairs = []
    for image_dir, images in images_by_dir.items():
        selected_images = [images[0]]
        for selected_image in selected_images:
            s3_name = s3_images_path / selected_image.parts[-1]

            image_pairs.append((selected_image, s3_name))
            s3_endpoint = options['s3_endpoint'] + '/' if options['s3_endpoint'][-1] != '/' else ''
            http_path = f'{s3_endpoint}{options["s3_bucket"]}-images/{s3_images_path}/{selected_image.parts[-1]}'

            markdown_pairs.append((str(selected_image)[len(str(Path.cwd())):], http_path))

    upload_datasets_images(options, image_pairs)

    with open('README.md', 'w') as f:
        for markdown_pair in markdown_pairs:
            f.write(f'## {markdown_pair[0]} \n')
            f.write(f'![text]({markdown_pair[1]})')


if __name__ == "__main__":
    imgs = create_readme({'s3_endpoint': 'http://datasets.backend.jhub.be', 's3_bucket': 'datasets', 'data_folders': [Path('/home/gilles/test_datasets/dogs_vs_cats/data')]})

