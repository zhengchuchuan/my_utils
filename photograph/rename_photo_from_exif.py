import re

import exifread
import glob
import os

from tqdm import tqdm


def get_exif_data(file_path):
    with open(file_path, 'rb') as f:
        tags = exifread.process_file(f)
        return tags

def get_files_list(file_paths, suffixes=['.ARW', '.jpeg', '.jpg', '.png', '.bmp','dng']):
    file_list = []
    for file_path in file_paths:
        for root, dirs, files in os.walk(file_path):

                for suffix in suffixes:
                    file_list.extend(glob.glob(fr"{root}/*{suffix}"))
    return file_list

def replace_invalid_chars(filename):
    # 定义 Windows 文件名中不允许的字符的正则表达式模式
    invalid_chars_pattern = r'[\\/:*?"<>|]'
    # 使用正则表达式将不允许的字符替换为空字符
    return re.sub(invalid_chars_pattern, '', filename)

def compare_exif(exif_data1, duplicate_name):

    exif_data2 = get_exif_data(duplicate_name)
    # 移除可能不同的标签
    exif_data1.pop('JPEGThumbnail', None)
    exif_data2.pop('JPEGThumbnail', None)

    # 比较字段
    different_fields = []

    # 比较每个字段的值
    for tag in exif_data1:
        if tag in exif_data2:
            if exif_data1[tag].values != exif_data2[tag].values:
                different_fields.append(tag)
        else:
            different_fields.append(tag)

    for tag in exif_data2:
        if tag not in exif_data1:
            different_fields.append(tag)
    if different_fields: # 如果有不同的字段
        return False
    else:
        return True


def get_unique_suffix_file_path(file_path):
    base_name, extension = os.path.splitext(file_path)
    new_file_path = file_path
    suffix = 1

    while os.path.exists(new_file_path):
        new_file_path = f"{base_name}_{suffix:03d}{extension}"
        suffix += 1

    return new_file_path
def rename_photo_from_exif(drive, files_path_list):
    for file_path in tqdm(files_path_list):
        suffix = file_path[-4:]
        exif_data = get_exif_data(file_path)

        camera_factory = exif_data.get('Image Make')
        if camera_factory is not None:
            camera_factory = camera_factory.values
        else:
            camera_factory = None

        camera_model = exif_data.get('Image Model')
        if camera_model is not None:
            camera_model = camera_model.values
        else:
            camera_model = None

        lens_model = exif_data.get('EXIF LensModel')
        if lens_model is not None:
            lens_model = lens_model.values
            lens_model = lens_model.replace(' ', '')
        else:
            lens_model = None

        image_data_time = exif_data.get('Image DateTime')
        if image_data_time is not None:
            image_data_time = image_data_time.values
            image_data_time = image_data_time.replace(' ', '-')
            image_data_time = image_data_time.replace(':', '')
        else:
            image_data_time = None

        color_space = exif_data.get('EXIF ColorSpace')

        focal_length_35mm_film = exif_data.get('EXIF FocalLengthIn35mmFilm')
        focal_length_35mm_film = str(focal_length_35mm_film) + 'mm'

        exposure_time = exif_data.get('EXIF ExposureTime')
        if exposure_time is not None:
            exposure_time = eval(str(exposure_time))
            exposure_time = str(round(exposure_time, 6)) + 's'

        f_number = exif_data.get('EXIF FNumber')
        if f_number is not None:
            f_number = f_number.values
            f_number = 'f' + str(eval("28/5"))
        else:
            f_number = None

        iso = exif_data.get('EXIF ISOSpeedRatings')
        iso = 'ISO' + str(iso)


        new_file_name = '_'.join([
            str(image_data_time),  str(focal_length_35mm_film),
            str(exposure_time), str(f_number), str(iso),
            str(camera_factory), str(camera_model), str(lens_model),
            str(color_space)
        ])
        new_file_name = new_file_name + suffix
        new_file_name = replace_invalid_chars(new_file_name)

        file_path_token = file_path.split('\\')[1:-1]
        file_dir = os.path.join(drive, *file_path_token)
        new_file_path = os.path.join(file_dir, new_file_name)

        if not os.path.exists(new_file_path):
            os.rename(file_path, new_file_path)
        elif not compare_exif(exif_data, new_file_path):
            file_path_with_suffix = get_unique_suffix_file_path(new_file_path)
            os.rename(file_path, file_path_with_suffix)
            print(f"文件 '{new_file_path}' 文件名已存在,但图像不同,已添加后缀")
        else:
            print(f"文件 '{new_file_path}' 已存在，跳过重命名操作。")




if __name__ == '__main__':
    files_dir = [r'D:\Pictures\temp',]
    drive = 'D:\\'
    files_path_list = get_files_list(files_dir)

    rename_photo_from_exif(drive, files_path_list)

    # files_path_list = [r'C:\Users\Administrator\Pictures\Photos\摄影原片\中国\四川省\绵阳市\西科大\毕业照\SWUST_511.ARW',]
    # drive = 'C:\\'
    # rename_photo_from_exif(drive, files_path_list)

'''Image Make SONY
Image Model ILCE-7RM3
Image DateTime 2024:03:19 18:18:07
Image Artist zhengchuchuan
EXIF ExposureTime 1/200
EXIF FNumber 28/5
EXIF ISOSpeedRatings 100
EXIF ColorSpace sRGB
EXIF ExifImageWidth 7952
EXIF ExifImageLength 5304
EXIF FocalLengthIn35mmFilm 200
'''
