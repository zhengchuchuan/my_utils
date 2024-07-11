import os
import shutil
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# 定义文件路径
input_txt_path = r'C:\Users\zcc\project\wayho\oil_detection\oil_identification\data\data_list\miss.txt'  # 包含文件路径的txt文档
search_directory = r'Z:\01数据'  # 要搜索文件的目录
target_directory = r'C:\Users\zcc\project\wayho\oil_detection\oil_identification\data\oil'  # 复制文件的目标目录

# 读取txt文档中的文件路径
with open(input_txt_path, 'r') as file:
    file_paths = file.read().splitlines()

# 去除路径和后缀后的文件名
base_names = [os.path.splitext(os.path.basename(file_path))[0] for file_path in file_paths]

# 定义扩展名列表
extensions = ['jpg', 'hdr', 'img']


def copy_file_if_exists(source_file, target_directory):
    if os.path.isfile(source_file):
        shutil.copy(source_file, target_directory)
        print(f'Copied: {source_file} to {target_directory}')


def process_directory(root, base_names, target_directory):
    for base_name in base_names:
        for extension in extensions:
            source_file = os.path.join(root, f'{base_name}.{extension}')
            copy_file_if_exists(source_file, target_directory)


# 使用线程池来并发处理
with ThreadPoolExecutor(max_workers=8) as executor:
    futures = []
    for root, dirs, files in os.walk(search_directory):
        futures.append(executor.submit(process_directory, root, base_names, target_directory))

    # 等待所有任务完成
    for future in futures:
        future.result()

print('File copying process completed.')
