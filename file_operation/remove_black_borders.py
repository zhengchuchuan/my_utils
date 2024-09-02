import os
import cv2
import numpy as np
from tqdm import tqdm

def remove_borders(image):
    if image.shape[2] == 4:  # Image has an alpha channel
        alpha_channel = image[:, :, 3]  # Extract the alpha channel
        # Find rows and columns where alpha is not 0
        rows = np.any(alpha_channel != 0, axis=1)
        cols = np.any(alpha_channel != 0, axis=0)
    else:  # Image does not have an alpha channel (RGB image)
        rgb_image = image[:, :, :3]
        # Find rows and columns where RGB is not all black or all white
        rows = np.any((rgb_image != [0, 0, 0]) & (rgb_image != [255, 255, 255]), axis=1)
        cols = np.any((rgb_image != [0, 0, 0]) & (rgb_image != [255, 255, 255]), axis=0)

    # Get the bounding box of the non-transparent/non-black/non-white region
    top, bottom = np.argmax(rows), len(rows) - np.argmax(rows[::-1])
    left, right = np.argmax(cols), len(cols) - np.argmax(cols[::-1])

    # Crop the image to the bounding box
    cropped_image = image[top:bottom, left:right]

    return cropped_image

def process_images_in_folder(folder_path):
    for filename in tqdm(os.listdir(folder_path)):
        if filename.endswith(".png"):
            image_path = os.path.join(folder_path, filename)
            image = cv2.imdecode(np.fromfile(image_path, dtype=np.uint8), cv2.IMREAD_UNCHANGED)

            # Check if the image is valid
            if image is not None:
                processed_image = remove_borders(image)

                # Save the processed image, overwriting the original
                image_type = '.png'
                success, img_encoded = cv2.imencode(image_type, processed_image)
                if not success:
                    raise ValueError(f"Could not encode image to format: {image_type}")
                img_encoded.tofile(image_path)
            else:
                print(f"Failed to read image: {filename}")

# 使用文件夹路径来调用函数
folder_path = r'\\192.168.3.155\高光谱测试样本库\原油检测\00大庆现场测试\03标注数据以及模型文件\00数据和标签\dataset_20240806_one_label\generate_samples\20240814\0'
process_images_in_folder(folder_path)
