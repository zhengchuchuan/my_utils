import os

# 定义文件路径
img_directory = r'C:\Users\zcc\project\wayho\oil_detection\oil_identification\data\oil\imgs'  # 包含.img, .hdr, .jpg文件的目录
extra_files_list_path = r'C:\Users\zcc\project\wayho\oil_detection\oil_identification\data\data_list\extra_files.txt'  # 保存多余文件名的txt文档路径

# 读取txt文档中的文件名（不带后缀）
with open(extra_files_list_path, 'r') as file:
    extra_file_base_names = file.read().splitlines()

# 删除这些文件名对应的所有后缀文件
for base_name in extra_file_base_names:
    for extension in ['img', 'hdr', 'jpg']:
        file_path = os.path.join(img_directory, f"{base_name}.{extension}")
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted: {file_path}")

print("Deletion process completed.")
