import os


def get_filenames_from_txt(file_path):
    """
    读取txt文件中的路径并提取文件名。

    参数:
    file_path (str): txt文件的路径

    返回:
    set: 包含文件名的集合
    """
    filenames = set()
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            # 去掉行尾的换行符和多余的空格
            line = line.strip()
            # 提取文件名
            filename = os.path.basename(line)
            filenames.add(filename)
    return filenames


def find_common_filenames(file1, file2, output_file):
    """
    找到两个txt文件中均存在的文件名，并将其写入输出文件。

    参数:
    file1 (str): 第一个txt文件的路径
    file2 (str): 第二个txt文件的路径
    output_file (str): 输出文件的路径
    """
    # 获取每个txt文件中的文件名集合
    filenames1 = get_filenames_from_txt(file1)
    filenames2 = get_filenames_from_txt(file2)

    # 找到公共文件名
    common_filenames = filenames1.intersection(filenames2)
    common_filenames = list(common_filenames)
    common_filenames.sort()

    # 将公共文件名写入输出文件
    with open(output_file, 'w', encoding='utf-8') as output:
        for filename in common_filenames:
            output.write(filename + '\n')

    print(f"已将{len(common_filenames)}个公共文件名写入到{output_file}中。")


# 示例用法
file1 = r'C:\Users\zcc\project\python_project\my_utils\data_list\temp1.txt'  # 第一个包含路径的txt文件
file2 = r'C:\Users\zcc\project\python_project\my_utils\data_list\temp2.txt'  # 第二个包含路径的txt文件
output_file = r'C:\Users\zcc\project\python_project\my_utils\data_list\common_filenames.txt'  # 输出文件，存放共有的文件名

find_common_filenames(file1, file2, output_file)
