import glob
import os
import sys


def get_file_path_list(file_paths, suffixes=None, prefix=None, file_name_pattern=None, process_folders=None,
                  ignore_files=None):
    filename_list = []

    # 每个文件夹路径
    for file_path in file_paths:
        # 处理文件夹的子目录
        for root, dirs, files in os.walk(file_path):
            dir_paths = []
            root_dir = os.path.basename(root)

            # 处理指定的子文件夹
            if process_folders and root_dir in process_folders or not process_folders:
                # 获取文件路径列表
                for suffix in suffixes:
                    dir_paths.extend(glob.glob(fr"{root}/{file_name_pattern}{suffix}"))

                # 仅获取带后缀的文件名,并排除指定的文件
                if ignore_files:
                    dir_paths = [path for path in dir_paths if
                                 not any(path.endswith(ignore_file) for ignore_file in ignore_files)]

                # 将路径前加上前缀
                if prefix is not None:
                    dir_paths = [os.path.join(prefix, path) for path in dir_paths]

                filename_list.extend(dir_paths)

    return filename_list

if __name__ == '__main__':
    data_dirs = [r'\\192.168.3.155\高光谱测试样本库\原油检测\00大庆现场测试\03标注数据以及模型文件\00数据和标签\dataset_20240806_one_label\source\202404',
                 r'\\192.168.3.155\高光谱测试样本库\原油检测\00大庆现场测试\03标注数据以及模型文件\00数据和标签\dataset_20240806_one_label\source\202405',
                 r'\\192.168.3.155\高光谱测试样本库\原油检测\00大庆现场测试\03标注数据以及模型文件\00数据和标签\dataset_20240806_one_label\source\202406',
                 r'\\192.168.3.155\高光谱测试样本库\原油检测\00大庆现场测试\03标注数据以及模型文件\00数据和标签\dataset_20240806_one_label\source\202407']
    save_dir = "exp"
    # list_name = '20240729_foreground_list.txt'
    # list_name = '20240729_background_list.txt'
    list_name = 'data_list_04-07_20240807.txt'
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    prefix = None
    suffixes = ['.png', '.jpg', '.jpeg']
    file_name_pattern = '*'
    process_folders = ['images']  # 指定要处理的子文件夹名
    ignore_files = ['classes.txt']  # 指定要忽略的文件名

    label_list = (get_file_path_list
                  (file_paths=data_dirs, suffixes=suffixes, prefix=prefix, file_name_pattern=file_name_pattern,
                               process_folders=process_folders, ignore_files=ignore_files))

    print(len(label_list))
    label_list.sort()

    list_save_path = os.path.join(save_dir, list_name)

    with open(list_save_path, "w", encoding='utf-8') as file:
        for string in label_list:
            file.write(string + "\n")
