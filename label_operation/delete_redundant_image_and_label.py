import os
import shutil

from tqdm import tqdm


def get_file_stems(directory, file_extensions):
    """
    获取目录下指定扩展名文件的文件名（不包括扩展名）

    Parameters:
    - directory: 文件目录路径
    - file_extensions: 要匹配的文件扩展名的元组 (e.g., ('.jpg', '.png'))

    Returns:
    - 包含文件名（不包括扩展名）的集合
    """
    return {os.path.splitext(f)[0] for f in os.listdir(directory) if f.endswith(file_extensions)}


def process_files(file_dir_1, file_dir_2, output_dir, file_extensions_1, file_extensions_2,
                  operation_mode='intersection'):
    """
    根据指定的操作模式处理文件：
    - 如果是交集模式: 将没有相同文件名的文件移动到指定的输出目录。
    - 如果是差集模式: 仅输出多余文件的列表。

    Parameters:
    - file_dir_1: 第一个文件目录（通常是图像目录）
    - file_dir_2: 第二个文件目录（通常是标签目录）
    - output_dir: 交集模式下，多余文件的目标目录
    - file_extensions_1: 第一个文件目录中需要匹配的文件扩展名 (e.g., ('.jpg', '.png'))
    - file_extensions_2: 第二个文件目录中需要匹配的文件扩展名 (e.g., ('.txt',))
    - operation_mode: 'intersection' 或 'difference'
    """
    # 获取两个目录下的文件名（不包含扩展名）的集合
    stems_1 = get_file_stems(file_dir_1, file_extensions_1)
    stems_2 = get_file_stems(file_dir_2, file_extensions_2)

    if operation_mode == 'intersection':
        # 找出没有对应文件的文件名
        extra_files_1 = stems_1 - stems_2
        extra_files_2 = stems_2 - stems_1

        # 移动没有对应的文件到 output_dir
        for stem in tqdm(extra_files_1):
            for ext in file_extensions_1:
                file_path = os.path.join(file_dir_1, stem + ext)
                if os.path.exists(file_path):
                    dest_path = os.path.join(output_dir, os.path.basename(file_path))
                    shutil.move(file_path, dest_path)
                    # print(f"Moved file: {file_path} to {dest_path}")

        for stem in tqdm(extra_files_2):
            for ext in file_extensions_2:
                file_path = os.path.join(file_dir_2, stem + ext)
                if os.path.exists(file_path):
                    dest_path = os.path.join(output_dir, os.path.basename(file_path))
                    shutil.move(file_path, dest_path)
                    # print(f"Moved file: {file_path} to {dest_path}")



if __name__ == "__main__":
    file_dir_1 = r'\\192.168.3.155\高光谱测试样本库\原油检测\00大庆现场测试\03标注数据以及模型文件\00数据和标签\dataset_20240806_one_label\all_images_except_missed_detections\04_汇总无框有标签文件的图像\疑似油\images'
    file_dir_2 = r'\\192.168.3.155\高光谱测试样本库\原油检测\00大庆现场测试\03标注数据以及模型文件\00数据和标签\dataset_20240806_one_label\all_images_except_missed_detections\04_汇总无框有标签文件的图像\疑似油\labels'
    output_dir = r'\\192.168.3.155\高光谱测试样本库\原油检测\00大庆现场测试\03标注数据以及模型文件\00数据和标签\dataset_20240806_one_label\all_images_except_missed_detections\04_汇总无框有标签文件的图像\疑似油\temp'

    # 指定文件扩展名
    file_extensions_1 = ('.jpg', '.png')
    file_extensions_2 = ('.txt',)

    # 设置操作模式为 'intersection' 或 'difference'
    operation_mode = 'intersection'


    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    process_files(file_dir_1, file_dir_2, output_dir, file_extensions_1, file_extensions_2, operation_mode)
