import os
import shutil

from tqdm import tqdm


def move_empty_label_files(source_image_paths, source_label_paths, target_folder):
    # 创建目标文件夹
    target_labels_folder = os.path.join(target_folder, 'labels')
    target_images_folder = os.path.join(target_folder, 'images')

    os.makedirs(target_labels_folder, exist_ok=True)
    os.makedirs(target_images_folder, exist_ok=True)

    # 遍历每个标签文件
    for i in tqdm(range(len(source_image_paths))):
        image_path = source_image_paths[i]
        label_path = source_label_paths[i]

        move_file = False

        # 检查标签文件是否存在
        if not os.path.exists(label_path):
            # 创建空标签文件
            open(label_path, 'w').close()
            move_file = True
        else:
            # 读取文件内容
            with open(label_path, 'r') as file:
                # 去除空行
                lines = file.readlines()
                lines = [line.strip() for line in lines if line.strip()]

            # 如果文件为空，则需要移动
            if not lines:
                move_file = True

        if move_file:
            # 移动标签文件到 labels 文件夹
            shutil.move(label_path, os.path.join(target_labels_folder, os.path.basename(label_path)))
            # 移动图片文件到 images 文件夹
            shutil.move(image_path, os.path.join(target_images_folder, os.path.basename(image_path)))



if __name__ == '__main__':
    image_path_list = r'C:\Users\zcc\project\python_project\my_utils\exp\data_list_all_20240805.txt'

    target_folder = r'C:\Users\zcc\project\wayho\oil_detection\yolov5-7.0\dataset\oil\empty_data'  # 替换为你的目标文件夹路径

    with open(image_path_list, 'r') as fin:
        image_paths = [line.replace('\n', '') for line in fin]
    label_paths = [path.replace('images', 'labels').replace(os.path.splitext(path)[1], '.txt') for path in image_paths]
    move_empty_label_files(image_paths, label_paths, target_folder)
