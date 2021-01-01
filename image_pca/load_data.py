import cv2
import glob
import numpy as np
from sklearn.feature_extraction.image import extract_patches_2d
from .download_data import downloadData
from .parameters import *



def load_overlapping_patches(path):
    image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    image_patches = extract_patches_2d(image=image, patch_size=(PATCH_LEN, PATCH_LEN), max_patches=MAX_PATCHES)
    image_patches = image_patches.reshape(-1, PATCH_LEN * PATCH_LEN)

    return image_patches


def load_image_patches(path='./input/dataset/BSR/BSDS500/data/images/train/'):
    # downloadData()
    images_path_list = glob.glob(f'{path}/*.jpg')

    image_patches = []

    for image_path in images_path_list:
        patches = load_overlapping_patches(image_path)
        image_patches.append(patches)

    image_patches = np.vstack(image_patches)

    return image_patches
