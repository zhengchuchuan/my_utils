import numpy as np


# 线性归一化数组
def linear_normalize(array, min_value, max_value, dtype=np.uint8):
    """
    :param array: 待归一化的数组
    :param min_value: 归一化后的最小值
    :param max_value: 归一化后的最大值
    :param dtype: 输出数组的数据类型，默认为 np.uint8
    :return: 映射到指定范围的数组
    """
    # 检查数组是否包含无效值
    has_invalid_values = np.any(np.isnan(array)) or np.any(np.isinf(array))

    # 如果数组中有无效值，则将其替换为0
    if has_invalid_values:
        array = np.nan_to_num(array)

    # 计算数组的范围
    array_min = np.min(array)
    array_range = np.ptp(array)

    # 如果范围为0，则将数组全部设置为 min_value，避免除以0的错误
    if array_range == 0:
        normalized_array = np.full_like(array, min_value, dtype=dtype)
    else:
        # 线性映射
        normalized_array = (array - array_min) / array_range * (max_value - min_value) + min_value

    # 将数据类型转换为指定的类型
    normalized_array = normalized_array.astype(dtype)

    return normalized_array

