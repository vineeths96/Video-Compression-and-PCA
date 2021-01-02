import os
from .readFrame import YUV_read_rame, display_frames, save_frames
from .utils import luma_mse, plot_mse
from .parameters import *


def compress(filename):
    frames = YUV_read_rame(filename, (HEIGHT, WIDTH))
    # display_frames(frames)

    path = f".{filename.split('.')[1]}"
    save_frames(frames, path)
    total_frames = len(os.listdir(path))

    """To know more about keyint, min-keyint ,no-scenecut check over at https://video.stackexchange.com/a/24684"""
    for bitrate in range(BITRATE_START, BITRATE_END, BITRATE_STEP):
        os.system(f"ffmpeg -hide_banner -loglevel panic -i {path}/%03d.jpg -b:v {bitrate}k -c:v libx264 -x264-params keyint=300:min-keyint=300:no-scenecut=1:bframes=0 -c:a copy -y ./results/image_compression_and_resolution/compress/{bitrate}.h264")
        frame_details = os.popen(f"ffprobe -hide_banner -loglevel panic -show_frames ./results/image_compression_and_resolution/compress/{bitrate}.h264 | grep pict_type")

        I_frame_count = 0
        P_Frame_count = 0
        for line in frame_details:
            type = line.rstrip().split('=')[-1]

            if type == 'I':
                I_frame_count += 1
            else:
                P_Frame_count += 1

        print(f"I Frame Count: {I_frame_count}, P Frame Count: {P_Frame_count}, Total Frames: {total_frames}")


def decompress():
    for bitrate in range(BITRATE_START, BITRATE_END, BITRATE_STEP):
        os.makedirs(f'./results/image_compression_and_resolution/compress/{bitrate}/', exist_ok=True)
        os.system(f"ffmpeg -hide_banner -loglevel panic -i ./results/image_compression_and_resolution/compress/{bitrate}.h264 -qscale:v 2 ./results/image_compression_and_resolution/compress/{bitrate}/%03d.jpg")


def plot_performance():
    MSE = {}
    for bitrate in range(BITRATE_START, BITRATE_END, BITRATE_STEP):
        first_path = './input/pa1_25fps'
        second_path = f'./results/image_compression_and_resolution/compress/{bitrate}/'
        MSE[bitrate] = luma_mse(first_path, second_path)

    plot_mse(MSE, 'compress')

    return MSE
