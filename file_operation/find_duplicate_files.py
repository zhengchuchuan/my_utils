def find_duplicate_files(input_file, output_file):
    # 读取输入文件的内容
    with open(input_file, 'r') as f:
        lines = f.read().splitlines()

    # 使用字典统计每个文件名出现的次数
    file_count = {}
    for line in lines:
        if line in file_count:
            file_count[line] += 1
        else:
            file_count[line] = 1

    # 找出重复的文件名（出现次数大于1的文件名）
    duplicate_files = [file for file, count in file_count.items() if count > 1]

    # 将重复的文件名写入到输出文件中
    with open(output_file, 'w') as out_f:
        for file in duplicate_files:
            out_f.write(file + '\n')

    print(f"重复的文件名已保存到 {output_file} 中.")

# 使用示例
input_file_path = r'../data_list/20240830_temp.txt'
output_file_path = r'../data_list/duplicates.txt'

find_duplicate_files(input_file_path, output_file_path)
