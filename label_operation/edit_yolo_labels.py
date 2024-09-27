import os

from tqdm import tqdm


def process_yolo_labels(folder_path):
    # 列出文件夹中的所有文件
    files = os.listdir(folder_path)

    # 过滤掉 classes.txt 文件
    txt_files = [f for f in files if f.endswith('.txt') and f != 'classes.txt']

    # 遍历每个TXT文件
    for txt_file in tqdm(txt_files):
        file_path = os.path.join(folder_path, txt_file)

        # 读取文件内容
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # 处理每一行
        updated_lines = []
        for line in lines:
            parts = line.strip().split()
            if len(parts) >= 1:
                # 获取当前类别索引
                class_index = int(parts[0])

                # 更新类别索引
                if class_index == 0:
                    parts[0] = '1'
                # elif class_index in {1, 2, 3}:
                #     parts[0] = '0'

                # 重建行内容并添加到更新后的行列表中
                updated_lines.append(' '.join(parts))

        # 写回更新后的内容到文件
        with open(file_path, 'w') as file:
            file.write('\n'.join(updated_lines))


# 使用示例
folder_path = r'\\192.168.3.155\高光谱测试样本库\原油检测\00大庆现场测试\03标注数据以及模型文件\00数据和标签\dataset_zcc\generate_images\20240807\labels'  #
process_yolo_labels(folder_path)
