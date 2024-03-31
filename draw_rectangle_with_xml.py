import os
from my_utils.file_operations.io import read_image_with_PIL, read_voc_xml
from my_utils.visualization.draw import draw_bboxes_on_image

if __name__ == '__main__':
    img_folder = r""
    xml_folder = r""

    img_files = [f for f in os.listdir(img_folder)]
    # xml_files = [f for f in os.listdir(xml_folder)]
    for img_name in img_files:
        # 以图像为基准获取文件路径
        img_path = os.path.join(img_folder, img_name)
        xml_path = os.path.join(xml_folder, img_name[:-4])
        # 读取图像
        img = read_image_with_PIL(img_path)
        # 读取标签
        labels, bboxes = read_voc_xml(xml_path)
        if labels is not None and bboxes is not None:
            print("Labels:", labels)
            print("Bounding boxes:", bboxes)
        else:
            print(f"文件:{img_name},找不到对应的xml文件")
            # 绘制标签
        draw_bboxes_on_image(img, labels, bboxes, line_width=10, draw_label=False)
    print("end")
