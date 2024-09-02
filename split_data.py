import sys

# sys.path.append("..")
import random
import glob
import os
from datetime import datetime

# 获取当前脚本文件所在目录的上级目录路径
current_dir = os.path.dirname(os.path.realpath(__file__))
parent_dir = os.path.dirname(current_dir)
# 将上级目录路径添加到 sys.path 中
sys.path.append(parent_dir)




def split_dataset(hdr_files, train_ratio=0.8, val_ratio=0.2):
    """
    划分数据集为训练集、验证集和测试集
    :param hdr_files: 包含所有数据文件的列表
    :param train_ratio: 训练集的比例
    :param val_ratio: 验证集的比例
    :return: 训练集、验证集和测试集（如果测试集比例为0，则返回训练集和验证集）
    """
    # 检查比例之和是否小于等于1
    if train_ratio + val_ratio > 1.0:
        raise ValueError("训练集和验证集的比例之和不能大于1")


    # 打乱文件列表
    random.shuffle(hdr_files)

    # 计算划分的索引
    num_samples = len(hdr_files)


    if train_ratio + val_ratio < 1.0:
        num_train = int(train_ratio * num_samples)
        num_val = int(val_ratio * num_samples)

        # 划分数据集
        train_data = hdr_files[:num_train]
        val_data = hdr_files[num_train:num_train + num_val]
        test_data = hdr_files[num_train + num_val:]
    elif train_ratio + val_ratio == 1.0:
        num_train = int(train_ratio * num_samples)

        # 划分数据集
        train_data = hdr_files[:num_train]
        val_data = hdr_files[num_train:]
        test_data = []


    # 打印划分结果
    print("Training data:", len(train_data))
    print("Validation data:", len(val_data))
    print("Testing data:", len(test_data))

    return train_data, val_data, test_data



def get_data_path(file_paths, suffixes=['.hdr'], prefix=None, train_ratio=0.8, val_ratio=0.1):
    train_list = []
    val_list = []
    test_list = []
    # 每个文件夹路径
    for file_path in file_paths:
        # 处理文件夹的子目录
        for root, dirs, files in os.walk(file_path):
            dir_paths = []
            root_dir = os.path.basename(root)
            # 处理指定的子文件夹
            if root_dir == 'images':
                # 获取文件路径列表
                for suffix in suffixes:
                    dir_paths.extend(glob.glob(fr"{root}/*{suffix}"))
                # 将路径前加上前缀
                if prefix is not None:
                    dir_paths = [os.path.join(prefix, path) for path in dir_paths]  #######
                # 确保每个文件夹下都有训练集、验证集和测试集
                train_part, val_part, test_part = split_dataset(hdr_files=dir_paths, train_ratio=train_ratio, val_ratio=val_ratio)

                train_list.extend(train_part)
                val_list.extend(val_part)
                test_list.extend(test_part)

    return train_list, val_list, test_list



if __name__ == '__main__':
    data_dirs = [r'\\192.168.3.155\高光谱测试样本库\原油检测\00大庆现场测试\03标注数据以及模型文件\00数据和标签\dataset_20240806_one_label\source\202404',
                 r'\\192.168.3.155\高光谱测试样本库\原油检测\00大庆现场测试\03标注数据以及模型文件\00数据和标签\dataset_20240806_one_label\source\202405',
                 r'\\192.168.3.155\高光谱测试样本库\原油检测\00大庆现场测试\03标注数据以及模型文件\00数据和标签\dataset_20240806_one_label\source\202406',
                 r'\\192.168.3.155\高光谱测试样本库\原油检测\00大庆现场测试\03标注数据以及模型文件\00数据和标签\dataset_20240806_one_label\source\202407',
                 ]
    save_dir = "exp"
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    prefix = None
    suffixes = ['.png', '.jpg', '.jpeg']

    train_list = []
    val_list = []
    test_list = []

    train_list, val_list, test_list = get_data_path(file_paths=data_dirs, suffixes=suffixes, prefix=prefix, train_ratio=0.8, val_ratio=0.2)

    train_list.sort()
    val_list.sort()
    test_list.sort()

    now = datetime.now()
    current_date = now.strftime("%Y%m%d")
    save_train_path = os.path.join(save_dir, f"{current_date}_train_list.txt")
    save_val_path = os.path.join(save_dir, f"{current_date}_val_list.txt")
    save_test_path = os.path.join(save_dir, f"{current_date}_test_list.txt")

    with open(save_train_path, "w") as file:
        for string in train_list:
            file.write(string + "\n")

    with open(save_val_path, "w") as file:
        for string in val_list:
            file.write(string + "\n")

    with open(save_test_path, "w") as file:
        for string in test_list:
            file.write(string + "\n")
