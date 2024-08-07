import shutil
import os


def copy_files(file_list_path, target_directory):
    # 确保目标目录存在，不存在则创建
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    # 读取文件列表
    with open(file_list_path, 'r') as file:
        file_paths = file.readlines()

    # 去除每行的换行符
    file_paths = [file_path.strip() for file_path in file_paths]

    # 复制文件到目标目录
    for file_path in file_paths:
        if os.path.exists(file_path):
            shutil.copy(file_path, target_directory)
        else:
            print(f"文件 {file_path} 不存在，无法复制。")


# 示例用法
file_list_path = '/home/cia005/ZCC/oil/yolov5-7.0/dataset/data_list/20240806_test_list.txt'  # 存储文件路径的文件列表
target_directory = '/home/cia005/ZCC/oil/yolov5-7.0/dataset/test'  # 目标目录
copy_files(file_list_path, target_directory)
