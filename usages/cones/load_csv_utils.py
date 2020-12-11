import numpy as np
from pathlib import Path
import cv2

def parse_bbs(bbs):
    new_bbs = []
    for bb in bbs:
        if len(bb) == 0:
            break
        del_brackets = bb[1:-1]
        new_bbs.append([int(bb_str) for bb_str in del_brackets.split(',')])
    return new_bbs


def get_crops(img, bbs):
    return [img[bb[1]:bb[1] + bb[3], bb[0]:bb[0] + bb[2]] for bb in bbs]


def get_label(image_path: Path, bbs):
    vid_name = image_path.parts[-1]
    if vid_name == 'vid_31':
        return ['orange_cone'] * len(bbs)
    img = cv2.imread(str(image_path))
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    crops = get_crops(img, bbs)
    labels = []

    for crop in crops:
        std_crop = np.std(crop, axis=-1)
        crop_foreground = std_crop > np.mean(std_crop)

        crop_background = np.logical_not(np.repeat(np.expand_dims(crop_foreground, axis=-1), 3, axis=-1))

        crop_without_background = np.array(crop, copy=True)
        crop_without_background[crop_background] = 0

        #     foreground = np.ma.masked_where(np.logical_not(crop_background), crop)

        red_score = np.mean(crop[:, :, 0][crop_foreground])
        green_score = np.mean(crop[:, :, 1][crop_foreground])
        blue_score = np.mean(crop[:, :, 2][crop_foreground])

        yellow_score = (red_score + green_score) / 2
        labels.append('blue_cone' if blue_score > yellow_score else 'yellow_cone')

    return labels


def to_supervisely_json(img_width, img_height, bbs, labels):
    start_dict = {
        "description": "",
        "tags": [],
        "size": {
            "height": img_height,
            "width": img_width
        },
        "objects": [

        ]
    }

    for bb, label in zip(bbs, labels):
        start_dict['objects'].append(
            {
                "tags": [],
                "classTitle": label,
                "geometryType": "rectangle",
                "points": {
                    "exterior": [
                        [
                            bb[0],
                            bb[1]
                        ],
                        [
                            bb[0] + bb[2],
                            bb[1] + bb[3]
                        ]
                    ],
                    "interior": []
                }
            }
        )

    return start_dict