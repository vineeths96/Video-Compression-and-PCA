import cv2
import glob
import numpy as np
import matplotlib.pyplot as plt


def load_frames(path):
    files = glob.glob(f'{path}/*.jpg')

    files.sort()
    frames = []
    for file in files:
        frame = cv2.imread(file)
        frames.append(frame)

    return frames


def down_sample(frames):
    downsampled_frames = []
    for frame in frames:
        downsampled_frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_CUBIC)
        downsampled_frames.append(downsampled_frame)

    return downsampled_frames


def up_sample(frames):
    upsampled_frames = []
    for frame in frames:
        upsampled_frame = cv2.resize(frame, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        upsampled_frames.append(upsampled_frame)

    return upsampled_frames


def luma_mse_image_pair(first_image, second_image):
    firstImage = cv2.imread(first_image)
    firstImage_yuv = cv2.cvtColor(firstImage, cv2.COLOR_BGR2YUV)
    firstImage_y, _, _ = cv2.split(firstImage_yuv)

    secondImage = cv2.imread(second_image)
    secondImage_yuv = cv2.cvtColor(secondImage, cv2.COLOR_BGR2YUV)
    secondImage_y, _, _ = cv2.split(secondImage_yuv)

    return np.mean(np.square(firstImage_y - secondImage_y))


def luma_mse(first_path, second_path):
    first_path_images = glob.glob(f'{first_path}/*.jpg')
    second_path_images = glob.glob(f'{second_path}/*.jpg')

    first_path_images.sort()
    second_path_images.sort()

    MSE = 0
    for first_image, second_image in zip(first_path_images, second_path_images):
        MSE += luma_mse_image_pair(first_image, second_image)

    return MSE


def plot_mse(MSE, folder=''):
    plt.figure()
    plt.plot(MSE.keys(), MSE.values())
    plt.xlabel('Bitrate in Kbps')
    plt.ylabel('Mean Squared Error (MSE)')
    plt.title('MSE vs Bitrate')
    plt.savefig(f'./results/image_compression_and_resolution/{folder}/performance.png')
    plt.show()


def plot_comparision(firstMSE, secondMSE):
    plt.figure()
    plt.plot(firstMSE.keys(), firstMSE.values(), label='Compress - Decompress')
    plt.plot(secondMSE.keys(), secondMSE.values(), label='Downsample - Compress - Decompress - Upsample')
    plt.xlabel('Bitrate in Kbps')
    plt.ylabel('Mean Squared Error (MSE)')
    plt.title('MSE vs Bitrate')
    plt.legend()
    plt.savefig('./results/image_compression_and_resolution/comparision.png')
    plt.show()
