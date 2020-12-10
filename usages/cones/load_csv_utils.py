def parse_bbs(bbs):
    new_bbs = []
    for bb in bbs:
        if len(bb) == 0:
            break
        del_brackets = bb[1:-1]
        new_bbs.append([int(bb_str) for bb_str in del_brackets.split(',')])
    return new_bbs


def to_supervisely_json(img_width, img_height, bbs):
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

    for bb in bbs:
        start_dict['objects'].append(
            {
                "tags": [],
                "classTitle": "unknown_cone",
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