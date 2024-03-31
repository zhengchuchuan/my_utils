from PIL import ImageDraw, ImageFont


def draw_bboxes_on_image(img, labels, bboxes, font_size=12, font_color='red', line_width=5, line_color='red', draw_label=True):
    """
    在图像上绘制包围框和标签



    :param img: 要绘制的图像，PIL格式的图像对象
    :param labels: 标签列表
    :param bboxes: 包围框坐标列表，每个包围框是一个四元组(xmin, ymin, xmax, ymax)
    :param font_size: 字体尺寸 px
    :param font_color: 字体颜色
    :param line_width: 线条粗细 px
    :param line_color: 线条颜色
    :param draw_label: 是否绘制标签

    :return: 绘制了包围框和标签的图像，PIL格式的图像对象
    """
    # 创建绘图对象
    draw = ImageDraw.Draw(img)

    # 设置字体和字体大小
    font = ImageFont.truetype("arial.ttf", font_size)

    for label, bbox in zip(labels, bboxes):
        # 提取包围框坐标
        xmin, ymin, xmax, ymax = bbox
        # 绘制矩形框
        draw.rectangle([xmin, ymin, xmax, ymax], outline=line_color, width=line_width)
        # 绘制标签文本
        if draw_label is True:
            # 计算标签文本的包围框
            label_bbox = draw.textbbox((xmin, ymin), label, font=font)
            # 获取包围框的左下角坐标
            label_x = label_bbox[0]
            label_y = label_bbox[1] - font.size - line_width / 2
            # 绘制标签文本,绘制在标签左上角
            draw.text((label_x, label_y), label, fill=font_color, font=font)

    return img
