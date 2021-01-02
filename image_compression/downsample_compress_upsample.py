import os
from .read_frame import YUV_read_frame, display_frames, save_frames
from .utils import load_frames, down_sample, up_sample, luma_mse, plot_mse
from .parameters import *


def downsample_compress(filename):
    """
    Downsamples (spatially by 2) and compress the specified file with H.264 compression and saves it in the
    results directory (One I frame and rest P frames)
    :param filename: YUV file to be compressed
    :return: None
    """

    # Reads YUV file as frames and saves it in a directory
    frames = YUV_read_frame(filename, (HEIGHT, WIDTH))
    # display_frames(frames)

    frames = down_sample(frames)
    path = f".{filename.split('.')[1]}_downsampled"
    save_frames(frames, path)
    total_frames = len(os.listdir(path))

    """To know more about keyint, min-keyint, no-scenecut check over at https://video.stackexchange.com/a/24684"""

    """
    Reads image frames from the 'path' directory, creates and saves a H.264 file with the specified bit rate
    '-i' specifies the input directory where images are saved as three digit integers sequentially
    '-b:v' specifies the bitrate to tbe used when compressing
    '-c:v' specified the video codec to be used H.264 (libx264)
    '-c:a' specifies the audio codec to be copied from original
    '-x264-params' like 'keyint', 'min-keyint', 'no-scenecut' are chosen so as to have one I frame and rest P frame 
    Last provide the output file path
    'hide-banner' and 'loglevel panic' options are for setting the logging to minimum
    """
    for bitrate in range(BITRATE_START, BITRATE_END, BITRATE_STEP):
        os.system(
            f"ffmpeg -hide_banner -loglevel panic -i {path}/%03d.jpg -b:v {bitrate}k -c:v libx264 "
            f"-x264-params keyint=300:min-keyint=300:no-scenecut=1:bframes=0 -c:a copy -y "
            f"./results/image_compression_and_resolution/downsample_compress_upsample/{bitrate}.h264"
        )

        # Check the frame types and print stats for the compressed file
        frame_details = os.popen(
            f"ffprobe -hide_banner -loglevel panic -show_frames "
            f"./results/image_compression_and_resolution/downsample_compress_upsample/{bitrate}.h264 | grep pict_type"
        )

        I_frame_count = 0
        P_Frame_count = 0
        for line in frame_details:
            type = line.rstrip().split("=")[-1]

            if type == "I":
                I_frame_count += 1
            else:
                P_Frame_count += 1

        print(f"I Frame Count: {I_frame_count}, P Frame Count: {P_Frame_count}, Total Frames: {total_frames}")


def decompress_upsample():
    """
    Decompresses a H.264 file into frames and saves it in a directory
    Frames are upsampled and saved in the upsampled directory
    :return: None
    """

    for bitrate in range(BITRATE_START, BITRATE_END, BITRATE_STEP):
        os.makedirs(
            f"./results/image_compression_and_resolution/downsample_compress_upsample/{bitrate}/", exist_ok=True
        )
        os.system(
            f"ffmpeg -hide_banner -loglevel panic -i "
            f"./results/image_compression_and_resolution/downsample_compress_upsample/{bitrate}.h264 "
            f"-qscale:v 2 ./results/image_compression_and_resolution/downsample_compress_upsample/{bitrate}/%03d.jpg"
        )

    for bitrate in range(BITRATE_START, BITRATE_END, BITRATE_STEP):
        frames = load_frames(f"./results/image_compression_and_resolution/downsample_compress_upsample/{bitrate}/")
        frames = up_sample(frames)
        save_frames(
            frames, f"./results/image_compression_and_resolution/downsample_compress_upsample/{bitrate}_upsampled/"
        )


def plot_downsample_compress_upsample_performance():
    """
    Plots the performance in terms of MSE and saves it
    :return: None
    """

    MSE = {}
    for bitrate in range(100, 1001, 100):
        first_path = "./input/pa1_25fps"
        second_path = f"./results/image_compression_and_resolution/downsample_compress_upsample/{bitrate}_upsampled/"
        MSE[bitrate] = luma_mse(first_path, second_path)

    plot_mse(MSE, "downsample_compress_upsample")

    return MSE
