import tkinter as tk
import random as rd
from answer import Answer


class Lattice:
    seq = []  # 01序列
    txt_list = []  # 转成tk的字符串
    buttons = []  # 按钮
    mny = 0  # 尝试次数
    root = tk.Tk()
    root.title('点亮所有格子')

    def __init__(self, scale, rule=2, mode=0):
        self.scale = scale  # 规模
        self.rule = rule    # 点击后多少距离的格子改变
        self.mode = mode    # 是否保证生成的矩阵有解
        self.init_rand()    # 首次初始化
        self.root.geometry(f"{self.scale}00x{self.scale}00")  # 界面大小

    def init_rand(self):
        if self.mode == 0:
            for odd in range(self.scale ** 2):
                n = rd.randint(0, 1)
                self.seq.append(n)
                t = tk.StringVar()
                self.txt_list.append(t)
        else:
            init = Answer(self.scale, self.rule)
            self.seq = init.sol_sys()
            for odd in range(self.scale ** 2):
                t = tk.StringVar()
                self.txt_list.append(t)

        for i in range(self.scale ** 2):
            self.txt_list[i].set(str(self.seq[i]))

    def change(self, x, y):  # 点击后改变的规则
        for xi in range(self.scale):
            for yj in range(self.scale):
                if self.dist((x, y), (xi, yj)) <= self.rule:
                    if self.txt_list[self.scale * xi + yj].get() == '0':
                        self.txt_list[self.scale * xi + yj].set('1')
                    else:
                        self.txt_list[self.scale * xi + yj].set('0')
        self.mny += 1

    def popup(self):
        num = 0
        for tx in self.txt_list:
            if tx.get() == '1':
                num += 1
        up = tk.Toplevel()
        up.geometry("400x60")
        label = tk.Label(up)
        if num == self.scale ** 2:
            label.config(text=f'共花了{self.mny}步完成!')
            label.pack()
        else:
            label.config(text='未完成')
            label.pack()
        lab = tk.Label(up)
        target = [1 for x in range(self.scale ** 2)]
        asw = Answer(self.scale, self.rule)
        ans_list = asw.answer(self.seq, target)
        if ans_list:
            lab.config(text=f'答案为:{", ".join(str(x) for x in ans_list)}')
        else:
            lab.config(text='无解')
        lab.pack()

    def start_ui(self):  # 启动ui界面
        # 使用grid布局排列按钮，并调整行和列的大小
        for i in range(self.scale):
            self.root.rowconfigure(i, weight=1)
            self.root.columnconfigure(i, weight=1)
            for j in range(self.scale):
                button = tk.Button(self.root, textvariable=self.txt_list[self.scale * i + j])
                self.buttons.append(button)
                self.buttons[i * self.scale + j].grid(row=i, column=j, sticky="nsew")
        for i in range(self.scale ** 2):
            self.buttons[i].config(command=lambda f=i: self.change(f // self.scale, f % self.scale))
        bt = tk.Button(width=4, height=1, text='结束', command=self.popup)
        bt.grid(row=self.scale + 1, column=(self.scale - 1) // 2)
        bt2 = tk.Button(width=4, height=1, text='重置', command=self.back)
        bt2.grid(row=self.scale + 1, column=0)
        bt3 = tk.Button(width=4, height=1, text='随机', command=self.rand)
        bt3.grid(row=self.scale + 1, column=self.scale - 1)
        self.root.mainloop()

    def back(self):  # 回到初始状态
        for od in range(self.scale ** 2):
            self.txt_list[od].set(str(self.seq[od]))
        self.mny = 0

    def rand(self):  # 再次随机
        self.seq = []
        self.mny = 0
        if self.mode == 0:
            for _ in range(self.scale ** 2):
                nub = rd.randint(0, 1)
                self.seq.append(nub)
        else:
            rand = Answer(self.scale, self.rule)
            self.seq = rand.sol_sys()
        for __ in range(self.scale ** 2):
            self.txt_list[__].set(str(self.seq[__]))

    @staticmethod
    def dist(x, y):  # 定义距离, 用于编写规则
        return abs(x[0] - y[0]) + abs(x[1] - y[1])


if __name__ == '__main__':
    number = int(input('输入方阵规模(n阶):'))
    r = int(input("输入规则, 点击后多少距离的格子改变:"))
    m = int(input("是否保证必定有解(是1, 否0):"))
    Lattice(number, r, m).start_ui()
