# -*- coding: utf-8 -*-

# !/usr/bin/python

import os
import sys

from PIL import Image
from tqdm import tqdm

validate_category_max_count = 1;


def detect():
    if len(sys.argv) != 2:
        print('Syntax: {} <dir/>'.format(sys.argv[0]))
        sys.exit(0)

    dir = sys.argv[1]

    categories = os.listdir(dir)
    for category in tqdm(categories, total=len(categories)):
        sub_folder_path = os.path.join(dir, category)

        if os.path.isdir(sub_folder_path):
            for img_file in os.listdir(sub_folder_path):
                if img_file.endswith(".jpg") or img_file.endswith(".jpeg"):
                    img_path = os.path.join(sub_folder_path, img_file)
                    try:
                        img = Image.open(img_path)  # open the image file
                        img.verify()  # verify that it is, in fact an image
                    except (IOError, SyntaxError) as e:
                        os.remove(img_path)
                        print('Removed broken jpg file:', img_path)  # print out the names of corrupt files

    return 0


if __name__ == '__main__':
    detect()
