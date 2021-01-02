from image_compression.compress import compress, decompress, plot_performance
from image_compression.downsample_compress_upsample import downsample_compress, decompress_upsample, plot_downsample_compress_upsample_performance
from image_compression.utils import plot_comparision

print("Compressing to H.264 Video")
compress('./input/pa1_25fps.yuv')
print("Decompressing from H.264 Video")
decompress()
print("Plotting performance")
compress_performance = plot_performance()

print("Downsampling and Compressing to H.264")
downsample_compress('./input/pa1_25fps.yuv')
print("Decompressing from H.264 and upsampling")
decompress_upsample()
print("Plotting performance")
downsample_compress_upsample_performance = plot_downsample_compress_upsample_performance()

print("Plotting comparision")
plot_comparision(compress_performance, downsample_compress_upsample_performance)
