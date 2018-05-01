import sys
import argparse
import numpy as np
from PIL import Image
import matplotlib as mpl

from keras.preprocessing import image
from keras.models import load_model
from keras.applications.inception_v3 import preprocess_input

mpl.use('TkAgg')

import matplotlib.pyplot as plt

target_size = (229, 229)  # fixed size for InceptionV3 architecture


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

    img_test = "test/00faf8958470eb9a.jpg"  # small green leaf tower - tourist attraction

    # img_{train folder}_{class in model}
    img_9003_0 = "train/9003/d83118ef0291a8a3.jpg"  # Louvre Museum - white - big - horizontal - louvre triangle
    img_9301_5 = "train/9301/c5a836101f701633.jpg"  # cathedral - yellow clock tower
    img_9999_11 = "train/9999/df68277c0b4a1653.jpg"  # Bass Harbor Head Lighthouse

    a.add_argument("--image", help="path to image", default=img_test)
    a.add_argument("--model", default="inceptionv3-ft.model")
    args = a.parse_args()

    if args.image is None and args.image_url is None:
        a.print_help()
        sys.exit(1)

    model = load_model(args.model)
    if args.image is not None:
        img = Image.open(args.image)
        preds = predict(model, img, target_size)
        plot_preds(img, preds)
