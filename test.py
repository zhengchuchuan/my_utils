import exifread

import exifread


def compare_exif(image_path1, image_path2):
    with open(image_path1, 'rb') as file1, open(image_path2, 'rb') as file2:
        tags1 = exifread.process_file(file1)
        tags2 = exifread.process_file(file2)

    # 移除可能不同的标签
    tags1.pop('JPEGThumbnail', None)
    tags2.pop('JPEGThumbnail', None)

    # 比较字段
    different_fields = []

    # 比较每个字段的值
    for tag in tags1:
        if tag in tags2:
            if tags1[tag].values != tags2[tag].values:
                different_fields.append(tag)
        else:
            different_fields.append(tag)

    for tag in tags2:
        if tag not in tags1:
            different_fields.append(tag)
    if different_fields: # 如果有不同的字段
        return False
    else:
        return True


# 使用示例
image1_path = r"C:\Users\Administrator\Pictures\Photos\摄影原片\中国\四川省\绵阳市\西科大\毕业照\SWUST_444.ARW"
image2_path = r"C:\Users\Administrator\Pictures\Photos\摄影原片\中国\四川省\绵阳市\西科大\毕业照\SWUST_444.ARW"
differences = compare_exif(image1_path, image2_path)

print("Different fields:", differences)
