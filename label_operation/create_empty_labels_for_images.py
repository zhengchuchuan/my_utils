import os

from tqdm import tqdm


def create_empty_labels_for_images(directory):
    # 创建labels文件夹，如果不存在
    labels_folder = os.path.join(os.path.dirname(directory), 'labels')
    os.makedirs(labels_folder, exist_ok=True)

    # 遍历文件夹中的所有文件
    for filename in tqdm(os.listdir(directory)):
        # 检查文件是否为图像文件（JPG或PNG）
        if filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            # 构造对应的TXT文件路径
            label_filename = os.path.splitext(filename)[0] + '.txt'
            label_file_path = os.path.join(labels_folder, label_filename)

            # 创建空的TXT文件
            with open(label_file_path, 'w') as file:
                pass  # 只创建空文件，不写入内容

            # print(f"Created empty label for {filename}")


# 指定图像文件夹路径
images_folder_path = r'\\192.168.3.155\高光谱测试样本库\原油检测\00大庆现场测试\03标注数据以及模型文件\00数据和标签\dataset_20240806_one_label\all_images_except_missed_detections\04_汇总无框有标签文件的图像\背景\植被\images'
create_empty_labels_for_images(images_folder_path)
