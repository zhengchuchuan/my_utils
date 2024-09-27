import os
import re

import cv2
import numpy as np
import spectral as spy

from tqdm import tqdm
from skimage.registration import phase_cross_correlation

from file_operation.gather_file_paths import gather_file_paths


def set_byte_order(hdr_file):
    with open(hdr_file, mode='r', encoding='utf-8') as f:
        lines = f.readlines()
    with open(hdr_file, mode='w', encoding='utf-8') as f:
        for line in lines:
            if "Date" in line or "byte order" in line or "project class" in line or len(line) == 0:
                continue
            f.write(line)
        f.writelines("\nbyte order = 0")


def open_hdr_img(src_file):
    """
    读取hdr格式的图像文件。
    src_file (str): hdr文件的路径。
    """
    try:
        set_byte_order(src_file)
        scr_img = spy.open_image(src_file)
        return scr_img[:, :, :]
    except IOError as e:
        print(f"无法读取文件：{src_file}，错误信息：{e}")
        return None  # 或者你可以根据需要返回其他值




def bands_align(image):
    std_image = image[:, :, 2] # R通道
    offset_image = image[:, :, 3] # 850nm通道
    h,w,c = image.shape

    aligned_img = image.copy()
    shift, error, diffphase = phase_cross_correlation(std_image, offset_image)
    ty, tx = shift
    # 仿射变换,填充黑色
    aligned_img[:, :, 3] = cv2.warpAffine(offset_image, np.float32([[1, 0, tx], [0, 1, ty]]), dsize=(w, h),
                                          borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    return aligned_img

if __name__ == '__main__':
    # 合成的图像保存路径
    save_dir = r'\\192.168.3.155\高光谱测试样本库\原油检测\00大庆现场测试\03标注数据以及模型文件\00数据和标签\dataset_one_label\test\negative\tif'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)
    # 处理的文件路径
    txt_file_paths = None
    file_directories = None
    txt_file_paths = [
        # r'C:\Users\zcc\project\python_project\my_utils\data_list\20240902_temp.txt'
    ]
    file_directories =  [
        r'\\192.168.3.155\高光谱测试样本库\原油检测\00大庆现场测试\03标注数据以及模型文件\00数据和标签\dataset_one_label\test\negative\images'
    ]
    # 获取文件路径列表
    get_list_extension = ['.png']
    file_path_list = gather_file_paths(txt_paths=txt_file_paths,directories=file_directories, extensions=get_list_extension)


    for bgr_path in tqdm(file_path_list, desc="Processing images"):
        hdr_path = bgr_path.replace('.png', '.hdr')
        bgr = cv2.imdecode(np.fromfile(bgr_path, dtype=np.uint8), cv2.IMREAD_COLOR)
        spectral = open_hdr_img(hdr_path)
        if spectral is not None:
            # 向彩色传感器图像对齐

            channel_850 = spectral[:,:,6]
            # 从16位图像转换为8位图像
            channel_850 = (channel_850 / 65535 * 255).astype(np.uint8)
            # 通道拼接BGR + 850nm
            synthesis_image = np.dstack((bgr, channel_850))



            # 波段对齐
            aligned_data = bands_align(synthesis_image)


            #保存多通道图像为tif格式
            tif_save_path = os.path.join(save_dir, os.path.basename(bgr_path).replace('.png', '.tif'))
            cv2.imencode('.tif', aligned_data)[1].tofile(tif_save_path)

        else:
            print(f"无法处理文件：{hdr_path}")


