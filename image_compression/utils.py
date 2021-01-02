import cv2
import glob
import numpy as np
import matplotlib.pyplot as plt


def load_frames(path):
    """
    Loads all the images in a directory as a list of frames
    :param path: Directory of images
    :return: List of frames
    """

    files = glob.glob(f"{path}/*.jpg")

    files.sort()
    frames = []
    for file in files:
        frame = cv2.imread(file)
        frames.append(frame)

    return frames


def down_sample(frames):
    """
    Downsample a list of frames by a factor of 2
    :param frames: List of frames
    :return: Downsampled frames
    """

    downsampled_frames = []
    for frame in frames:
        downsampled_frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
        downsampled_frames.append(downsampled_frame)

    return downsampled_frames


def up_sample(frames):
    """
    Upsample a list of frames by a factor of 2
    :param frames: List of frames
    :return: Upsampled frames
    """

    upsampled_frames = []
    for frame in frames:
        upsampled_frame = cv2.resize(frame, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        upsampled_frames.append(upsampled_frame)

    return upsampled_frames


def luma_mse_image_pair(first_image, second_image):
    """
    Calculates the MSE in luminance between two images
    :param first_image: First image
    :param second_image: Second image
    :return: MSE in luminance
    """

    firstImage = cv2.imread(first_image)
    firstImage_yuv = cv2.cvtColor(firstImage, cv2.COLOR_BGR2YUV)
    firstImage_y, _, _ = cv2.split(firstImage_yuv)

    secondImage = cv2.imread(second_image)
    secondImage_yuv = cv2.cvtColor(secondImage, cv2.COLOR_BGR2YUV)
    secondImage_y, _, _ = cv2.split(secondImage_yuv)

    return np.mean(np.square(firstImage_y - secondImage_y))


def luma_mse(first_path, second_path):
    """
    Calculates the average MSE in luminance between images in two directories
    :param first_path: Directory for first set of images
    :param second_path: Directory for second set of images
    :return: MSE averaged over all images
    """

    first_path_images = glob.glob(f"{first_path}/*.jpg")
    second_path_images = glob.glob(f"{second_path}/*.jpg")

    first_path_images.sort()
    second_path_images.sort()

    MSE = 0
    for first_image, second_image in zip(first_path_images, second_path_images):
        MSE += luma_mse_image_pair(first_image, second_image)

    return MSE / len(first_path_images)


def plot_mse(MSE, directory=""):
    """
    Plots the MSE vs Bitrate graph
    :param MSE: Dictionary with Bitrate - MSE as key - value pairs
    :param directory: Directory where plot has to be saved
    :return: None
    """

    plt.figure()
    plt.plot(MSE.keys(), MSE.values())
    plt.xlabel("Bitrate in Kbps")
    plt.ylabel("Mean Squared Error (MSE)")
    plt.title("MSE vs Bitrate")
    plt.savefig(f"./results/image_compression_and_resolution/{directory}/performance.png")
    plt.show()


def plot_comparision(firstMSE, secondMSE):
    """
    Plots the two MSE vs Bitrate graph for comparision
    :param firstMSE: First dictionary with Bitrate - MSE as key - value pairs
    :param secondMSE: Second dictionary with Bitrate - MSE as key - value pairs
    :return: None
    """

    plt.figure()
    plt.plot(firstMSE.keys(), firstMSE.values(), label="Compress - Decompress")
    plt.plot(secondMSE.keys(), secondMSE.values(), label="Downsample - Compress - Decompress - Upsample")
    plt.xlabel("Bitrate in Kbps")
    plt.ylabel("Mean Squared Error (MSE)")
    plt.title("MSE vs Bitrate")
    plt.legend()
    plt.savefig("./results/image_compression_and_resolution/comparision.png")
    plt.show()
