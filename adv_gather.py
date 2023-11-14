import os
from bar import Bar


# file_lst = ['c.txt', 'b.txt', 'a.txt']    # 按指定顺序合并

class Gather:
    def __init__(self, folder_path, target_path, order_list=None, read_file=None,
                 root=None,  label=None):
        self.folder_path = folder_path  # 合并前文件夹
        self.target_path = target_path  # 合并后路径
        self.root = root
        self.label = label  # 进程显示标签
        self.order_list = order_list  # 文件顺序
        self.read_file = read_file  # 从其他文件读取顺序
        self.total = 1  # 合并总量

    def prt_prg(self, prg):
        Bar(self.total).prt(prg)

    def prt_prg_label(self, prg):
        Bar(self.total).label_prt(prg, self.label, self.root)

    def file_gather(self):
        if self.order_list is None:  # 判断是否默认顺序
            if self.read_file is None:
                self.order_list = os.listdir(self.folder_path)
            else:
                with open(self.read_file, 'r') as file:
                    lines = file.readlines()
                    lines = [line.strip() for line in lines]
                self.order_list = lines
        # print('顺序为:', self.order_list)
        self.total = len(self.order_list)
        i = 0
        with open(self.target_path, 'wb') as merged_file:
            for file_name in self.order_list:
                file_path = self.folder_path + '/' + file_name
                with open(file_path, 'rb') as f:
                    merged_file.write(f.read())
                    i += 1
                    self.prt_prg(i)  # 输出进度
                    if self.root and self.label:
                        self.prt_prg_label(i)  # 在标签输出进度


if __name__ == '__main__':
    Gather('F:/ts_list', 'F:/mv/s.mp4', ['0AgJF6sl.ts',
                                         '00psSh46.ts', '0ALvDEaH.ts']).file_gather()
