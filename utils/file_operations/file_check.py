import os


def check_file_correspondence(folder_1, folder_2):
    """
    检查不同后缀的文件去除文件名后是否一一对应
    :param folder_1:
    :param folder_2:
    :return:
    """
    # 获取文件夹下的所有文件名
    file_list_1 = os.listdir(folder_1)
    file_list_2 = os.listdir(folder_2)
    # 分离文件名(路径名)和拓展名,return [文件名,带点后缀名如.jpg]
    file_name_list_1, file_suffix_list_1 = [os.path.splitext(file) for file in file_list_1]
    file_name_list_2, file_suffix_list_2 = [os.path.splitext(file) for file in file_list_2]
    # 计算补集,即为缺失文件
    missing_list_2_files = set(file_name_list_1) - set(file_name_list_2)
    missing_list_1_files = set(file_name_list_2) - set(file_name_list_1)
    # 有缺失文件
    if missing_list_1_files:
        print("{0}以下的文件缺少对应的文件:".format(folder_1))
        for file in missing_list_1_files:
            print(file + file_suffix_list_1)
    if missing_list_2_files:
        print("{0}以下的文件缺少对应的文件:".format(folder_2))
        for file in missing_list_2_files:
            print(file + file_suffix_list_2)
    # 无缺失文件
    if not missing_list_2_files and not missing_list_1_files:
        print("所有文件一一对应。")


def check_file_exists(path):
    """
    检查指定路径的文件是否存在
    :param path: 文件的完整路径
    :return: 存在返回 True,否则返回 False
    """
    try:
        if os.path.exists(path):
            if os.path.isfile(path):
                return True
            else:
                return False
                print("The specified path is a folder.")
        else:
            return False
            print("File does not exist.")
    except FileNotFoundError:
        print("File does not exist.")
    except IsADirectoryError:
        print("The specified path is a folder.")
    except Exception as error:
        print(f"An error occurred: {error}")


def check_folder_exists(path):
    """
    检查文件夹是否存在,如果不存在则创建该文件夹
    :param path: 文件夹路径
    :return: 文件夹路径存在,并且是文件夹return True,非文件夹 return false
             文件夹路径不存在则在该路径下创建文件夹并 return True
    """
    try:
        if os.path.exists(path):
            if os.path.isdir(path):
                return True
            else:
                return False
                print("File is not a folder")
        else:
            os.makedirs(path)
            return True
    except FileNotFoundError:
        print("File does not exist.")
    except NotADirectoryError:
        print("The path is not a directory.")
    except Exception as error:
        return f"An error occurred: {error}"


