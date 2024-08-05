import os
import shutil
from my_utils.file_operations.file_batch_processing import copy_files_from_folder


if __name__ == '__main__':
    source_folder = r'D:\Documents\DataSet\ZDRH\poppy_top5_more\XmlDrawRect_all'
    destination_folder = r'D:\Documents\DataSet\ZDRH\poppy_top5_more\XmlDrawRect_split'
    # 方式一:移动文本文件中的文件名
    # txt_path = r''
    # with open(txt_path, 'r') as file:
    #     file_names = file.read().splitlines()
    # 方式二:获取列表的形式
    folder_path = r'D:\Documents\DataSet\ZDRH\poppy_top5_more\img'
    file_name_list = [f for f in os.listdir(folder_path)]

    # 移动文件夹中的指定文件
    copy_files_from_folder(source_folder, destination_folder, file_name_list)
    print("All files moved.")
