import csv
from pathlib import Path
import cv2
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import shutil
from utils import parse_bbs, to_supervisely_json, get_label
import json

training_all_file = '/home/gilles/datasets/cones/yolov3-training_all.csv'
orig_img_dir = Path('/home/gilles/datasets/cones/YOLO_Dataset')

rows = []
with open(training_all_file) as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        rows.append(row)
