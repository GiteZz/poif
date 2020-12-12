from pathlib import Path
import shutil
import json

from general_loading import rows, orig_img_dir
from utils import parse_bbs, get_label, to_supervisely_json


yolo_ds_folder = Path('/home/gilles/datasets/cones/yolo')
yolo_ds_folder.mkdir(exist_ok=True)
yolo_ds_folder = yolo_ds_folder / 'data'
yolo_ds_folder.mkdir(exist_ok=True)


labels_to_int = {
    'blue_cone': 0,
    'yellow_cone': 1,
    'orange_cone': 2
}

labels = ['blue_cone', 'yellow_cone', 'orange_cone']

classes_txt = yolo_ds_folder / 'classes.txt'

with open(classes_txt, 'w') as f:
    for label in labels:
        f.write(label)
        if label != labels[-1]:
            f.write('\n')

for index in range(5, len(rows)):
    current_row = rows[index]
    file_name = current_row[0]

    file_name_without_extension = file_name.replace('.jpg', '')
    img_width = int(current_row[2])
    img_height = int(current_row[3])

    ds_name = '_'.join(file_name.split('_')[:2])

    bbs = current_row[5:]
    bbs = parse_bbs(bbs)

    img_loc = orig_img_dir / file_name
    new_img_loc = yolo_ds_folder / file_name
    new_ann_loc = yolo_ds_folder / f'{file_name_without_extension}.txt'

    shutil.copy(img_loc, new_img_loc)

    with open(new_ann_loc, 'w') as f:
        labels = get_label(img_loc, bbs)
        for bb, label in zip(bbs, labels):
            x = (bb[0] + bb[3] / 2) / img_width
            y = (bb[1] + bb[2] / 2) / img_height
            width = bb[3] / img_width
            height = bb[2] / img_height
            f.write(f'{labels_to_int[label]} {x} {y} {width} {height}')

            if bb != bbs[-1]:
                f.write('\n')
