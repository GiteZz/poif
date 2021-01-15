Referenced from [here](https://towardsdatascience.com/image-data-labelling-and-annotation-everything-you-need-to-know-86ede6c684b1#:~:text=YOLO%3A%20In%20YOLO%20labeling%20format,object%20coordinates%2C%20height%20and%20width.).

# Object detectors

## YOLO

General dataset format. For each image a annotation file is created whereby the .jpg extension is replaced with the .txt extension.

**Filetree:**
```
train
 - img25.jpg
 - img25.txt
 - img36.jpg
 - img36.txt
 - ...

val
 - img12.jpg
 - img12.txt
 - img23.jpg
 - img23.txt
```

Each line in the annotation files follow this format

```
<object-class> <x> <y> <width> <height>
```

The x, y, width and height are float values relative to the width and height

So if img36.jpg would have 4 objects from 3 classes this would be the annotation file:

```
0 20 30 100 400
```

### YOLOv2 and YOLOv3 (Darknet)

[Reference](https://manivannan-ai.medium.com/how-to-train-yolov2-to-detect-custom-objects-9010df784f36)

Example for dog and cat detector.

Meta files
```python

```