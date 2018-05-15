# -*- coding: utf-8 -*-

# !/usr/bin/python

import os
import sys

from tqdm import tqdm

validate_category_max_count = 3;


def split():
    if len(sys.argv) != 3:
        print('Syntax: {} <train_dir/> <validate_dir/>'.format(sys.argv[0]))
        sys.exit(0)

    (train_dir, validate_dir) = sys.argv[1:]

    categories = os.listdir(train_dir)
    for category in tqdm(categories, total=len(categories)):
        train_sub_folder_path = os.path.join(train_dir, category)
        validate_sub_folder_path = os.path.join(validate_dir, category)

        if os.path.isdir(train_sub_folder_path):
            if not os.path.exists(validate_sub_folder_path):
                os.makedirs(validate_sub_folder_path)

            validate_img_count = 0
            for img_file in os.listdir(validate_sub_folder_path):
                if img_file.endswith(".jpg") or img_file.endswith(".jpeg"):
                    validate_img_count += 1

            for img_file in os.listdir(train_sub_folder_path):
                if img_file.endswith(".jpg") or img_file.endswith(".jpeg"):
                    img_path = os.path.join(train_sub_folder_path, img_file)
                    if validate_img_count < validate_category_max_count:
                        os.rename(img_path, os.path.join(validate_sub_folder_path, img_file))
                        validate_img_count += 1
                    else:
                        break

    return 0


if __name__ == '__main__':
    split()
