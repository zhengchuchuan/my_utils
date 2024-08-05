import numpy as np
import matplotlib.pyplot as plt

# 生成x值，从400到700，间隔为10
x = np.linspace(400, 700, 31)

# 生成单调上升曲线，同时添加噪声
ground_truth = np.array([
    0.01, 0.03333333, 0.06266667, 0.125, 0.11333333, 0.17666667,
    0.22, 0.21333333, 0.26666667, 0.312, 0.28, 0.36666667,
    0.35, 0.43333333, 0.46666667, 0.4, 0.43333333, 0.46666667,
    0.58, 0.53333333, 0.52666667, 0.65, 0.71333333, 0.76666667,
    0.77, 0.83333333, 0.86666667, 0.912, 0.83333333, 0.76666667,
    0.64
])
noise = np.random.normal(0, 0.015, len(x))  # 调整标准差以控制噪声的强度
MST_plius_plus = ground_truth + noise
# 计算相关系数
corr_coefficient = np.corrcoef(ground_truth, MST_plius_plus)[0, 1]
# 打印相关系数
print("Correlation Coefficient:", corr_coefficient)

# 打印x和MST_plius_plus的值
print("x:", x)
print("MST_plius_plus:", MST_plius_plus)

# 绘制曲线图
plt.plot(x, MST_plius_plus, label='MST_plius_plus')
plt.plot(x, ground_truth, label='Ground Truth', linestyle='--', color='red')
plt.xlabel('Wavelength(nm)')
plt.ylabel('Intensity')
plt.title('Simulated Hyperspectral Image')
plt.legend()
plt.show()
