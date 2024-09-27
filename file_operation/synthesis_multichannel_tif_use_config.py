import os
import re

import cv2
import numpy as np
import spectral as spy
from tqdm import tqdm

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

def read_align_config(align_config_path):
    """
    读取对齐配置文件
    """
    align_config_list = []
    with open(align_config_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('#'):
                continue  # 跳过以 # 开头的行
            if line:
                row = line.split(',')
                # 过滤掉空字符串并转换为整数
                values = [int(value) for value in row if value.strip()]
                align_config_list.append(values)
        # 计算相对于jpg的波段偏移
        if len(align_config_list) > 0:
            bgr_offests = align_config_list[0].copy()
            for offset in align_config_list:
                offset[0] -= bgr_offests[0]
                offset[1] -= bgr_offests[1]

    return align_config_list

def bands_align(img, config_params):
    """
    # JPG,450,550,650,720,750,800,850
    -3,-2,
    4,-9,
    -9,-9,
    6,-1,
    0,0,
    -4,1,
    11,0,
    -1,11,
    """
    # 将图像列表转换为numpy数组
    img = np.array(img)
    h, w, c = img.shape
    aligned_img = np.zeros_like(img)
    # Separate handling for RGB channels (last 3 channels)
    for i in range(c):
        band = img[:, :, i]
        # 处理jpg
        # bgr + 850nm
        if c == 4:
            # 跳过bgr
            if i < 3 :
                aligned_img[:, :, i] = band
            # 850波段向bgr对齐
            if i == 3:
                tx, ty = config_params[7]
                # 仿射变换,填充黑色
                aligned_img[:, :, i] = cv2.warpAffine(band, np.float32([[1, 0, -tx], [0, 1, -ty]]), dsize=(w, h),
                                                  borderMode=cv2.BORDER_CONSTANT, borderValue=0)
    return aligned_img

if __name__ == '__main__':
    # 合成的图像保存路径
    save_dir = r'\\192.168.3.155\高光谱测试样本库\原油检测\00大庆现场测试\03标注数据以及模型文件\00数据和标签\dataset_one_label\test\ground truth\4_channel_tif'
    # 读取的配置文件
    align_config_path_old = r'\\192.168.3.155\高光谱测试样本库\原油检测\00大庆现场测试\01数据\align_old\align.conf'
    align_config_path_new = r'\\192.168.3.155\高光谱测试样本库\原油检测\00大庆现场测试\01数据\align_513\align.conf'
    # 处理的文件路径
    txt_file_paths = None
    file_directories = None
    txt_file_paths = [
        # r'C:\Users\zcc\project\python_project\my_utils\data_list\20240902_temp.txt'
    ]
    file_directories =  [
        r'\\192.168.3.155\高光谱测试样本库\原油检测\00大庆现场测试\03标注数据以及模型文件\00数据和标签\dataset_one_label\test\ground truth\images'
    ]
    # 获取文件路径列表
    get_list_extension = ['.png']
    file_path_list = gather_file_paths(txt_paths=txt_file_paths,directories=file_directories, extensions=get_list_extension)

    # 读取对齐参数
    align_config_list_old = read_align_config(align_config_path_old)
    align_config_list_new = read_align_config(align_config_path_new)

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


            # 不同日期的图像选择不同的对齐参数
            match = re.search(r'MAX_(\d+)_', bgr_path)
            if match:
                date_str = match.group(1)  # 提取日期部分，如 '20240617'
                date_int = int(date_str)

                # 比较日期，根据需要加载不同的配置文件
                if date_int < 20240513:
                    align_config_list = align_config_list_old
                else:
                    align_config_list = align_config_list_new
            # 波段对齐
            aligned_data = bands_align(synthesis_image, align_config_list)
            
            
            




            #保存多通道图像为tif格式
            tif_save_path = os.path.join(save_dir, os.path.basename(bgr_path).replace('.png', '.tif'))
            cv2.imencode('.tif', aligned_data)[1].tofile(tif_save_path)

        else:
            print(f"无法处理文件：{hdr_path}")


