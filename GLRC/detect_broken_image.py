# -*- coding: utf-8 -*-

# !/usr/bin/python

import os
import sys

from PIL import Image
from tqdm import tqdm
from shutil import rmtree


def detect():
    if len(sys.argv) != 2:
        print('Syntax: {} <dir/>'.format(sys.argv[0]))
        sys.exit(0)

    dir = sys.argv[1]

    img_paths = []

    categories = os.listdir(dir)

    print("Create image list\")
    for category in tqdm(categories, total=len(categories)):
        sub_folder_path = os.path.join(dir, category)

        if os.path.isdir(sub_folder_path):
            for img_file in os.listdir(sub_folder_path):
                if img_file.endswith(".jpg") or img_file.endswith(".jpeg"):
                    img_path = os.path.join(sub_folder_path, img_file)
                    img_paths.append(img_path)

    print("Remove broken jpg file")
    for img_path in tqdm(img_paths, total=len(img_paths)):
        try:
            img = Image.open(img_path)  # open the image file
            img.load()
        except (IOError, SyntaxError) as e:
            os.remove(img_path)
            print('Removed broken jpg file:', img_path)  # print out the names of corrupt files

    print("Remove empty folder")
    for category in tqdm(categories, total=len(categories)):
        sub_folder_path = os.path.join(dir, category)

        if os.path.isdir(sub_folder_path):
            has_no_img = True
            for img_file in os.listdir(sub_folder_path):
                if img_file.endswith(".jpg") or img_file.endswith(".jpeg"):
                    has_no_img = False
                    break

            if has_no_img:
                rmtree(sub_folder_path)
                print('Removed empty folder:', sub_folder_path)

    return 0


if __name__ == '__main__':
    detect()
