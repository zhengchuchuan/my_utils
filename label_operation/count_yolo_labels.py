import os
from collections import defaultdict
from tqdm import tqdm


def parse_yolo_label_file(file_path):
    """解析YOLO格式标签文件"""
    with open(file_path, 'r') as file:
        lines = file.readlines()
    labels = [line.strip().split()[0] for line in lines]
    return labels


def count_yolo_labels(directory):
    """统计目录及子目录下所有YOLO标签文件中每个类别的数量"""
    label_counts = defaultdict(int)
    file_list = []

    # 遍历目录获取所有txt文件路径（排除classes.txt）
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.txt') and file != 'classes.txt':
                file_list.append(os.path.join(root, file))

    # 使用tqdm显示进度条
    for file_path in tqdm(file_list, desc="Processing files"):
        labels = parse_yolo_label_file(file_path)
        for label in labels:
            label_counts[label] += 1

    return label_counts


# 示例用法
directory = r'\\192.168.3.155\高光谱测试样本库\原油检测\00大庆现场测试\03标注数据以及模型文件\00数据和标签\dataset_20240806_one_label'  # 替换为你的目录路径
label_counts = count_yolo_labels(directory)

# 打印每个类别的数量
for label, count in label_counts.items():
    print(f"类别索引 {label}: {count} 个")
