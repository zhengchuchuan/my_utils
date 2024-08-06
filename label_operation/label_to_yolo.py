import json
import os
import glob
from pathlib import Path


def labelme_to_yolo(json_folder):
    json_files = glob.glob(os.path.join(json_folder, '*.json'))

    for json_file in json_files:
        with open(json_file, 'r') as f:
            data = json.load(f)

            # Extract image dimensions
            image_width = data['imageWidth']
            image_height = data['imageHeight']

            # Create corresponding YOLO format text file
            base_filename = os.path.splitext(os.path.basename(json_file))[0]
            txt_filename = os.path.join(json_folder, f'{base_filename}.txt')

            with open(txt_filename, 'w') as txt_file:
                for shape in data['shapes']:
                    label = shape['label']
                    if label == '1':
                        label = '0'
                    points = shape['points']

                    # Calculate YOLO format coordinates
                    x_center = (points[0][0] + points[1][0]) / (2 * image_width)
                    y_center = (points[0][1] + points[1][1]) / (2 * image_height)
                    width = abs(points[1][0] - points[0][0]) / image_width
                    height = abs(points[1][1] - points[0][1]) / image_height

                    # Write YOLO format line to file
                    txt_file.write(f"{label} {x_center:.6f} {y_center:.6f} {width:.6f} {height:.6f}\n")


# Example usage:
json_folder = r'C:\Users\zcc\project\wayho\oil_detection\temp\generate\labels'
labelme_to_yolo(json_folder)
