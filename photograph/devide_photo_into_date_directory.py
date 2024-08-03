import glob
import os
import re
import shutil
from datetime import datetime

import exifread


def get_exif_data(file_path):
    with open(file_path, 'rb') as f:
        tags = exifread.process_file(f)
        return tags

def get_files_list(file_paths, suffixes=None):
    file_list = []
    for file_path in file_paths:
        for root, dirs, files in os.walk(file_path):
                if suffixes is None:
                    file_list.extend(glob.glob(fr"{root}/*"))
                else:
                    for suffix in suffixes:
                        file_list.extend(glob.glob(fr"{root}/*{suffix}"))
    return file_list

def classify_files_by_date(file_paths):
    # 创建一个空字典来存储文件按日期分类的结果
    classified_files = {}

    for file_path in file_paths:

        exif_data = get_exif_data(file_path)

        image_data_time = exif_data.get('Image DateTime')

        if image_data_time is not None:
            # 访问字段值
            image_data_time_value = image_data_time.values
        else:
            continue

        date_parts = image_data_time_value.split(' ')
        # 提取日期部分
        date = date_parts[0]
        date_str = date.replace(':', '-')
        # 如果日期不在字典中，则创建一个新列表来存储该日期对应的文件
        if date_str not in classified_files:
            classified_files[date_str] = []

        # 将文件路径添加到相应日期的文件列表中
        classified_files[date_str].append(file_path)

    return classified_files

def move_files_to_date_folders(classified_files):
    # 遍历分类好的文件字典
    for date, files in classified_files.items():
        # 创建以日期命名的目标文件夹路径
        date_folder = os.path.dirname(files[0])
        date_folder = os.path.join(date_folder, date)
        # 如果目标文件夹不存在，则创建它
        if not os.path.exists(date_folder):
            os.makedirs(date_folder)
        # 移动每个文件到相应的日期文件夹中
        for file_path in files:
            file_name = os.path.basename(file_path)
            destination_path = os.path.join(date_folder, file_name)
            shutil.move(file_path, destination_path)
        print(f'已将{len(files)}个文件移动到{date_folder}文件夹')


if __name__ == '__main__':
    # 指定要分类的文件路径
    root_paths = r'C:\Users\Administrator\Pictures\Photos\摄影原片\中国\重庆市'

    for root, dirs, file_name_list in os.walk(root_paths):

        # 使用正则表达式检查根目录是否匹配日期格式
        if re.match(r'\d{4}-\d{2}-\d{2}', os.path.basename(root)):
            print('已经是日期文件夹,跳过')
            continue
        # 获取文件列表
        image_extensions = ['.arw','.jpg', '.jpeg', '.png', '.gif', '.bmp']

        photo_path_list = [os.path.join(root, file_name) for file_name in file_name_list if
                          os.path.splitext(file_name)[1].lower() in image_extensions]

        if photo_path_list != []:
            # 按日期分类文件
            classified_files = classify_files_by_date(photo_path_list)

            move_files_to_date_folders(classified_files)



