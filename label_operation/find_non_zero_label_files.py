import os


def find_non_zero_label_files(directory):
    non_zero_label_files = []

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".txt") and file != "classes.txt":
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as f:
                    lines = f.readlines()
                    for line in lines:
                        label_index = int(line.split()[0])
                        if label_index != 0:
                            non_zero_label_files.append(file_path)
                            break

    return non_zero_label_files


if __name__ == "__main__":
    directory = r"D:\wayho\oil_detection\data"  # 请替换为你的目标目录路径
    non_zero_label_files = find_non_zero_label_files(directory)

    print("Files with non-zero label indices:")
    for file_path in non_zero_label_files:
        print(file_path)
