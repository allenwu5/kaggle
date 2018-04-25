# -*- coding: utf-8 -*-

# !/usr/bin/python

# Note: requires the tqdm package (pip install tqdm)

# Note to Kagglers: This script will not run directly in Kaggle kernels. You
# need to download it and run it on your local machine.

# Downloads images from the Google Landmarks dataset using multiple threads.
# Images that already exist will not be downloaded again, so the script can
# resume a partially completed download. All images will be saved in the JPG
# format with 90% compression quality.

import sys, os, multiprocessing, csv
from urllib import request, error
from PIL import Image
from io import BytesIO
import tqdm


def parse_data(data_file):
    csvfile = open(data_file, 'r')
    csvreader = csv.reader(csvfile)
    id_url_cat_list = [line[:3] for line in csvreader]
    return id_url_cat_list[1:]  # Chop off header


def download_image(id_url_cat):
    out_dir = sys.argv[2]

    if len(id_url_cat) >= 3:
        (id, url, cat) = id_url_cat
    else:
        (id, url) = id_url_cat
        cat = ""

    sub_folder = os.path.join(out_dir, cat)
    if not os.path.exists(sub_folder):
        os.mkdir(sub_folder)
    filename = os.path.join(sub_folder, '{}.jpg'.format(id))

    if os.path.exists(filename):
        print('Image {} already exists. Skipping download.'.format(filename))
        return 0

    try:
        response = request.urlopen(url)
        image_data = response.read()
    except:
        print('Warning: Could not download image {} from {}'.format(id, url))
        return 1

    try:
        pil_image = Image.open(BytesIO(image_data))
    except:
        print('Warning: Failed to parse image {}'.format(id))
        return 1

    try:
        pil_image_rgb = pil_image.convert('RGB')
    except:
        print('Warning: Failed to convert image {} to RGB'.format(id))
        return 1

    try:
        pil_image_rgb.save(filename, format='JPEG', quality=90)
    except:
        print('Warning: Failed to save image {}'.format(filename))
        return 1

    return 0


def loader():
    if len(sys.argv) != 3:
        print('Syntax: {} <data_file.csv> <output_dir/>'.format(sys.argv[0]))
        sys.exit(0)
    (data_file, out_dir) = sys.argv[1:]

    id_url_cat_list = parse_data(data_file)
    pool = multiprocessing.Pool(processes=4)  # Num of CPUs
    failures = sum(tqdm.tqdm(pool.imap_unordered(download_image, id_url_cat_list), total=len(id_url_cat_list)))
    print('Total number of download failures:', failures)
    pool.close()
    pool.terminate()


# arg1 : data_file.csv
# arg2 : output_dir
if __name__ == '__main__':
    loader()
