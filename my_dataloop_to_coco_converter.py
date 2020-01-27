import os
import json
import numpy as np


path_to_dataloop_images_dir = '/Users/noam/tiny_mice_data/items'
path_to_dataloop_annotations_dir = '/Users/noam/tiny_mice_data/json'

images = [{'file_name': filename,
           'id': i}
          for i, filename in enumerate(os.listdir(path_to_dataloop_images_dir))]

paths_to_dataloop_annotations = [os.path.join(path_to_dataloop_annotations_dir, j) for j in os.listdir(path_to_dataloop_annotations_dir) if 'json' in j]

dataloop_jsons = []
for json_path in paths_to_dataloop_annotations:
    with open(json_path) as jf:
        dataloop_json = json.load(jf)
    dataloop_jsons.append(dataloop_json)
# compute labels to id
labels = []
for single_dataloop_json in dataloop_jsons:
    for annotation in single_dataloop_json['annotations']:
        label = annotation['label']
        labels.append(label)
np_labels = np.array(labels)
class_list = np.unique(np_labels)

label_to_id = {name: i for i, name in enumerate(class_list)}
categories = [{'id': i, 'name': name} for name, i in label_to_id.items()]

# compute annotations
index = 0
annotations = []
for single_dataloop_json in dataloop_jsons:
    filename = single_dataloop_json['filename']
    # find which is the right image and extract the id
    for img in images:
        if img['file_name'] in filename:
            img_id = img['id']
            break

    for annotation in single_dataloop_json['annotations']:
        x = annotation['coordinates'][0]['x']
        y = annotation['coordinates'][0]['y']
        w = annotation['coordinates'][1]['x'] - x
        h = annotation['coordinates'][1]['y'] - y
        label = annotation['label']
        index += 1
        annot = {'bbox': [x, y, w, h],
                 'category_id': label_to_id[label],
                 'image_id': img_id,
                 'iscrowd': 0,
                 'id': index
                 }

        annotations.append(annot)

coco_json = {'images': images,
             'annotations': annotations,
             'categories': categories}

with open('instances_train.json', 'w') as outfile:
    json.dump(coco_json, outfile)

