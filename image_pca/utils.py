import matplotlib.pyplot as plt


def plot_image_grid(images, num_images_per_row=5):
    component = 0
    num_rows = len(images) // num_images_per_row
    f, ax = plt.subplots(num_rows, num_images_per_row)

    for i in range(num_rows):
        for j in range(num_images_per_row):
            component += 1
            ax[i, j].imshow(images[i * num_images_per_row + j])
            ax[i, j].set_title(component)
            ax[i, j].axis('off')

        f.set_figheight(20)
        f.set_figwidth(20)

    plt.savefig("./results/natural_image_pca.png")
    plt.show()
