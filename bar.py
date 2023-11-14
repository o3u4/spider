import time
import tkinter as tk


class Bar:
    def __init__(self, total, color='default'):
        self.total = total
        self.color = color
        self.colors = {
            'default': '█',
            'black': '\033[30m█\033[0m',
            'red': '\033[31m█\033[0m',
            'green': '\033[32m█\033[0m',
            'yellow': '\033[33m█\033[0m',
            'blue': '\033[34m█\033[0m',
            'magenta': '\033[35m█\033[0m',
            'cyan': '\033[36m█\033[0m',
            'white': '\033[37m█\033[0m',
            'reset': '\033[0m'
        }
        self.bar_length = 50  # 条总长

    def value(self, progress):
        filled_length = int(self.bar_length * progress // self.total)  # 当前进度占长
        bar = (self.colors[self.color] * filled_length +
               '-' * (self.bar_length - filled_length))  # 构建字符串
        percentage = progress / self.total * 100  # 百分比
        return bar, percentage

    def prt(self, progress):
        bar = self.value(progress)[0]
        percentage = self.value(progress)[1]
        print(f'\rProgress: [{bar}] {percentage:.1f}%  {progress}/{self.total}', end='', flush=True)
        # end=''不换行, flush=True, 立即将输出刷新到终端

    def label_prt(self, progress, label, window):
        bar = self.value(progress)[0]
        percentage = self.value(progress)[1]
        label.config(text=f'\rProgress: [{bar}] {percentage:.1f}%  {progress}/{self.total}')
        window.update()

    @staticmethod
    def class_label_prt(progress, progressbar, window):     # 经典进度条
        progressbar['value'] = progress
        window.update()


if __name__ == '__main__':
    # 示例用法
    total_progress = 150
    # bar1 = Bar(total_progress, 'red')
    # for i in range(50, total_progress + 1):
    #     bar1.prt(i)
    #     time.sleep(0.1)
    root = tk.Tk()
    root.title("M3U8视频下载器")
    lb = tk.Label(root)
    lb.pack()
    bar2 = Bar(total_progress)
    for i in range(total_progress + 1):
        bar2.label_prt(i, lb)
    tk.mainloop()
