import tkinter as tk
import random
import threading
import time


def win():
    window = tk.Tk()
    width = window.winfo_screenwidth()
    height = window.winfo_screenheight()
    a = random.randrange(0, width)
    b = random.randrange(0, height)
    window.title('abc')
    window.geometry("200x50" + "+" + str(a) + "+" + str(b))
    tk.Label(window,
             text='abc',
             bg='white',
             font=('楷体', 17),
             width=15, height=2
             ).pack()
    window.mainloop()


if __name__ == '__main__':
    thread = []
    for i in range(100):
        t = threading.Thread(target=win)
        thread.append(t)
        time.sleep(0.1)
        thread[i].start()
