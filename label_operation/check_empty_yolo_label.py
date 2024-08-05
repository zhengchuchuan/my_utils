import os
import shutil


def move_empty_label_files(source_image_folder,source_label_folder, target_folder):
    # 创建目标文件夹
    labels_folder = os.path.join(target_folder, 'labels')
    imgs_folder = os.path.join(target_folder, 'imgs')
    os.makedirs(labels_folder, exist_ok=True)
    os.makedirs(imgs_folder, exist_ok=True)

    # 列出文件夹中的所有文件
    files = os.listdir(source_label_folder)

    # 过滤掉 classes.txt 文件
    txt_files = [f for f in files if f.endswith('.txt') and f != 'classes.txt']

    # 遍历每个TXT文件
    for txt_file in txt_files:
        file_path = os.path.join(source_label_folder, txt_file)

        # 读取文件内容
        with open(file_path, 'r') as file:
            lines = file.readlines()

        # 如果文件为空，则需要移动
        if not lines:
            # 找到对应的图像文件
            image_file_jpg = txt_file.replace('.txt', '.jpg')
            image_file_png = txt_file.replace('.txt', '.png')

            image_file_jpg_path = os.path.join(source_image_folder, image_file_jpg)
            image_file_png_path = os.path.join(source_image_folder, image_file_png)

            # 移动标签文件到 labels 文件夹
            shutil.move(file_path, os.path.join(labels_folder, txt_file))

            # 移动对应的图像文件到 imgs 文件夹
            if os.path.exists(image_file_jpg_path):
                shutil.move(image_file_jpg_path, os.path.join(imgs_folder, image_file_jpg))
            elif os.path.exists(image_file_png_path):
                shutil.move(image_file_png_path, os.path.join(imgs_folder, image_file_png))


# 使用示例
source_label_folder = 'D:\wayho\oil_detection\data\have_label\labels_0'  # 替换为你的源文件夹路径
source_image_folder = 'D:\wayho\oil_detection\data\have_label\imgs'  # 替换为你的源文件夹路径
target_folder = 'D:\wayho\oil_detection\data\have_label\labels_0_without_shadow'  # 替换为你的目标文件夹路径
move_empty_label_files(source_image_folder,source_label_folder, target_folder)
