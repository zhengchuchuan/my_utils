import os
import random
import shutil
from my_utils.file_operations.file_check import *


def copy_files_from_folder(src_folder_path, dest_folder_path, file_list):
    """
    将文件夹下的文件,根据一个文件名列表复制到指定目录下
    :param src_folder_path: 待复制的文件夹路径
    :param dest_folder_path: 目标文件夹路径
    :param file_list: 移动的文件名列表
    :return: None
    """
    for file_name in file_list:
        source_file_path = os.path.join(src_folder_path, file_name)

        try:
            # 检查文件路径是否存在,不存在则创建
            if check_file_exists(source_file_path) and check_folder_exists(dest_folder_path):
                # 复制文件袋到指定文件夹
                shutil.copy(source_file_path, dest_folder_path)
        except FileExistsError:
            print(f"File '{file_name}' already exists in the destination folder.")
        except Exception as e:
            print(f"An error occurred while copy '{file_name}': {e}")


def move_files_from_folder(src_folder_path, dest_folder_path, file_list):
    """
    将文件夹下的文件，根据一个文件名列表移动到指定目录下
    :param src_folder_path: 待移动的文件夹路径
    :param dest_folder_path: 目标文件夹路径
    :param file_list: 移动的文件名列表
    :return: None
    """
    for file_name in file_list:
        source_file_path = os.path.join(src_folder_path, file_name)

        try:
            # 检查文件路径是否存在，不存在则创建
            if check_file_exists(source_file_path) and check_file_exists(dest_folder_path):
                # 移动文件到指定文件夹
                shutil.move(source_file_path, dest_folder_path)
        except FileExistsError:
            print(f"File '{file_name}' already exists in the destination folder.")
        except Exception as e:
            print(f"An error occurred while moving '{file_name}': {e}")


def voc_dataset_division(voc_root_folder, xml_file_path, train_proportion=0.7, trainval_proportion=0.8):
    """
    划分voc数据集,并将数据保存在voc数据集格式的对应文件夹下
    :param voc_root_folder: voc格式数据集的根目录,07或者12,用于保存文件
    :param xml_file_path: 待划分的xml文件目录
    :param train_proportion: 训练集比例
    :param trainval_proportion: 训练验证集比例
    :return: None
    """
    # 获取xml文件名列表
    total_xml = os.listdir(xml_file_path)
    # 计算划分数据的索引
    file_length = len(total_xml)  # 文件数量
    file_index_list = range(file_length)  # 文件索引列表
    # 计算详细划分的个数
    trainval_index = int(file_length * trainval_proportion)  
    train_index = int(trainval_index * train_proportion)  
    # 返回训练验证集的划分索引
    trainval_index = random.sample(file_index_list, trainval_index)
    # 在训练验证集上继续划分
    train_index = random.sample(trainval_index, train_index)
    # 打开txt文件,没有则创建
    trainval_file = open(voc_root_folder + 'ImageSets\\Main\\trainval.txt', 'w')
    test_file = open(voc_root_folder + 'ImageSets\\Main\\test.txt', 'w')
    train_file = open(voc_root_folder + 'ImageSets\\Main\\train.txt', 'w')
    val_file = open(voc_root_folder + 'ImageSets\\Main\\val.txt', 'w')
    # 划分数据并写入文件
    for i in file_index_list:
        # voc格式保存的标签不带后缀,一行一个内容
        name = total_xml[i][:-4] + '\n'
        # 属于训练验证集
        if i in trainval_index:
            trainval_file.write(name)
            # 属于训练集
            if i in train_index:
                train_file.write(name)
            # 属于验证集
            else:
                val_file.write(name)
        # 测试集
        else:
            test_file.write(name)
    # 关闭文件
    trainval_file.close()
    train_file.close()
    val_file.close()
    test_file.close()


# 将文件夹下的文件名称合并到一个txt文件中
def get_file_names_from_folder(folder_path, txt_save_path):
    """
    将文件夹下的所有文件的名称合并到一个txt文件中,一个文件名占一行
    未处理文件夹嵌套
    :param folder_path:文件夹的路径
    :param txt_save_path:文本文件保存路径
    :return:None
    """
    try:
        # 获取文件夹下的所有文件
        files = os.listdir(folder_path)
    except FileNotFoundError:
        print("文件路径:{}不存在".format(folder_path))
    # 提取文件名（不包括后缀名）
    file_names = [os.path.splitext(file)[0] for file in files]

    # 将文件名保存到txt文件中
    with open(txt_save_path, 'w') as f:
        f.write('\n'.join(file_names))
