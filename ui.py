import tkinter as tk
from tkinter import ttk, font
import math


class HeartRateGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Heart Rate Monitor")
        # 设置窗口无边框和透明背景
        self.root.overrideredirect(True)
        self.root.attributes("-transparentcolor", "#121212")
        self.root.attributes("-topmost", True)
        self.root.configure(bg="#121212")

        # 设置窗口位置和大小
        window_width = 200
        window_height = 200
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = screen_width - window_width * 0.75
        x = int(x)
        y = 0  # 可以设为 10 等值，留出一点边距
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        # self.root.geometry("200x200+100+100")

        # 创建画布
        self.canvas = tk.Canvas(
            self.root,
            width=200,
            height=200,
            bg="#121212",
            highlightthickness=0
        )
        self.canvas.pack()


        # 创建心率显示文本
        self.heart_rate_font = font.Font(family="Helvetica", size=42, weight="bold")
        self.heart_rate_text = self.canvas.create_text(
            100, 90,
            text="--",
            font=self.heart_rate_font,
            fill="#555555"
        )





        # 绑定鼠标事件
        self.canvas.bind("<ButtonPress-1>", self.start_move)
        self.canvas.bind("<B1-Motion>", self.on_move)
        self.canvas.bind("<Button-3>", self.show_context_menu)

        # 创建右键菜单
        self.context_menu = tk.Menu(self.root, tearoff=0, bg="#1a1a1a", fg="#cccccc")
        self.context_menu.add_command(label="Exit", command=self.root.destroy)



    def start_move(self, event):
        self.x = event.x_root - self.root.winfo_x()
        self.y = event.y_root - self.root.winfo_y()

    def on_move(self, event):
        x = event.x_root - self.x
        y = event.y_root - self.y
        self.root.geometry(f"+{x}+{y}")

    def show_context_menu(self, event):
        try:
            self.context_menu.tk_popup(event.x_root, event.y_root)
        finally:
            self.context_menu.grab_release()



    def update_heart_rate(self, heart_rate):
        # 根据心率值改变颜色
        if heart_rate < 60:  # 心率过低
            color = "#4da6ff"  # 柔和的蓝色
            pulse_color = "#4da6ff"
        elif heart_rate < 100:  # 正常心率
            color = "#66ff66"  # 柔和的绿色
            pulse_color = "#ff5555"
        elif heart_rate < 120:  # 偏高心率
            color = "#ffcc66"  # 柔和的橙色
            pulse_color = "#ffcc66"
        else:  # 过高心率
            color = "#ff6666"  # 柔和的红色
            pulse_color = "#ff6666"

        # 更新文本颜色
        self.canvas.itemconfig(self.heart_rate_text, text=f"{heart_rate}", fill=color)




