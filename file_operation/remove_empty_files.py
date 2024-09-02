import os

def remove_empty_files(directory):
    """
    删除指定目录及其子目录中的所有空文件
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if os.path.getsize(file_path) == 0:
                os.remove(file_path)
                print(f"Deleted empty file: {file_path}")

if __name__ == "__main__":
    directory = r'\\192.168.3.155\高光谱测试样本库\原油检测\00大庆现场测试\03标注数据以及模型文件\00数据和标签\dataset_20240806_one_label\source_big_label'
    remove_empty_files(directory)
