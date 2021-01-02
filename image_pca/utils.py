import matplotlib.pyplot as plt
from .parameters import *


def plot_image_grid(images, num_images_per_row=5):
    """
    Plots and saves the images in a grid in sequential order
    :param images: List of images to be plotted
    :param num_images_per_row: Number of images to plot in a row
    :return: None
    """

    component = 0
    num_rows = len(images) // num_images_per_row
    f, ax = plt.subplots(num_rows, num_images_per_row)

    for i in range(num_rows):
        for j in range(num_images_per_row):
            component += 1
            ax[i, j].imshow(images[i * num_images_per_row + j])
            ax[i, j].set_title(component)
            ax[i, j].axis("off")

        f.set_figheight(20)
        f.set_figwidth(20)

    plt.savefig(f"./results/natural_image_pca/{MAX_PATCHES}.png")
    plt.show()
