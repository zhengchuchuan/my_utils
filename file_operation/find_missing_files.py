import os

from tqdm import tqdm


def find_files_with_extensions(directory, ext_list):
    """获取目录下指定后缀的所有文件"""
    files = []
    for root, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(tuple(ext_list)):
                files.append(os.path.join(root, filename))
    return files


def find_missing_extensions(directory, ext_list, target_ext):
    """查找某文件的其他后缀，如果某后缀找不到，记录下来"""
    missing_files = []

    # 获取目录下所有指定后缀的文件
    files_with_ext = find_files_with_extensions(directory, ext_list)

    for file_path in tqdm(files_with_ext):
        base_name = os.path.splitext(file_path)[0]
        found = False

        # 查找是否存在相同文件名但不同后缀的文件
        for ext in target_ext:
            target_file = base_name + ext
            if os.path.exists(target_file):
                found = True
                break

        # 如果没有找到目标后缀文件，将其加入 missing_files 列表
        if not found:
            missing_files.append(file_path)

    return missing_files


def save_list_to_file(file_list, output_file):
    """将列表内容保存到指定文件中"""
    with open(output_file, 'w') as f:
        for item in file_list:
            f.write(f"{item}\n")


# 使用示例
if __name__ == "__main__":
    directory = r"\\192.168.3.155\高光谱测试样本库\原油检测\00大庆现场测试\03标注数据以及模型文件\00数据和标签\dataset_one_label\train\suspect\images"  # 指定要查找的目录
    ext_list = [".png"]  # 原始文件的后缀
    target_ext = [".img", ".hdr"]  # 要查找的目标后缀
    output_file = "../exp/missing_files.txt"  # 结果保存的文件

    # 查找缺失的文件
    missing_files = find_missing_extensions(directory, ext_list, target_ext)

    # 保存缺失文件列表到文件
    save_list_to_file(missing_files, output_file)

    print(f"Missing files saved to {output_file}")
