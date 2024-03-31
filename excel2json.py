import pandas as pd
import json


def read_excel_to_dict(file_path):
    # 读取 Excel 文件
    df = pd.read_excel(file_path, dtype=str)

    # 创建一个空字典，用于存储拼接后的键值对
    result_dict = {}

    # 遍历所有非空行
    for index, row in df.iterrows():
        # 获取拼接后的键，第二列的值加下划线与第三列的值拼接
        key = f"{row['Page']}_{row['Row']}"
        # 检查键是否已存在
        if key in result_dict:
            print(f"Duplicate key found: {key}")
            # 如果键已存在，这里你可以选择进行一些处理，比如跳过该行或者合并值等
        else:
            # 将拼接后的键和第一列的值存储到字典中
            result_dict[key] = row['PANTONE Color']

    return result_dict


# 指定 Excel 文件路径
excel_file_path = r'C:\Documents\SyncFIoder\Work\Wayho\色卡数据\PANTONE_SOLID_COATED_INDEX.xlsx'

# 调用函数读取 Excel 文件并得到结果字典
result = read_excel_to_dict(excel_file_path)

# 打印结果字典
print(result)
# 指定保存 JSON 文件路径
json_file_path = r'C:\Documents\SyncFIoder\Work\Wayho\色卡数据\PANTONE_SOLID_COATED_INDEX.json'

# 保存为 JSON 文件
with open(json_file_path, 'w') as json_file:
    json.dump(result, json_file, indent=4)

# 打印保存的 JSON 文件路径
print(f"Result saved to: {json_file_path}")
