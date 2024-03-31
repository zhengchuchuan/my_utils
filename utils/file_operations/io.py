import os
import cv2
import numpy as np
import xml.etree.ElementTree as ET
from xml.dom import minidom
from PIL.Image import Image
from osgeo import gdal, gdal_array

"""
包括文件I/O函数
--------------
读取模块

--------------
存储模块

--------------
"""


def read_image_with_cv2(path):
    # dtype对于tif图像需要切换成uint16

    image = cv2.imdecode(np.fromfile(path, dtype=np.uint8), cv2.IMREAD_UNCHANGED)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    return image


# 使用PIL读取图像
def read_image_with_PIL(image_path):
    try:
        image = Image.open(image_path)
        return image
    except Exception as e:
        print("An error occurred:", e)
        return None


# 读取多通道的tif文件
def read_tif_with_gdal(path):
    """
    读取tif文件,并将其转换为ndarray格式
    返回:数组数据,通道数,高度,宽度
    """
    try:
        dataset = gdal.Open(path, gdal.GA_Update)
        if dataset is None:
            raise IOError("无法打开TIF文件，请检查文件路径。")
    except IOError as e:  # IO异常
        print(str(e))
    except Exception as e:  # 其他异常
        print("其他异常：", str(e))
    # 获取TIF文件的通道数
    channels = dataset.RasterCount
    # 获取TIF文件的宽度和高度
    width = dataset.RasterXSize
    height = dataset.RasterYSize
    # 栅格数据的空间参考信息
    geo_trans = dataset.GetGeoTransform()
    # 投影信息
    geo_proj = dataset.GetProjection()
    # 将tif文件读取为ndarray数组,数据的格式(通道,高度,宽度)
    arr_dataset = dataset.ReadAsArray()  # 转为numpy格式
    del dataset
    return arr_dataset, channels, height, width, geo_trans, geo_proj


def read_voc_xml(xml_file_path):
    """
    读取VOC格式的xml文件，提取标签和包围框信息。

    参数：
    xml_file_path：xml文件的路径。

    返回值：
    labels：包含所有标签的列表。
    bboxes：包含所有包围框坐标的列表，每个包围框是一个四元组(xmin, ymin, xmax, ymax)。
    """
    tree = ET.parse(xml_file_path)
    root = tree.getroot()

    labels = []
    bboxes = []

    for obj in root.findall('object'):
        label = obj.find('name').text
        bbox = obj.find('bndbox')
        xmin = int(bbox.find('xmin').text)
        ymin = int(bbox.find('ymin').text)
        xmax = int(bbox.find('xmax').text)
        ymax = int(bbox.find('ymax').text)
        bboxes.append((xmin, ymin, xmax, ymax))
        labels.append(label)

    return labels, bboxes


def read_yolo_txt(path, classes, width, height):
    """
    读取yolo数据集的txt标签格式
    :param classes: 标签类别列表
    :param path: 读取的标签文件路径
    :param width: 标签对应的图像宽度
    :param height: 标签对应的图像高度
    :return: 列表,每个子元素列表对应值:[标签名,左上角x坐标,左上角y坐标,右下角x坐标,右下角y坐标].值为int形
    """
    yolo_datas = []  # txt文件中标签的列表
    with open(path, 'r') as f:
        # 一次读取一行
        for line in f.readlines():
            txt_line = line.strip().split(' ')
            label_index = int(float(txt_line[0].strip()))
            center_x = round(float(str(txt_line[1]).strip()) * width)
            center_y = round(float(str(txt_line[2]).strip()) * height)
            bbox_width = round(float(str(txt_line[3]).strip()) * width)
            bbox_height = round(float(str(txt_line[4]).strip()) * height)

            # 返回标签名,左上角坐标,右下角坐标
            data_line = [classes[label_index], center_x, center_y, bbox_width, bbox_height]
            yolo_datas.append(data_line)
    return yolo_datas


def write_image_with_cv2(path, img):
    # 解析文件名
    file_name = os.path.basename(path)
    # 文件拓展名
    file_extension = os.path.splitext(file_name)[1]
    # 创建目录(如果不存在)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    # RGB->BGR
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    # 保存文件到指定路径
    cv2.imencode(file_extension, img)[1].tofile(path)


def write_img_with_PIL(img_write_folder, file_name, arr):
    """
    使用PIL库保存png图像
    :param img_write_folder: 保存的文件夹路径
    :param file_name: 文件名(带后缀)
    :param arr: ndarray数组
    :return: None
    """
    # 生成保存路径
    img_write_path = os.path.join(img_write_folder, file_name)
    # 将数组转换为PIL图像 CHW->WHC
    img = Image.fromarray(arr)
    # 保存png图像
    img.save(img_write_path)


def write_tif_with_gdal(tif_write_path, base_tif_file_name, file_number, dataset, channels, width, height):
    """
    写入tif文件,
    参数:导出子图的路径,子图的数组,保存文件的类型,通道数,拆分的图像宽度,拆分的图像高度
    """
    # 生成子图文件路径,从000001开始
    # 创建与未切割文件同名的文件夹（如果不存在）
    tif_output_folder_path = os.path.join(tif_write_path, base_tif_file_name)
    if not os.path.exists(tif_output_folder_path):
        os.makedirs(tif_output_folder_path)
    # 文件名
    sub_tif_file_name = f"{base_tif_file_name}_{file_number}.tif"
    # 保存路径
    sub_tif_output_path = os.path.join(tif_output_folder_path, sub_tif_file_name)
    driver = gdal.GetDriverByName("GTiff")
    # 创建tif文件
    output_dataset = driver.Create(sub_tif_output_path, width, height, channels,
                                   gdal_array.GDALTypeCodeToNumericTypeCode(dataset.dtype))
    # 将子图数据写入TIF文件
    '''
    注意写入顺序,不同的图像可能需要更改,此次处理的图像尺寸格式为C,H,W,顺序错误图像会无法正确显示
    问题:似乎切割出来的图像色相有一定的偏差
    代办:自动识别图像的尺寸写入格式
    '''
    for channel in range(channels):
        output_dataset.GetRasterBand(channel + 1).WriteArray(dataset[channel, :, :])
    # 关闭TIF文件
    output_dataset = None


def write_voc_xml(folder_path, file_name, labels, bboxes, image_width, image_height, image_depth):
    """
    将标签和包围框信息保存为VOC格式的xml文件。

    参数：
    xml_file_path：xml文件的保存路径。
    labels：包含所有标签的列表。
    bboxes：包含所有包围框坐标的列表，每个包围框是一个四元组(xmin, ymin, xmax, ymax)。
    image_width: 图像宽度
    image_height: 图像高度
    image_depth: 图像通道数
    """
    xml_write_path = os.path.join(folder_path, file_name)
    # 创建XML根元素
    root = ET.Element("annotation")
    # 添加图像信息
    folder = ET.SubElement(root, "folder")
    folder.text = "VOC2007"  # 替换为您的图像所在的文件夹名称
    filename = ET.SubElement(root, "filename")
    filename.text = f"{file_name}.png"  # 替换为您的图像文件名和扩展名
    size = ET.SubElement(root, "size")
    width = ET.SubElement(size, "width")
    width.text = str(image_width)
    height = ET.SubElement(size, "height")
    height.text = str(image_height)
    depth = ET.SubElement(size, "depth")
    depth.text = str(image_depth)

    for label, bbox in zip(labels, bboxes):
        obj = ET.SubElement(root, "object")
        name = ET.SubElement(obj, "name")
        name.text = label
        pose = ET.SubElement(obj, "pose")
        pose.text = "Unspecified"
        truncated = ET.SubElement(obj, "truncated")
        truncated.text = "0"
        difficult = ET.SubElement(obj, "difficult")
        difficult.text = "0"
        bndbox = ET.SubElement(obj, "bndbox")
        xmin, ymin, xmax, ymax = bbox
        ET.SubElement(bndbox, "xmin").text = str(xmin)
        ET.SubElement(bndbox, "ymin").text = str(ymin)
        ET.SubElement(bndbox, "xmax").text = str(xmax)
        ET.SubElement(bndbox, "ymax").text = str(ymax)

    # 将XML文件格式化
    xml_string = ET.tostring(root, encoding="utf-8")
    dom = minidom.parseString(xml_string)
    pretty_xml_string = dom.toprettyxml(indent="    ")

    # 将格式化后的XML字符串保存为文件
    with open(xml_write_path, "w", encoding="utf-8") as f:
        f.write(pretty_xml_string)
