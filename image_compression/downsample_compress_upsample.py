import os
from .readFrame import YUV_read_rame, display_frames, save_frames
from .utils import load_frames, down_sample, up_sample, luma_mse, plot_mse
from .parameters import *


def downsample_compress(filename):
    frames = YUV_read_rame(filename, (HEIGHT, WIDTH))
    # display_frames(frames)

    frames = down_sample(frames)
    path = f".{filename.split('.')[1]}_downsampled"
    save_frames(frames, path)
    total_frames = len(os.listdir(path))

    """To know more about keyint, min-keyint ,no-scenecut check over at https://video.stackexchange.com/a/24684"""
    for bitrate in range(BITRATE_START, BITRATE_END, BITRATE_STEP):
        os.system(f"ffmpeg -hide_banner -loglevel panic -i {path}/%03d.jpg -b:v {bitrate}k -c:v libx264 -x264-params keyint=300:min-keyint=300:no-scenecut=1:bframes=0 -c:a copy -y ./results/image_compression_and_resolution/downsample_compress_upsample/{bitrate}.h264")
        frame_details = os.popen(f"ffprobe -hide_banner -loglevel panic -show_frames ./results/image_compression_and_resolution/downsample_compress_upsample/{bitrate}.h264 | grep pict_type")

        I_frame_count = 0
        P_Frame_count = 0
        for line in frame_details:
            type = line.rstrip().split('=')[-1]

            if type == 'I':
                I_frame_count += 1
            else:
                P_Frame_count += 1

        print(f"I Frame Count: {I_frame_count}, P Frame Count: {P_Frame_count}, Total Frames: {total_frames}")


def decompress_upsample():
    for bitrate in range(BITRATE_START, BITRATE_END, BITRATE_STEP):
        os.makedirs(f'./results/image_compression_and_resolution/downsample_compress_upsample/{bitrate}/', exist_ok=True)
        os.system(f"ffmpeg -hide_banner -loglevel panic -i ./results/image_compression_and_resolution/downsample_compress_upsample/{bitrate}.h264 -qscale:v 2 ./results/image_compression_and_resolution/downsample_compress_upsample/{bitrate}/%03d.jpg")

    for bitrate in range(BITRATE_START, BITRATE_END, BITRATE_STEP):
        frames = load_frames(f'./results/image_compression_and_resolution/downsample_compress_upsample/{bitrate}/')
        frames = up_sample(frames)
        save_frames(frames, f'./results/image_compression_and_resolution/downsample_compress_upsample/{bitrate}_upsampled/')


def plot_downsample_compress_upsample_performance():
    MSE = {}
    for bitrate in range(100, 1001, 100):
        first_path = './input/pa1_25fps'
        second_path = f'./results/image_compression_and_resolution/downsample_compress_upsample/{bitrate}_upsampled/'
        MSE[bitrate] = luma_mse(first_path, second_path)

    plot_mse(MSE, 'downsample_compress_upsample')

    return MSE
