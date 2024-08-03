import cv2
import matplotlib.pyplot as plt

# 读取BMP图像，默认是以BGR格式存储的
image_bgr = cv2.imread(r"C:\Users\Administrator\wayho\rgb_spectral_reconstruction\spectral_reconstruction_from_rgb_images\data\maxs800\maxs800_development_board_camera\test\MAX_G_0010_Color_4203_1024.tif.bmp")

# 检查图像是否成功加载
if image_bgr is None:
    print("Error: 图像加载失败")
else:
    # 分离 BGR 通道
    B, G, R = cv2.split(image_bgr)


    # 创建新的图像，保持蓝色通道不变，将绿色通道映射到红色和绿色通道
    image_custom = cv2.merge([B,G,R])

    # 使用 Matplotlib 显示图像G
    plt.imshow(image_custom)
    plt.axis('off')  # 不显示坐标轴
    plt.title('Custom Mapped Image')
    plt.show()
