import os

# 指定文件夹路径
folder_path = r"C:\Users\Administrator\project\wayho\rgb_spectral_reconstruction\spectral_reconstruction_from_rgb_images\data\maxs800\maxs800"



# 存储找到的匹配文件的名字
matched_files = []
suffix = '.hdr'
match = '.img'
# 遍历每个文件名，检查是否存在对应的.hdr和.img文件

for root, dirs, files in os.walk(folder_path):
    root_dir = os.path.basename(root)
    # 处理指定的子文件夹
    if root_dir == 'process_remove_edges' or root_dir == 'fire_hydrants':
        # 获取文件路径列表
        for file_name in files:
            # 检查是否存在对应的.hdr和.img文件
            if file_name.endswith('.img'):
                img_file_name = file_name[:-4] + '.hdr'
                if img_file_name not in files:
                    matched_files.append(file_name)


# 输出找到的匹配文件名
print("匹配的文件名：", matched_files)