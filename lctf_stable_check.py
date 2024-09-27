import os
import sys
import numpy as np
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext, ttk
from spectral import open_image
import threading

# 日志变量，用于记录错误信息
log_messages = ""

# 存储超出阈值的文件路径
error_images = []

# 在全局范围内添加一个标志变量
is_running = True

def set_byte_order(hdr_file):
    with open(hdr_file, mode='r', encoding='utf-8') as f:
        lines = f.readlines()
    with open(hdr_file, mode='w', encoding='utf-8') as f:
        for line in lines:
            if "Date" in line or "byte order" in line or "project class" in line or len(line) == 0:
                continue
            f.write(line)
        f.writelines("\nbyte order = 0")

# 检查与 hdr 文件对应的 img 文件是否存在
def open_hdr_img(hdr_file):
    global log_messages
    img_file = hdr_file.replace('.hdr', '.img')  # 获取与 hdr 文件对应的 img 文件路径

    if not os.path.exists(img_file):
        # 如果 img 文件不存在，记录到日志并跳过该文件
        log_messages += f"跳过文件 {hdr_file}: 对应的 img 文件不存在\n"
        return None

    try:
        set_byte_order(hdr_file)
        scr_img = open_image(hdr_file)
        return scr_img[:, :, :]
    except IOError as e:
        # 如果读取 img 文件失败，记录到日志并跳过该文件
        error_message = f"无法读取文件：{hdr_file}，错误信息：{e}"
        log_messages += error_message + "\n"
        return None

# 计算两幅图像的平均像素误差
def calculate_normalized_error(ref_img, calc_img):
    if ref_img.shape != calc_img.shape:
        log_messages += f"Shape mismatch: Reference image shape {ref_img.shape}, Calculated image shape {calc_img.shape}\n"
        return None  # 尺寸不匹配

    # 计算绝对误差
    absolute_error = np.abs(ref_img - calc_img)

    # 计算平均误差
    mean_error = np.mean(absolute_error)

    # 获取图像数据类型的最大值
    max_gray_value = np.iinfo(ref_img.dtype).max  # 适用于整数类型
    # 如果图像是浮点类型，您可能需要手动设置最大值，例如：
    # max_gray_value = 1.0  # 对于0到1之间的浮点图像

    # 计算标准化误差
    if max_gray_value == 0:
        return None  # 避免除以零的情况

    normalized_error = mean_error / max_gray_value

    return normalized_error

# 打开文件对话框选择参考img文件
def select_reference_img():
    file_path = filedialog.askopenfilename(filetypes=[("HDR files", "*.hdr"), ("All files", "*.*")])
    if file_path:
        reference_img_path.set(file_path)

# 打开文件夹对话框选择计算img文件路径
def select_calc_img_path():
    folder_path = filedialog.askdirectory()
    if folder_path:
        calc_img_path.set(folder_path)

# 保存结果到txt文件
def save_results():
    global error_images
    folder_path = calc_img_path.get()
    if not error_images:
        messagebox.showinfo("信息", "没有需要保存的超出阈值的文件路径")
        return

    # 保存文件名
    save_file = os.path.join(folder_path, "error_images.txt")

    try:
        with open(save_file, 'w', encoding='utf-8') as f:
            f.write("\n".join(error_images))
        messagebox.showinfo("保存成功", f"文件已保存到: {save_file}")
    except IOError as e:
        messagebox.showerror("保存失败", f"无法保存文件：{e}")

# 终止计算的线程函数
def stop_calculation():
    global is_running
    is_running = False
    progress_bar['value'] = 0  # 清空进度条

# 开始计算的线程函数
def calculate_in_thread():
    global log_messages, error_images, is_running
    log_messages = ""  # 清空日志信息
    error_images = []  # 清空之前的错误文件路径
    ref_img_file = reference_img_path.get()
    folder_path = calc_img_path.get()
    threshold = float(error_threshold.get()) / 100

    if not os.path.exists(ref_img_file):
        messagebox.showerror("错误", "参考图像文件不存在")
        return
    if not os.path.exists(folder_path):
        messagebox.showerror("错误", "计算图像路径不存在")
        return

    # 读取参考图像
    ref_img = open_hdr_img(ref_img_file)
    if ref_img is None:
        messagebox.showerror("错误", "无法读取参考图像")
        return

    # 计算误差
    total_files = 0
    skipped_files = 0
    files = []
    for root, _, filenames in os.walk(folder_path):
        for file in filenames:
            if file.endswith(".hdr"):
                files.append(os.path.join(root, file))

    # 更新进度条
    total_files = len(files)
    for index, hdr_path in enumerate(files):
        if not is_running:  # 检查是否应终止
            break
        calc_img = open_hdr_img(hdr_path)
        if calc_img is None:
            skipped_files += 1
            continue

        error = calculate_normalized_error(ref_img, calc_img)
        if error is not None and error > threshold:
            error_images.append(hdr_path)

        # 更新进度条和日志
        progress_bar['value'] = (index + 1) / total_files * 100
        log_textbox.delete(1.0, tk.END)
        log_textbox.insert(tk.END, log_messages)

    result_text = f"计算完成！总文件数: {total_files}，超出阈值的文件数: {len(error_images)}，跳过文件数: {skipped_files}\n"
    result_text += "\n".join(error_images)
    result_textbox.delete(1.0, tk.END)  # 清空之前的内容
    result_textbox.insert(tk.END, result_text)

# 开始计算
def start_calculation():
    global is_running
    is_running = True  # 重置运行标志
    # 创建并启动新线程
    thread = threading.Thread(target=calculate_in_thread)
    thread.start()

# 清空结果显示
def clear_result():
    result_textbox.delete(1.0, tk.END)  # 清空文本框内容
    log_textbox.delete(1.0, tk.END)  # 清空日志窗口内容

# 创建主窗口
root = tk.Tk()
root.title("LCTF Stable Check")

# 定义UI变量
reference_img_path = tk.StringVar()
calc_img_path = tk.StringVar()
error_threshold = tk.StringVar(value="10")

# 参考img文件
tk.Label(root, text="参考img文件:").grid(row=0, column=0, sticky="e")
tk.Entry(root, textvariable=reference_img_path, width=50).grid(row=0, column=1)
tk.Button(root, text="...", command=select_reference_img).grid(row=0, column=2)

# 计算img文件路径
tk.Label(root, text="计算img文件路径:").grid(row=1, column=0, sticky="e")
tk.Entry(root, textvariable=calc_img_path, width=50).grid(row=1, column=1)
tk.Button(root, text="...", command=select_calc_img_path).grid(row=1, column=2)

# 允许百分比误差
tk.Label(root, text="允许百分比误差:").grid(row=2, column=0, sticky="e")
tk.Spinbox(root, from_=0, to=100, textvariable=error_threshold, width=5).grid(row=2, column=1, sticky="w")

# 开始计算按钮
tk.Button(root, text="开始计算", command=start_calculation).grid(row=3, column=1, sticky="w")
# 添加终止按钮
tk.Button(root, text="终止计算", command=stop_calculation).grid(row=3, column=2, sticky="w")

# 进度条
progress_bar = ttk.Progressbar(root, length=400, mode='determinate')
progress_bar.grid(row=4, column=0, columnspan=2, sticky='ew', padx=5, pady=5)

# 计算结果显示
tk.Label(root, text="计算结果:").grid(row=5, column=0, sticky="e")
result_textbox = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, width=60)
result_textbox.grid(row=5, column=1, columnspan=2, sticky="nsew")

# 日志显示
tk.Label(root, text="日志信息:").grid(row=6, column=0, sticky="e")
log_textbox = scrolledtext.ScrolledText(root, wrap=tk.WORD, height=10, width=60)
log_textbox.grid(row=6, column=1, columnspan=2, sticky="nsew")

# 保存结果按钮
tk.Button(root, text="保存结果", command=save_results).grid(row=7, column=1, sticky="w")
# 清空结果按钮
tk.Button(root, text="清空结果", command=clear_result).grid(row=7, column=2, sticky="w")



# 设置行列权重
root.columnconfigure(1, weight=1)
root.rowconfigure(5, weight=1)

root.mainloop()
