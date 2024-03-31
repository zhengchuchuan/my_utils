import os
import random


def split_dataset(input_folder, train_ratio=0.8):
    # 获取文件夹中所有.hdr后缀的文件名
    hdr_files = [file for file in os.listdir(input_folder) if file.endswith('.hdr')]

    # 打乱文件名列表
    random.shuffle(hdr_files)

    # 计算训练集和验证集的切分点
    split_point = int(len(hdr_files) * train_ratio)

    # 分割文件名列表
    train_files = hdr_files[:split_point]
    val_files = hdr_files[split_point:]

    # 将文件名写入train_list.txt
    with open('train_list.txt', 'w') as train_file:
        for file in train_files:
            train_file.write(f"{file}\n")

    # 将文件名写入val_list.txt
    with open('val_list.txt', 'w') as val_file:
        for file in val_files:
            val_file.write(f"{file}\n")


# 指定文件夹路径
folder_path = r'C:\Documents\SyncFolder\Work\Wayho\dataset\rgb_restruction\rgb_restruction'

# 调用函数进行文件名切分
split_dataset(folder_path)
