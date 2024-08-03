import os

# 定义文件路径
img_directory = r'C:\Users\zcc\project\wayho\oil_detection\oil_identification\data\oil\imgs'  # 包含.img, .hdr, .jpg文件的目录
labels_txt_path = r'C:\Users\zcc\project\wayho\oil_detection\oil_identification\data\data_list/label_list_before-0619.txt'  # 包含文件路径的txt文档
extra_files_output_path = r'C:\Users\zcc\project\wayho\oil_detection\oil_identification\data\data_list\extra_files.txt'  # 保存多余文件名的txt文档

# 读取labels文件中的文件路径，并提取不带后缀的文件名
with open(labels_txt_path, 'r') as file:
    label_file_paths = file.read().splitlines()
label_base_names = set(os.path.splitext(os.path.basename(path))[0] for path in label_file_paths)

# 获取imgs文件夹下的文件名（不带后缀）
img_base_names = set()
for root, _, files in os.walk(img_directory):
    for file in files:
        base_name = os.path.splitext(file)[0]
        img_base_names.add(base_name)

# 找出在img_base_names中但不在label_base_names中的文件名
extra_files = img_base_names - label_base_names

# 保存多余文件名到txt文档
with open(extra_files_output_path, 'w') as output_file:
    for base_name in extra_files:
        output_file.write(base_name + '\n')

print(f'Extra file names saved to {extra_files_output_path}')
