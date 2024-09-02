import os
import glob

from tqdm import tqdm


def delete_files_by_extension(root_dir, file_extension):
    # 使用 glob 模块查找指定目录及其子目录下的所有符合扩展名的文件
    search_pattern = os.path.join(root_dir, '**', f'*{file_extension}')
    files_to_delete = glob.glob(search_pattern, recursive=True)

    # 删除找到的文件
    for file_path in tqdm(files_to_delete):
        try:
            os.remove(file_path)
            # print(f'Deleted: {file_path}')
        except OSError as e:
            print(f'Error deleting {file_path}: {e}')


# 示例用法
root_directory = r'\\192.168.3.155\高光谱测试样本库\原油检测\00大庆现场测试\03标注数据以及模型文件\00数据和标签\dataset_20240806_one_label\all_images_except_missed_detections\01_source\202403'  # 指定根目录
extension = '.jpg'  # 要删除的文件扩展名，不需要加点
delete_files_by_extension(root_directory, extension)
