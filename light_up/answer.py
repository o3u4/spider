import random


class Answer:
    Base = []   # Ax = b 求解线性方程组

    def __init__(self, scale, rule):
        """
        生成特定规模和规则的矩阵
        :param scale: 规模
        :param rule: 规则
        """
        self.scale = scale
        self.rule = rule

    @staticmethod
    def dist(x, y):
        return abs(x[0] - y[0]) + abs(x[1] - y[1])

    def mat(self, i):
        """
        第 i 个元素及其周围为 1 的矩阵
        :param i:第 i 个元素
        :return:
        mi: 基矩阵
        """
        mi = []
        for x in range(self.scale):
            for y in range(self.scale):
                if self.dist((x, y), (i // self.scale, i % self.scale)) <= self.rule:
                    mi.append(1)
                else:
                    mi.append(0)
        return mi

    def gen_mat(self):
        """
        生成每个元素对应的基矩阵
        :return: self.Base里加入每个基矩阵
        """
        for item in range(self.scale ** 2):
            self.Base.append(self.mat(item))

    def add(self, m1, m2):
        """
        定义矩阵加法
        :param m1: 矩阵 1
        :param m2: 矩阵 2
        :return:
        相加后的新矩阵
        """
        new_m = []
        for i in range(self.scale ** 2):
            new_m.append((m1[i] + m2[i]) % 2)
        return new_m

    def prt(self):
        """
        格式化输出高斯消元过程
        :return:
        """
        for i in range(self.scale ** 2):
            for j in range(len(self.Base)):
                print(self.Base[j][i], end=' ')
                if j == self.scale ** 2 - 1:
                    print("|", end='')
            print()

    def row_add(self, i, j, mode=1):
        """
        行变换, 第i行加到第j行里
        :param i: 第i行
        :param j: 第j行
        :param mode: mode=1为增广矩阵, 0为系数矩阵
        :return:
        对 self.Base 的第j行做行变换
        """
        for x in range(self.scale ** 2 + mode):
            self.Base[x][j] = (self.Base[x][j] + self.Base[x][i]) % 2

    def row_change(self, i, j, mode=1):
        """
        行交换, i, j行交换
        :param i: 第i行
        :param j: 第j行
        :param mode: mode=1为增广矩阵, 0为系数矩阵
        :return:
        对 self.Base 的第i和j行做行交换
        """
        for x in range(self.scale ** 2 + mode):
            mid = self.Base[x][i]
            self.Base[x][i] = self.Base[x][j]
            self.Base[x][j] = mid

    def row_simplified(self, mode=1):
        """
        高斯消元法行化简
        :param mode: mode=1为增广矩阵, 0为系数矩阵
        :return:
        self.Base 为化简后的判别矩阵
        """
        for j in range(self.scale ** 2):
            position = []  # 第j列里1的位置
            for i in range(self.scale ** 2):
                if self.Base[j][i] == 1:
                    position.append(i)
            c_pos = -1  # 第1个大于等于j的非0元
            for f in position:
                if f >= j:
                    c_pos = f
                    break
            # print(c_pos)
            # print(position)
            if c_pos == -1:
                continue
            elif len(position) > 1:
                for p in position:
                    if p != c_pos:
                        self.row_add(c_pos, p, mode)
                if c_pos != j:
                    self.row_change(j, c_pos, mode)
            else:
                if c_pos != j:
                    self.row_change(j, c_pos, mode)
            # prt()
            # print('----------------------------------')

    def exam(self):
        """
        检查阶梯型判别矩阵是否满秩
        :return:
        是/否
        """
        flag = True
        for i in range(self.scale ** 2):
            if self.Base[i][i] == 0:
                flag = False
                break
            else:
                continue
        if not flag:
            # self.prt()
            # print("不满秩")
            return False
        else:
            return True

    def det(self):
        """
        判断是否有解
        :return:
        是/否
        """
        det = True
        for j in range(self.scale ** 2):
            if self.Base[self.scale ** 2][j] == 1 and self.Base[j][j] == 0:
                # print("无解")
                det = False
                break
        return det

    def answer(self, init, target):
        """
        计算答案
        :param init: 初始状态
        :param target: 目标状态
        :return:
        asw: 答案列表
        """
        self.Base = []      # 初始化判别矩阵
        self.gen_mat()      # 生成判别矩阵
        det_s = self.add(init, target)      # 初末状态相加
        self.Base.append(det_s)     # 添加到判别矩阵的增广列(b)
        self.row_simplified()       # 高斯消元法化简
        self.prt()          # 输出消元结果
        asw = []
        if self.exam() or self.det():
            for i in range(self.scale ** 2):
                if self.Base[self.scale ** 2][i] == 1:
                    asw.append(i + 1)
            if self.exam():
                print("满秩, 必有唯一解")
            else:
                print("不满秩, 但有解")
        else:
            print("无解")
        return asw

    def sol_sys(self):
        """
        解系, 通过对基矩阵的随机线性组合, 描述所有可能的解
        :return:
        生成随机的可行解
        """
        self.Base = []
        self.gen_mat()
        seq = [0 for x in range(self.scale ** 2)]
        for i in range(self.scale ** 2):
            if random.randint(0, 1) == 1:
                seq = self.add(seq, self.Base[i])
        return seq

    @classmethod
    def sol_list(cls, *scale_range):
        """
        查看所有情况的满秩解
        :param scale_range: 指定规模(默认为 3-9)
        :return:
        能够使特定规模有满秩解的规则
        默认输出 [[3, 1], [4, 2], [5], [6, 1, 3], [7, 1, 3], [8, 1], [9]]
        """
        f_sol = []
        if len(scale_range) == 0:
            default_a = 3
            default_b = 10
        elif len(scale_range) > 1:
            default_a = scale_range[0]
            default_b = scale_range[1]
        else:
            default_a = scale_range[0]
            default_b = scale_range[0]
        for f_j in range(default_a, default_b):
            f_s = [f_j]
            for i in range(1, f_j):
                f_a = Answer(f_j, i)
                f_a.Base = []
                f_a.gen_mat()
                f_a.row_simplified(0)
                if f_a.exam():
                    f_s.append(i)
            f_sol.append(f_s)
        print(f_sol)


if __name__ == '__main__':
    # Answer.sol_list(3, 10)       # [[3, 1], [4, 2], [5], [6, 1, 3], [7, 1, 3], [8, 1], [9]]
    x1 = [random.randint(0, 1) for x in range(4 * 4)]
    x2 = [random.randint(0, 1) for x in range(4 * 4)]
    a = Answer(4, 2)
    Asw = a.answer(x1, x2)
    print(Asw)
