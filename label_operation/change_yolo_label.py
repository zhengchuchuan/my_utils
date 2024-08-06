import os
from tqdm import tqdm
from collections import defaultdict


def modify_yolo_labels(image_paths):
    original_label_counts = defaultdict(int)
    modified_label_counts = defaultdict(int)

    for path in tqdm(image_paths):
        path = path.strip()
        if not os.path.exists(path):
            print(f"File {path} does not exist.")
            continue

        with open(path, 'r') as file:
            lines = file.readlines()

        for line in lines:
            parts = line.strip().split()
            if len(parts) < 2:
                continue
            index = int(parts[0])
            original_label_counts[index] += 1

        modified_lines = []

        for line in lines:
            parts = line.strip().split()
            if len(parts) < 2:
                continue

            index = int(parts[0])
            if index == 1:
                continue
            elif index in [0, 2, 3]:
                new_line = '0 ' + ' '.join(parts[1:])
                modified_lines.append(new_line)
                modified_label_counts[0] += 1

        with open(path, 'w') as file:
            file.write('\n'.join(modified_lines) + '\n')

    print("Original label counts:")
    for label, count in original_label_counts.items():
        print(f"Label {label}: {count}")

    print("Modified label counts:")
    for label, count in modified_label_counts.items():
        print(f"Label {label}: {count}")


if __name__ == '__main__':
    image_path_list = r'C:\Users\zcc\project\python_project\my_utils\exp\data_list_all_20240805.txt'
    with open(image_path_list, 'r') as fin:
        image_paths = [line.replace('\n', '').replace('images', 'labels').replace(os.path.splitext(line)[1], '.txt') for
                       line in fin]
    label_paths = [path.replace('images', 'labels').replace(os.path.splitext(path)[1], '.txt') for path in image_paths]
    modify_yolo_labels(label_paths)
