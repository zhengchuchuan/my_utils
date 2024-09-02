import os
import shutil
from tqdm import tqdm

from file_operation.delete_files_by_extension import extension
from file_operation.gather_file_paths import gather_file_paths


def transfer_files(file_paths, find_dir, dest_dir, target_folder_name=None, transfer_type='copy', extensions=None, direct_transfer=False):
    """
    根据标志位决定是查找文件还是直接根据路径复制或移动文件。

    :param file_paths: 文件路径或文件名的列表
    :param find_dir: 查找文件的目录
    :param dest_dir: 目标目录
    :param target_folder_name: 只处理指定名称的文件夹
    :param transfer_type: 'copy' 或 'move'，选择复制或移动文件
    :param extensions: 只处理指定后缀的文件
    :param direct_transfer: 是否直接根据路径进行复制或移动
    """
    # 创建保存未找到文件名的列表
    not_found_files = []

    # 创建目标目录（如果不存在）
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    # 根据标志位决定是查找文件还是直接复制/移动
    if direct_transfer:
        for file_path in tqdm(file_paths, desc="Directly transferring files", unit="file"):
            if os.path.exists(file_path):
                dest_file = os.path.join(dest_dir, os.path.basename(file_path))
                if transfer_type == 'copy':
                    shutil.copy2(file_path, dest_file)
                elif transfer_type == 'move':
                    shutil.move(file_path, dest_file)
            else:
                not_found_files.append(file_path)
    else:
        for file_path in tqdm(file_paths, desc="Processing files", unit="file"):
            found = False
            base_name = os.path.basename(file_path)  # 从路径中提取文件名

            # 如果指定了后缀列表，则只处理同名文件+指定后缀的文件
            if extensions:
                base_name_without_ext, _ = os.path.splitext(base_name)
                potential_names = [f"{base_name_without_ext}{ext}" for ext in extensions]
            else:
                potential_names = [base_name]

            # 遍历所有目录，查找匹配的文件
            for root, dirs, files in os.walk(find_dir):
                # 检查当前目录名是否为目标文件夹名
                if os.path.basename(root) == target_folder_name or target_folder_name is None:
                    for potential_name in potential_names:
                        if potential_name in files:
                            source_file = os.path.join(root, potential_name)
                            dest_file = os.path.join(dest_dir, potential_name)
                            # 如果目标文件已存在，则跳过
                            if os.path.exists(dest_file):
                                continue

                            # 根据 transfer_type 执行复制或移动操作
                            if transfer_type == 'copy':
                                shutil.copy2(source_file, dest_file)
                            elif transfer_type == 'move':
                                shutil.move(source_file, dest_file)

                            found = True
                    # 只找到一个文件就跳出循环
                    if found:
                        break

            if not found:
                not_found_files.append(file_path)

    # 输出未找到的文件名或路径
    if not_found_files:
        print(f"未找到的文件: {', '.join(not_found_files)}")
    else:
        print("所有文件都已找到并处理。")


if __name__ == "__main__":
    transfer_type = 'copy'  # 选择 'copy' 或 'move'
    # 需要移动的文件名或路径列表
    txt_file_paths = None
    # txt_file_paths = [r'C:\Users\zcc\project\python_project\my_utils\data_list\duplicates.txt']
    directories = None
    directories =  [r'\\192.168.3.155\高光谱测试样本库\原油检测\00大庆现场测试\03标注数据以及模型文件\00数据和标签\dataset_20240806_one_label\all_images_except_missed_detections\03_根据推理图像的分类结果\误检背景\植被']

    # 目标目录
    dest_dir = r'\\192.168.3.155\高光谱测试样本库\原油检测\00大庆现场测试\03标注数据以及模型文件\00数据和标签\dataset_20240806_one_label\all_images_except_missed_detections\04_汇总无框有标签文件的图像\背景\植被\images'


    direct_transfer = False  # 设置为 True 时，直接根据路径复制或移动文件；为 False 时，查找文件

    # 查找的文件夹
    find_dir = r'\\192.168.3.155\高光谱测试样本库\原油检测\00大庆现场测试\03标注数据以及模型文件\00数据和标签\dataset_20240806_one_label\all_images_except_missed_detections\01_source'
    target_folder_name = None  # 只查找此名字的文件夹
    # 查找所有指定后缀的文件
    extensions = ['.png']
    # extensions = None

    # 获取文件路径列表
    file_paths = gather_file_paths(txt_paths=txt_file_paths,directories=directories, extensions=extensions)

    transfer_files(file_paths=file_paths, find_dir=find_dir, dest_dir=dest_dir, target_folder_name=target_folder_name,
                   transfer_type=transfer_type, extensions=extensions, direct_transfer=direct_transfer)
