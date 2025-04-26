import tkinter as tk
from PIL import ImageGrab, Image, ImageTk, ImageDraw
import threading
import time
from datetime import datetime

class ScreenshotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("实时截图工具")
        self.root.attributes('-fullscreen', True)  # 设置全屏
        self.root.attributes('-alpha', 0.5)  # 设置半透明，方便用户看到桌面
        self.root.configure(bg='black')  # 设置背景颜色

        # 创建一个画布用于显示桌面截图
        self.canvas = tk.Canvas(self.root, width=self.root.winfo_screenwidth(), height=self.root.winfo_screenheight())
        self.canvas.pack()

        # 初始化截图区域
        self.start_x = None
        self.start_y = None
        self.rect = None

        # 绑定鼠标事件
        self.canvas.bind('<Button-1>', self.on_start)
        self.canvas.bind('<B1-Motion>', self.on_drag)
        self.canvas.bind('<ButtonRelease-1>', self.on_release)

        # 启动实时更新桌面截图的线程
        self.update_screenshot_thread = threading.Thread(target=self.update_screenshot)
        self.update_screenshot_thread.daemon = True  # 设置为守护线程
        self.update_screenshot_thread.start()

    def update_screenshot(self):
        while True:
            try:
                # 截取桌面
                screenshot = ImageGrab.grab()
                # 转换为Tkinter可显示的图片
                photo = ImageTk.PhotoImage(screenshot)
                # 如果已经有截图，更新它，否则创建新的
                if not hasattr(self, 'photo_image'):
                    self.photo_image = self.canvas.create_image(0, 0, image=photo, anchor='nw')
                else:
                    self.canvas.itemconfig(self.photo_image, image=photo)
                self.canvas.image = photo  # 防止图片被垃圾回收
                time.sleep(0.5)  # 降低更新频率
            except Exception as e:
                print(f"截图更新失败: {e}")
                break

    def on_start(self, event):
        self.start_x = event.x
        self.start_y = event.y
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(self.start_x, self.start_y, self.start_x, self.start_y, outline='red', width=2)

    def on_drag(self, event):
        if self.rect:
            self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)

    def on_release(self, event):
        if self.rect:
            self.canvas.coords(self.rect, self.start_x, self.start_y, event.x, event.y)
            # 获取截图区域
            x1, y1, x2, y2 = self.start_x, self.start_y, event.x, event.y
            # 确保坐标顺序正确
            x1, x2 = min(x1, x2), max(x1, x2)
            y1, y2 = min(y1, y2), max(y1, y2)

            # 隐藏窗口并清空屏幕缓冲区
            self.root.withdraw()
            self.root.update_idletasks()  # 强制刷新窗口，确保隐藏操作完成
            time.sleep(0.1)  # 等待0.1秒，确保窗口隐藏

            # 截取并保存截图
            screenshot = ImageGrab.grab(bbox=(x1, y1, x2, y2))
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"screenshot_{timestamp}.png"
            screenshot.save(filename)
            print(f"截图已保存为: {filename}")

            # 恢复窗口
            self.root.deiconify()
            self.root.destroy()  # 关闭窗口

if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenshotApp(root)
    root.mainloop()
