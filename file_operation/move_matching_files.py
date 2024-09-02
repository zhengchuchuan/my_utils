import os
import shutil
from tqdm import tqdm


def load_file_names(file_name_txt):
    """
    从txt文件中读取文件名列表。

    :param file_name_txt: 存放文件名的txt文件路径
    :return: 文件名列表
    """
    with open(file_name_txt, 'r') as f:
        file_names = f.read().splitlines()
    return file_names


def load_paths(path_txt):
    """
    从txt文件中读取路径列表。

    :param path_txt: 存放路径的txt文件路径
    :return: 路径列表
    """
    with open(path_txt, 'r') as f:
        paths = f.read().splitlines()
    return paths


def move_matching_files(file_name_txt, path_txt, dest_dir):
    """
    移动路径中和文件名匹配的文件到指定目录下。

    :param file_name_txt: 存放文件名的txt文件路径
    :param path_txt: 存放路径的txt文件路径
    :param dest_dir: 目标目录
    """
    # 读取文件名和路径列表
    file_names = load_file_names(file_name_txt)
    paths = load_paths(path_txt)

    # 创建目标目录（如果不存在）
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # 遍历每个路径，查找匹配的文件并移动
    for path in paths:
        if not os.path.exists(path):
            print(f"路径不存在: {path}")
            continue

        for root, dirs, files in os.walk(path):
            for file in files:
                if file in file_names:
                    source_file = os.path.join(root, file)
                    dest_file = os.path.join(dest_dir, file)

                    # 检查目标文件是否已存在，处理重名文件
                    if os.path.exists(dest_file):
                        base_name, ext = os.path.splitext(file)
                        counter = 1
                        new_dest_file = os.path.join(dest_dir, f"{base_name}_{counter}{ext}")
                        while os.path.exists(new_dest_file):
                            counter += 1
                            new_dest_file = os.path.join(dest_dir, f"{base_name}_{counter}{ext}")
                        dest_file = new_dest_file

                    # 移动文件
                    shutil.move(source_file, dest_file)
                    print(f"移动文件: {source_file} 到 {dest_file}")


if __name__ == "__main__":
    file_name_txt = r'C:\Users\zcc\project\python_project\my_utils\data_list\duplicates.txt'  # 存放文件名的txt文件
    path_txt = r'C:\Users\zcc\project\python_project\my_utils\data_list\20240830_temp.txt'  # 存放路径的txt文件
    dest_dir = r'\\192.168.3.155\高光谱测试样本库\原油检测\00大庆现场测试\03标注数据以及模型文件\00数据和标签\dataset_20240806_one_label\all_images_except_missed_detections\03_根据推理图像的分类结果\temp'  # 目标目录

    move_matching_files(file_name_txt, path_txt, dest_dir)
