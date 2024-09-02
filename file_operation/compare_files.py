def find_common_files(file1, file2, output_file):
    # 读取第一个文件的内容
    with open(file1, 'r') as f1:
        files1 = set(f1.read().splitlines())

    # 读取第二个文件的内容
    with open(file2, 'r') as f2:
        files2 = set(f2.read().splitlines())

    # 找出两个文件中相同的文件名
    common_files = files1.intersection(files2)

    #
    with open(output_file, 'w') as out_f:
        for file in common_files:
            out_f.write(file + '\n')

    print(f"相同的文件名已保存到 {output_file} 中.")


file_path_1 =  r'../data_list/20240830_temp.txt'
file_path_2 = r'../data_list/20240830_temp_1.txt'
save_path = r'../data_list/temp.txt'

find_common_files(file_path_1, file_path_2 ,save_path)
