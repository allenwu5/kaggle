# -*- coding: utf-8 -*-

# !/usr/bin/python

import json
import os
import sys
from multiprocessing import Manager, Pool
from shutil import rmtree

from PIL import Image
from tqdm import tqdm

PROCESS_COUNT = 4
img_paths = []
valid_images = Manager().list()  # <-- can be shared between processes.


def detect_one_image(process_index):
    img_path = img_paths[process_index]
    if img_path in valid_images:
        return

    try:
        img = Image.open(img_path)  # open the image file
        img.load()
        valid_images.append(img_path)
    except (IOError, SyntaxError) as e:
        os.remove(img_path)
        print('Removed broken jpg file:', img_path)  # print out the names of corrupt files


def detect():
    if len(sys.argv) != 2:
        print('Syntax: {} <dir/>'.format(sys.argv[0]))
        sys.exit(0)

    dir = sys.argv[1]

    categories = os.listdir(dir)

    print("Create image list")
    for category in tqdm(categories, total=len(categories)):
        sub_folder_path = os.path.join(dir, category)

        if os.path.isdir(sub_folder_path):
            for img_file in os.listdir(sub_folder_path):
                if img_file.endswith(".jpg") or img_file.endswith(".jpeg"):
                    img_path = os.path.join(sub_folder_path, img_file)
                    img_paths.append(img_path)

    if os.path.exists('valid_images.json'):
        with open('valid_images.json', 'r') as fp:
            for f in json.load(fp):
                valid_images.append(f)

    print("Remove broken jpg file")
    with Pool(processes=PROCESS_COUNT) as p:
        max_ = len(img_paths)
        with tqdm(total=max_) as pbar:
            for i, _ in enumerate(p.imap_unordered(detect_one_image, range(0, max_))):
                pbar.update()

        with open('valid_images.json', 'w') as fp:
            pure_list = []
            for f in valid_images:
                pure_list.append(f)
            json.dump(pure_list, fp, sort_keys=True, indent=4)

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
