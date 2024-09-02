import os

def gather_file_paths(txt_paths=None, directories=None, extensions=None, recursive=False, target_folder_name=None):
    """
    统一收集文件路径，可以从一个或多个 .txt 文件和/或目录中获取路径。

    :param txt_paths: 包含路径的 .txt 文件路径列表，可以为 None
    :param directories: 文件夹路径列表，可以为 None
    :param extensions: 要筛选的文件后缀列表，可以为 None
    :param recursive: 是否递归处理目录及其子目录，默认为 False
    :param target_folder_name: 只处理指定名称的文件夹，默认为 None
    :return: 合并后的文件路径列表
    """
    file_paths = []

    # 处理来自 .txt 文件中的路径
    if txt_paths:
        for txt_file in txt_paths:
            with open(txt_file, 'r') as file:
                paths = file.read().splitlines()
                # 移除每行两端的空白字符
                paths = [path.strip() for path in paths if path.strip()]
                file_paths.extend(paths)

    # 处理来自目录中的文件
    if directories:
        for directory in directories:
            if os.path.exists(directory):
                for root, dirs, files in os.walk(directory):
                    # 检查当前目录名是否匹配指定的目标文件夹名
                    if target_folder_name is None or os.path.basename(root) == target_folder_name:
                        # 筛选符合指定后缀的文件
                        for file_name in files:
                            if extensions:
                                if any(file_name.endswith(ext) for ext in extensions):
                                    file_paths.append(os.path.join(root, file_name))
                            else:
                                file_paths.append(os.path.join(root, file_name))

                    # 如果不递归，则跳出循环
                    if not recursive:
                        break
            else:
                print(f"目录不存在: {directory}")

    return file_paths

if __name__ == "__main__":
    # 示例用法
    txt_paths = [
        r'path_to_txt_file1.txt',
        r'path_to_txt_file2.txt'
    ]

    directories = [
        r'path_to_directory1',
        r'path_to_directory2'
    ]

    extensions = ['.jpg', '.png', '.txt']  # 要筛选的文件后缀
    recursive = True  # 是否递归处理子目录
    target_folder_name = None  # 只处理此名字的文件夹

    file_paths = gather_file_paths(txt_paths=txt_paths, directories=directories, extensions=extensions, recursive=recursive,
                                   target_folder_name=target_folder_name)

    print(file_paths)

