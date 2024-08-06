import os

def remove_whitespace_from_txt_files(directory):
    # 遍历文件夹中的所有文件
    for filename in os.listdir(directory):
        # 检查文件是否为TXT文件
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            # 读取文件内容
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            # 删除空白字符
            new_content = ''.join(content.split())
            # 覆盖原有文件
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(new_content)
            print(f"Processed {filename}")

# 指定文件夹路径
folder_path = r'\\192.168.3.155\高光谱测试样本库\原油检测\00大庆现场测试\03标注数据以及模型文件\00数据和标签\dataset_20240806\negative_examples\labels'
remove_whitespace_from_txt_files(folder_path)
