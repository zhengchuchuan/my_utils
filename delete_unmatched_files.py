import os


def delete_unmatched_files(folder_path):
    # 获取所有jpg和txt文件名（不包含扩展名）
    jpg_files = {os.path.splitext(f)[0] for f in os.listdir(folder_path) if f.endswith('.jpg')}
    txt_files = {os.path.splitext(f)[0] for f in os.listdir(folder_path) if f.endswith('.txt')}

    # 找出没有对应文件的文件名
    unmatched_jpg = jpg_files - txt_files
    unmatched_txt = txt_files - jpg_files

    # 删除没有对应的jpg文件
    for filename in unmatched_jpg:
        jpg_path = os.path.join(folder_path, filename + '.jpg')
        os.remove(jpg_path)
        print(f"Deleted: {jpg_path}")

    # 删除没有对应的txt文件
    for filename in unmatched_txt:
        txt_path = os.path.join(folder_path, filename + '.txt')
        os.remove(txt_path)
        print(f"Deleted: {txt_path}")


# 使用示例
folder_path = r'C:\Users\zcc\project\wayho\oil_detection\zcc_picked'  # 替换为实际的文件夹路径
delete_unmatched_files(folder_path)
