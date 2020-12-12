from pathlib import Path
import shutil
import json

from general_loading import rows, orig_img_dir
from utils import parse_bbs, get_label, to_supervisely_json


supervisely_project_folder = Path('/home/gilles/datasets/cones/supervisely')
supervisely_project_folder.mkdir(exist_ok=True)

meta_file = supervisely_project_folder / 'meta.json'
ex_path = Path(__file__).parent
shutil.copy(ex_path / 'cone_meta.json', meta_file)

for index in range(5, len(rows)):
    current_row = rows[index]
    file_name = current_row[0]
    width = int(current_row[2])
    height = int(current_row[3])

    ds_name = '_'.join(file_name.split('_')[:2])

    ds_folder = supervisely_project_folder / ds_name
    ds_folder.mkdir(exist_ok=True)

    annotation_folder = ds_folder / 'ann'
    annotation_folder.mkdir(exist_ok=True)
    img_folder = ds_folder / 'img'
    img_folder.mkdir(exist_ok=True)

    bbs = current_row[5:]
    bbs = parse_bbs(bbs)

    img_loc = orig_img_dir / file_name
    new_img_loc = img_folder / file_name
    new_ann_loc = annotation_folder / f'{file_name}.json'

    shutil.copy(img_loc, new_img_loc)

    with open(new_ann_loc, 'w') as f:
        labels = get_label(img_loc, bbs)
        json.dump(to_supervisely_json(width, height, bbs, labels), f, indent=4)
