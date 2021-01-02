import os
import cv2
import numpy as np


def YUV_read_rame(filename, size):
    height, width = size
    frame_len = width * height * 3 // 2
    shape = (int(height * 1.5), width)

    frames = []
    with open(filename, 'rb') as file:
        while True:
            try:
                raw = file.read(frame_len)
                yuv = np.frombuffer(raw, dtype=np.uint8)
                yuv = yuv.reshape(shape)

                img = cv2.cvtColor(yuv, cv2.COLOR_YUV2BGR_I420, 3)
                frames.append(img)
            except:
                break

    return frames


def display_frames(frames):
    for frame in frames:
        cv2.imshow('f', frame)
        cv2.waitKey(40)


def save_frames(frames, path):
    os.makedirs(path, exist_ok=True)
    for ind, frame in enumerate(frames, 1):
        cv2.imwrite(f'{path}/{ind:03d}.jpg', frame)
