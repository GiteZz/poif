import csv
from pathlib import Path

training_all_file = '/home/gilles/datasets/cones/yolov3-training_all.csv'
orig_img_dir = Path('/home/gilles/datasets/cones/YOLO_Dataset')

rows = []
with open(training_all_file) as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        rows.append(row)
