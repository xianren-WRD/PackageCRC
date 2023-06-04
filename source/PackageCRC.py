import os
import binascii
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from intelhex import IntelHex
from PIL import Image, ImageTk

# 计算CRC32值
def calculate_crc32(file_path):
    with open(file_path, 'rb') as file:
        data = file.read()
    crc32 = binascii.crc32(data) & 0xFFFFFFFF
    return crc32

# 在文件末尾追加CRC32值并创建新的bin文件
def append_crc32(file_path):
    crc32 = calculate_crc32(file_path)
    crc32_bytes = crc32.to_bytes(4, 'little')

    # 路径拼接并规范化
    output_folder = os.path.join(os.path.dirname(file_path), '_UpgradeFileOutput')
    output_folder = os.path.normpath(output_folder)
    # 创建输出文件夹
    os.makedirs(output_folder, exist_ok=True)

    output_file_path = os.path.join(output_folder, os.path.basename(file_path))
    output_file_path = os.path.normpath(output_file_path)

    with open(file_path, 'rb') as file:
        data = file.read()
    with open(output_file_path, 'wb') as output_file:
        output_file.write(data)
        output_file.write(crc32_bytes)

    return output_file_path

# 转换为Intel Hex格式的hex文件
def convert_to_hex():
    start_address = address_entry.get()
    if not start_address:  # 如果地址为空，则默认为0x10000
        start_address = "0x10000"
    file_name = os.path.splitext(file_path)[0]  # 移除扩展名
    hex_file_path = os.path.join(os.path.dirname(file_path), '_UpgradeFileOutput', os.path.basename(file_name) + '.hex')
    hex_file_path = os.path.normpath(hex_file_path)

    # 在二进制文件末尾追加CRC32值并创建新的bin文件
    new_bin_file_path = append_crc32(file_path)

    ih = IntelHex()

    # 加载二进制文件，并设置起始地址
    ih.loadbin(new_bin_file_path, offset=int(start_address, 16))

    # 保存为hex文件
    ih.write_hex_file(hex_file_path)

    messagebox.showinfo("Conversion Completed", f"Hex file saved as: {hex_file_path}")

    # 关闭窗口
    window.quit()  # 或者使用 window.destroy()


# 选择文件并处理
def select_file():
    global file_path
    file_path = filedialog.askopenfilename(filetypes=[("Binary Files", "*.bin")])
    if file_path:
        address_entry.config(state=tk.NORMAL)  # 允许编辑地址输入框
        convert_button.config(state=tk.NORMAL)  # 允许点击转换按钮
        address_entry.focus_set()  # 输入框获得焦点
        address_entry.delete(0, tk.END)  # 清空输入框内容

        # 禁止再次选择文件
        file_button.config(state=tk.DISABLED)

# 创建窗口
window = tk.Tk()
window.title("PackageCRC")

# 输入框和转换按钮
frame = tk.Frame(window)
frame.pack(pady=10, anchor=tk.CENTER)

address_label = tk.Label(frame, text="Start Address (Hexadecimal):")
address_label.pack(side=tk.LEFT)
address_entry = tk.Entry(frame, state=tk.DISABLED, width=10)  # 初始状态禁止编辑地址输入
address_entry.pack(side=tk.LEFT, padx=5)

convert_button = tk.Button(frame, text="Convert", state=tk.DISABLED, command=convert_to_hex)
convert_button.pack(side=tk.LEFT, padx=5)

# 加载图标
icon_path = "resources/Text_File.ico"
if os.path.exists(icon_path):
    icon_image = Image.open(icon_path)
    icon_image = icon_image.resize((24, 24))  # 调整图标大小
    icon_photo = ImageTk.PhotoImage(icon_image)
    file_button = tk.Button(frame, image=icon_photo, command=select_file)
    file_button.image = icon_photo  # 保持图像的引用，避免被垃圾回收
    file_button.pack(side=tk.LEFT, padx=5)
else:
    file_button = tk.Button(frame, text="Select File", command=select_file)
    file_button.pack(side=tk.LEFT, padx=5)

# 设置窗口大小
window.geometry("400x60")
window.resizable(False, False)

# 运行窗口
window.mainloop()
