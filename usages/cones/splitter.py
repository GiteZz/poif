from pathlib import Path
from collections import defaultdict
import random

from general_loading import rows, orig_img_dir
from utils import parse_bbs, get_label, to_supervisely_json


yolo_ds_folder = Path('/home/gilles/datasets/cones/yolo')
yolo_ds_folder.mkdir(exist_ok=True)

yolo_data_folder = yolo_ds_folder / 'data'


class_count = defaultdict(int)
vid_to_rows = defaultdict(list)

for index in range(5, len(rows)):
    current_row = rows[index]
    file_name = current_row[0]

    file_name_without_extension = file_name.replace('.jpg', '')

    vid_name = '_'.join(file_name_without_extension.split('_')[:2])

    class_count[vid_name] += 1 / len(rows)
    vid_to_rows[vid_name].append(current_row)

print(class_count)

vids = list(class_count.keys())

test_vids = []
test_split = .1
actual_test_split = 0.0
val_vids = []
val_split = .2
actual_val_split = 0.0

while actual_test_split < test_split:
    new_val = random.choice(vids)

    test_vids.append(new_val)
    actual_test_split += class_count[new_val]

    vids.remove(new_val)

while actual_val_split < val_split:
    new_val = random.choice(vids)

    val_vids.append(new_val)
    actual_val_split += class_count[new_val]

    vids.remove(new_val)

with open(yolo_ds_folder / 'train.txt', 'w') as f:
    for vid_name in vids:
        for row in vid_to_rows[vid_name]:
            file_name = row[0]
            f.write(f'{str(yolo_data_folder / file_name)}\n')

print(test_vids)
print(val_vids)
print(vids)

