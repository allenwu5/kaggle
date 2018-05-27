import argparse

# import matplotlib as mpl
import numpy as np
import os
from PIL import Image
from keras.applications.inception_v3 import preprocess_input
from keras.models import load_model
from keras.preprocessing import image
from tqdm import tqdm
import json
import csv

# mpl.use('TkAgg')

# import matplotlib.pyplot as plt

IM_WIDTH = 128
target_size = (IM_WIDTH, IM_WIDTH)
TOP_K = 10

def predict(model, img, target_size):
    """Run model prediction on image
    Args:
      model: keras model
      img: PIL format image
      target_size: (w,h) tuple
    Returns:
      list of predicted labels and their probabilities
    """
    if img.size != target_size:
        img = img.resize(target_size)

    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = preprocess_input(x)
    preds = model.predict(x)
    return preds[0]


def plot_preds(image, preds):
    """Displays image and the top-n predicted probabilities in a bar graph
    Args:
      image: PIL image
      preds: list of predicted labels and their probabilities
    """
    plt.imshow(image)
    plt.axis('off')

    plt.figure()
    index_classes = [x for x in range(0, len(preds))]
    labels = (index_classes)
    plt.barh(index_classes, preds, alpha=0.5)
    plt.yticks(index_classes, labels)
    plt.xlabel('Probability')
    plt.xlim(0, 1.01)
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    a = argparse.ArgumentParser()
    a.add_argument("--model", default="dense121-ft.model")
    a.add_argument("--predict_dir")

    args = a.parse_args()

    assert args.predict_dir, "--predict_dir <the dir includes images going to be predict>"

    with open('validation_class_indices.json', 'r') as fp:
        validation_class_indices = json.load(fp)
        index_to_class = dict((v, k) for k, v in validation_class_indices.items())

    with open("submission.csv", 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=',')
        csv_writer.writerow(["id", "landmarks"])
        csvfile.flush()

        model = load_model(args.model)

        img_paths = {}
        img_cat_folder = {}
        categories = os.listdir(args.predict_dir)
        for category in tqdm(categories, total=len(categories)):
            sub_folder_path = os.path.join(args.predict_dir, category)

            if os.path.isdir(sub_folder_path):
                for img_file in os.listdir(sub_folder_path):
                    if img_file.endswith(".jpg") or img_file.endswith(".jpeg"):
                        img_path = os.path.join(sub_folder_path, img_file)
                        img_id = img_file.split(".")[0]
                        img_paths[img_id] = img_path
                        img_cat_folder[img_id] = category

        for img_id, img_path in tqdm(img_paths.items(), total=len(img_paths)):
            img = Image.open(img_path)

            preds = predict(model, img, target_size)
            # plot_preds(img, preds)
            top1_index = np.argmax(preds, axis=None)
            topK_index = preds.argsort()[-TOP_K:][::-1]

            top1_class = index_to_class[top1_index]
            top1_score = preds[top1_index]
            topK_scores = " ".join([format(preds[x], "10.10f") for x in topK_index])
            csv_writer.writerow(
                [img_id, "{} {} {} {}".format(img_cat_folder[img_id], top1_class, top1_score, topK_scores)])
            csvfile.flush()
