import numpy as np

from my_utils.data_processing.data_processing import linear_normalize


def convert_tif_to_png(tif_channel):
    """
    读取CHW类型的tif数据,后去其前三个通道转换为png文件的格式后返回
    :param tif_channel:tif图像的RGB三通道的数组
    :return:png格式数据
    """
    # 取tif前3通道BGR
    png_array = tif_channel[:3, :, :]
    # 值映射到255,uint8
    png_array = linear_normalize(png_array, 0, 255, np.uint8)
    # 变换为RGB通道
    png_array[[0, 2], :, :] = png_array[[2, 0], :, :]
    return png_array
