
def rect_center_to_bbox(center_x, center_y, width, height):
    """
    将中心坐标表示的矩形转为包围盒表示
    :param center_x: 中心点坐标x
    :param center_y: 中心点坐标y
    :param width: 矩形宽度
    :param height: 矩形长度
    :return: 包围盒的坐标[左上角坐标,右下角坐标]
    """
    # 计算矩形左下角和右上角顶点的坐标
    x1 = int(center_x - width / 2)
    y1 = int(center_y - height / 2)
    x2 = int(center_x + width / 2)
    y2 = int(center_y + height / 2)

    # 返回四个顶点的坐标
    return [(x1, y1),  (x2, y2)]
