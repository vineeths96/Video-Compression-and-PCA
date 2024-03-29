from sklearn.decomposition import PCA
from .load_data import load_image_patches
from .utils import plot_image_grid
from .parameters import *


def natural_image_pca(path="./input/BSR/BSDS500/data/images/train/"):
    """
    Calculates the PCA of natural images and plots the weights
    :return: None
    """

    data = load_image_patches(path)

    image_pca = PCA(n_components=PCA_COMPONENTS)
    image_pca.fit(data)
    pca_weights = []

    for ind, pca_component in enumerate(image_pca.components_, 1):
        image = pca_component.reshape(PATCH_LEN, PATCH_LEN)
        pca_weights.append(image)

    plot_image_grid(pca_weights)
