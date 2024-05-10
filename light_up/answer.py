import random


class Answer:
    Base = []

    def __init__(self, scale, rule):
        self.scale = scale
        self.rule = rule

    @staticmethod
    def dist(x, y):
        return abs(x[0] - y[0]) + abs(x[1] - y[1])

    def mat(self, i):
        mi = []
        for x in range(self.scale):
            for y in range(self.scale):
                if self.dist((x, y), (i // self.scale, i % self.scale)) <= self.rule:
                    mi.append(1)
                else:
                    mi.append(0)
        return mi

    def gen_mat(self):
        for item in range(self.scale ** 2):
            self.Base.append(self.mat(item))

    def add(self, m1, m2):
        new_m = []
        for i in range(self.scale ** 2):
            new_m.append((m1[i] + m2[i]) % 2)
        return new_m

    def prt(self):
        for i in range(self.scale ** 2):
            for j in range(len(self.Base)):
                print(self.Base[j][i], end=' ')
                if j == self.scale ** 2 - 1:
                    print("|", end='')
            print()

    def row_add(self, i, j, mode=1):
        # 第i行加到第j行里, mode=1为增广矩阵, 0为系数矩阵
        for x in range(self.scale ** 2 + mode):
            self.Base[x][j] = (self.Base[x][j] + self.Base[x][i]) % 2

    def row_change(self, i, j, mode=1):
        # i, j行交换, mode=1为增广矩阵, 0为系数矩阵
        for x in range(self.scale ** 2 + mode):
            mid = self.Base[x][i]
            self.Base[x][i] = self.Base[x][j]
            self.Base[x][j] = mid

    def row_simplified(self, mode=1):
        # 高斯消元法行化简, mode=1为增广矩阵, 0为系数矩阵
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
        # 检查阶梯型是否满秩
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
        # 判断是否有解
        det = True
        for j in range(self.scale ** 2):
            if self.Base[self.scale ** 2][j] == 1 and self.Base[j][j] == 0:
                # print("无解")
                det = False
                break
        return det

    def answer(self, init, target):
        self.Base = []
        self.gen_mat()
        det_s = self.add(init, target)
        self.Base.append(det_s)
        self.row_simplified()
        self.prt()
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
        self.Base = []
        self.gen_mat()
        seq = [0 for x in range(self.scale ** 2)]
        for i in range(self.scale ** 2):
            if random.randint(0, 1) == 1:
                seq = self.add(seq, self.Base[i])
        return seq

    @classmethod
    def sol_list(cls):  # 查看所有情况的满秩解
        f_sol = []
        for f_j in range(3, 10):
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
    # Answer.sol_list()
    x1 = [random.randint(0, 1) for x in range(4 * 4)]
    x2 = [random.randint(0, 1) for x in range(4 * 4)]
    a = Answer(4, 2)
    Asw = a.answer(x1, x2)
    print(Asw)
