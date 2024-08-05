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


def create_folder_if_not_exists(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"文件夹 '{folder_path}' 不存在，已创建。")
    else:
        print(f"文件夹 '{folder_path}' 已经存在。")


def split_dataset(file_path_list, train_ratio=0.8, val_ratio=0.15):
    """
    划分数据集为训练集、验证集和测试集
    :param file_path_list: 包含所有数据文件的列表
    :param train_ratio: 训练集的比例
    :param val_ratio: 验证集的比例
    :return: 训练集、验证集和测试集（如果测试集比例为0，则返回训练集和验证集）
    """
    # 检查比例之和是否小于等于1
    if train_ratio + val_ratio > 1.0:
        raise ValueError("训练集和验证集的比例之和不能大于1")

    # 打乱文件列表
    random.shuffle(file_path_list)

    # 计算划分的索引
    num_samples = len(file_path_list)
    num_train = int(train_ratio * num_samples)
    num_val = int(val_ratio * num_samples)
    num_test = num_samples - num_train - num_val  # 剩余的部分作为测试集

    # 划分数据集
    train_data = file_path_list[:num_train]
    val_data = file_path_list[num_train:num_train + num_val]

    # 处理测试集为0的情况
    if num_test == 0:
        test_data = []
    else:
        test_data = file_path_list[num_train + num_val:]

    # 打印划分结果
    print("Training data:", len(train_data))
    print("Validation data:", len(val_data))
    print("Testing data:", len(test_data))

    return train_data, val_data, test_data






file_path_lists = [r'D:\Project\python_project\my_utils\exp\labeled_image_path_list.txt']

save_dir = "exp"

current_time = datetime.now()
formatted_time = current_time.strftime('%Y-%m-%d-%H-%M')

create_folder_if_not_exists(save_dir)
file_paths_lists = []
for file_path_list in file_path_lists:
    with open(file_path_list, 'r') as fin:
        file_paths = [line.replace('\n', '') for line in fin]
        file_paths_lists.extend(file_paths)

train_list = []
val_list = []
test_list = []

train_list, val_list, test_list = split_dataset(file_path_list=file_paths_lists, train_ratio=0.8, val_ratio=0.1)

description = None
save_train_path = os.path.join(save_dir, f"train_list_{formatted_time}.txt")
save_val_path = os.path.join(save_dir, f"val_list_{formatted_time}.txt")
save_test_path = os.path.join(save_dir, f"test_list_{formatted_time}.txt")

with open(save_train_path, "w") as file:
    for string in train_list:
        file.write(string + "\n")

with open(save_val_path, "w") as file:
    for string in val_list:
        file.write(string + "\n")

with open(save_test_path, "w") as file:
    for string in test_list:
        file.write(string + "\n")
