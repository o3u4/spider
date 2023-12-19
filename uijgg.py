import tkinter as tk
import random as rd
import jgg

root = tk.Tk()
root.title('9步内点亮所有格子')
root.geometry("300x300")
# 创建九个按钮
buttons = []
seq = []
txt_list = []
mny = 0

for i in range(9):
    nb = rd.randint(0, 1)
    seq.append(nb)
    txt = tk.StringVar()
    txt_list.append(txt)

for i in range(9):
    txt_list[i].set(str(seq[i]))


def dist(x, y):
    return abs(x[0] - y[0]) + abs(x[1] - y[1])


def change(x, y):
    global mny
    for xi in range(3):
        for yj in range(3):
            if dist((x, y), (xi, yj)) <= 1:
                if txt_list[3 * xi + yj].get() == '0':
                    txt_list[3 * xi + yj].set('1')
                else:
                    txt_list[3 * xi + yj].set('0')
    mny += 1


# 使用grid布局排列按钮，并调整行和列的大小
for i in range(3):
    root.rowconfigure(i, weight=1)
    root.columnconfigure(i, weight=1)
    for j in range(3):
        button = tk.Button(root, textvariable=txt_list[3 * i + j])
        buttons.append(button)
        buttons[i * 3 + j].grid(row=i, column=j, sticky="nsew")
for i in range(9):
    buttons[i].config(command=lambda f=i: change(f // 3, f % 3))


def popup():
    num = 0
    for tx in txt_list:
        if tx.get() == '1':
            num += 1
    up = tk.Toplevel()
    up.geometry("200x60")
    label = tk.Label(up)
    if num == 9:
        label.config(text=f'共花了{mny}步完成!')
        label.pack()
    else:
        target = [1, 1, 1, 1, 1, 1, 1, 1, 1]
        ans_list = jgg.answer(seq, target)
        label.config(text='未完成')
        label.pack()
        lab = tk.Label(up)
        lab.config(text=f'答案为:{", ".join(str(x) for x in ans_list)}')
        lab.pack()


def back():
    global mny
    for od in range(9):
        txt_list[od].set(str(seq[od]))
    mny = 0


bt = tk.Button(width=4, height=1, text='结束', command=popup)
bt.grid(row=4, column=2)
bt = tk.Button(width=4, height=1, text='重置', command=back)
bt.grid(row=4, column=0)

root.mainloop()
