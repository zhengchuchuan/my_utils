import cv2
import os
import numpy as np
from tqdm import tqdm


def reencode_images(txt_file_path, output_format='.png', output_dir=None):
    # 打开存储图像路径的txt文件
    with open(txt_file_path, 'r') as file:
        image_paths = file.readlines()

    # 遍历每一张图像路径
    for image_path in tqdm(image_paths):
        image_path = image_path.strip()  # 去掉路径两端的空白字符

        # 检查图像路径是否存在
        if not os.path.exists(image_path):
            print(f"Image path does not exist: {image_path}")
            continue

        # 如果文件已经是指定格式，则跳过
        if image_path.endswith(output_format):
            continue
        # 读取图像为二进制数据
        with open(image_path, 'rb') as img_file:
            img_data = img_file.read()

        # 使用 imdecode 解码图像
        image = cv2.imdecode(np.frombuffer(img_data, np.uint8), cv2.IMREAD_UNCHANGED)

        # 使用 imencode 编码图像为指定格式
        _, encoded_image = cv2.imencode(f'{output_format}', image)

        # 构建输出路径
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
            output_path = os.path.join(output_dir, os.path.basename(image_path))
        else:
            output_path = image_path

        # 将文件扩展名替换为新的格式
        output_path = os.path.splitext(output_path)[0] + f'{output_format}'

        # 保存重新编码的图像
        with open(output_path, 'wb') as out_file:
            out_file.write(encoded_image.tobytes())

        # print(f"Re-encoded and saved: {output_path}")


if __name__ == '__main__':
    txt_path = r'../data_list/20240830_temp_1.txt'
    output_format = '.png'
    # 不设置输出路径则原路径保存
    output_path = None
    reencode_images(txt_file_path=txt_path, output_format=output_format, output_dir=output_path)
